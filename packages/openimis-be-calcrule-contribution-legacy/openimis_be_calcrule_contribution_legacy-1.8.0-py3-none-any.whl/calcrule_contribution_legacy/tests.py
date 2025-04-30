import base64
from unittest import mock
from django.test import TestCase

import graphene
from product.test_helpers import create_test_product
from policy.test_helpers import create_test_policy
from contract.models import Contract, ContractDetails
from core.models import TechnicalUser, User
from core.models.openimis_graphql_test_case import openIMISGraphQLTestCase, BaseTestContext
from core.test_helpers import create_test_interactive_user
from policyholder.tests.helpers import create_test_policy_holder_insuree, create_test_policy_holder
from contribution_plan.tests.helpers import create_test_contribution_plan, \
    create_test_contribution_plan_bundle, create_test_contribution_plan_bundle_details
from contract import schema as contract_schema
from graphene import Schema
from graphene.test import Client
from graphene_django.utils.testing import GraphQLTestCase
from django.conf import settings
import json
import uuid
from graphql_jwt.shortcuts import get_token
from calcrule_contribution_legacy.calculation_rule import ContributionPlanCalculationRuleProductModeling
import datetime
from core.models.openimis_graphql_test_case import BaseTestContext

class MutationTestContract(openIMISGraphQLTestCase):
    GRAPHQL_URL = f'/{settings.SITE_ROOT()}graphql'
    # This is required by some version of graphene but is never used. It should be set to the schema but the import
    # is shown as an error in the IDE, so leaving it as True.
    GRAPHQL_SCHEMA = True
    admin_user = None
    schema = Schema(
        query=contract_schema.Query,
    )


    @classmethod
    def setUpClass(cls):
        super(MutationTestContract, cls).setUpClass()
        cls.user = User.objects.filter(username='admin', i_user__isnull=False).first()
        if not cls.user:
            cls.user = create_test_interactive_user(username='admin')
        # some test data so as to created contract properly
        cls.user_token = BaseTestContext(user=cls.user).get_jwt()

        cls.income = 500
        cls.rate = 5
        cls.number_of_insuree = 2
        cls.policy_holder = create_test_policy_holder()
        product = create_test_product("PlanCode", custom_props={"lump_sum": 200})

        # create contribution plans etc
        cls.contribution_plan_bundle = create_test_contribution_plan_bundle()
        cls.contribution_plan = create_test_contribution_plan(
            product=product,
            calculation=ContributionPlanCalculationRuleProductModeling.uuid,
            custom_props={"json_ext": {"calculation_rule": {"rate": cls.rate}}}
        )
        cls.contribution_plan_bundle_details = create_test_contribution_plan_bundle_details(
            contribution_plan=cls.contribution_plan,
            contribution_plan_bundle=cls.contribution_plan_bundle
        )
        from core import datetime
        # create policy holder insuree for that test policy holder
        for i in range(0, cls.number_of_insuree):
            ph_insuree = create_test_policy_holder_insuree(
                policy_holder=cls.policy_holder,
                contribution_plan_bundle=cls.contribution_plan_bundle,
                custom_props={
                    "last_policy": None
                }
            )
            create_test_policy(
                cls.contribution_plan.benefit_plan,
                ph_insuree.insuree,
                custom_props={
                    "start_date": datetime.datetime(2016, 3, 1),
                    "expiry_date": datetime.datetime(2021, 7, 1)
                }
            )

        cls.policy_holder_insuree = create_test_policy_holder_insuree(
            policy_holder=cls.policy_holder,
            contribution_plan_bundle=cls.contribution_plan_bundle
        )
        cls.policy_holder_insuree2 = create_test_policy_holder_insuree(
            policy_holder=cls.policy_holder,
            contribution_plan_bundle=cls.contribution_plan_bundle
        )

        cls.schema = Schema(
            query=contract_schema.Query,
            mutation=contract_schema.Mutation
        )
        cls.graph_client = Client(cls.schema)

    def test_mutation_contract_create_with_policy_holder(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "code": "XYZ:" + str(time_stamp),
            "policyHolderId": str(self.policy_holder.id),
            "clientMutationId": str(uuid.uuid4()),
            "dateValidFrom": str(time_stamp.date()),
            "dateValidTo": str((time_stamp + datetime.timedelta(days=30)).date())
        }
        content = self.send_mutation("createContract", input_param, self.user_token)
        self.assertEqual(content['data']['mutationLogs']['edges'][0]['node']['status'], 2)
        del input_param["clientMutationId"]
        result = self.find_by_exact_attributes_query(
            "contract",
            params=input_param,
        )["edges"]
        converted_id = base64.b64decode(result[0]['node']['id']).decode('utf-8').split(':')[1]

        # SUBMIT
        input_param = {
            'id': converted_id,
            "clientMutationId": str(uuid.uuid4())
        }
        content = self.send_mutation("submitContract", input_param, self.user_token)
        self.assertEqual(content['data']['mutationLogs']['edges'][0]['node']['status'], 2)

        # COUNTER
        input_param = {
            'id': converted_id,
            "clientMutationId": str(uuid.uuid4())
        }
        content = self.send_mutation("counterContract", input_param, self.user_token)

        self.assertEqual(content['data']['mutationLogs']['edges'][0]['node']['status'], 2)

        # reSUBMIT
        input_param = {
            'id': converted_id,
            "clientMutationId": str(uuid.uuid4())
        }
        content = self.send_mutation("submitContract", input_param, self.user_token)
        self.assertEqual(content['data']['mutationLogs']['edges'][0]['node']['status'], 2)
        # Approve
        input_param = {
            'id': converted_id,
            "clientMutationId": str(uuid.uuid4())
        }
        content = self.send_mutation("approveContract", input_param, self.user_token)

        self.assertEqual(content['data']['mutationLogs']['edges'][0]['node']['status'], 2)

        # tear down the test data (TODO FK conflict with mutation )
        # ContractDetails.objects.filter(contract_id=str(converted_id)).delete()
        # ontract.objects.filter(id=str(converted_id)).delete()


    def find_by_id_query(self, query_type, id, context=None):
        query = F'''
        {{
            {query_type}(id:"{id}") {{
                totalCount
                edges {{
                  node {{
                    id
                    version
                  }}
                  cursor
                }}
          }}
        }}
        '''

        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]['edges']

        if len(records) > 1:
            raise ValueError(F"Ambiguous id {id} for query {query_type}")

        return records

    def find_by_exact_attributes_query(self, query_type, params, context=None):
        if "dateValidFrom" in params:
            params.pop('dateValidFrom')
        if "clientMutationId" in params:
            params.pop('clientMutationId')
        if "dateValidTo" in params:
            params.pop('dateValidTo')
        if "policyHolderId" in params:
            params.pop('policyHolderId')
        if "contributionPlanBundleId" in params:
            params.pop('contributionPlanBundleId')
        if "insureeId" in params:
            params.pop('insureeId')
        if "uuids" in params:
            params["id"] = params["uuids"][0]
            params.pop("uuids")
        node_content_str = "\n".join(params.keys()) if query_type == "contract" else ''
        query = F'''
        {{
            {query_type}({(
                'contract_Id: "' + str(params["contractId"]) + '", orderBy: ["-dateCreated"]'
                if "contractId" in params else
                self.build_params(params))
                }) {{
                totalCount
                edges {{
                  node {{
                    id
                    {node_content_str}
                    version
                    {'amountDue' if query_type == 'contract' else ''}
                    {'amountNotified' if query_type == 'contract' else ''}
                    {'amountRectified' if query_type == 'contract' else ''}
                    {'state' if query_type == 'contract' else ''}
                    {'paymentReference' if query_type == 'contract' else ''}
                  }}
                  cursor
                }}
          }}
        }}
        '''
        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]
        return records

    def execute_query(self, query, context=None):
        if context is None:
            context = BaseTestContext(self.user).get_request()

        query_result = self.graph_client.execute(query, context=context)
        query_data = query_result['data']
        return query_data

    def add_mutation(self, mutation_type, input_params, context=None):

        if "clientMutationId" not in input_params:
            input_params["clientMutationId"] = str(uuid.uuid4())
        mutation = f'''
        mutation
        {{
            {mutation_type}(input: {{
               {self.build_params(input_params)}
            }})

          {{
            internalId
            clientMutationId
          }}
        }}
        '''
        mutation_result = self.query(
            mutation,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.user_token}"},
        )
        self.assertResponseNoErrors(mutation_result)
        content = json.loads(mutation_result.content)
        return content


    def execute_mutation(self, mutation, context=None):
        if context is None:
            context = BaseTestContext(self.user).get_request()

        mutation_result = self.graph_client.execute(mutation, context=context)
        return mutation_result

    def build_params(self, params):
        def wrap_arg(v):
            if isinstance(v, str):
                return F'"{v}"'
            if isinstance(v, list):
                return json.dumps(v)
            if isinstance(v, bool):
                return str(v).lower()
            if isinstance(v, datetime.date):
                return graphene.DateTime.serialize(
                    datetime.datetime.fromordinal(v.toordinal()))
            return v

        params_as_args = [f'{k}:{wrap_arg(v)}' for k, v in params.items()]
        return ", ".join(params_as_args)
