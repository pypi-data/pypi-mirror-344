from core.test_helpers import create_test_interactive_user
from rest_framework import status
from rest_framework.test import APITestCase
from dataclasses import dataclass
from graphql_jwt.shortcuts import get_token
from core.models import User
from django.conf import settings
from django.db import connection


from core.models.openimis_graphql_test_case import BaseTestContext as DummyContext


class ReportAPITests(APITestCase):

    admin_user = None
    admin_token = None
    POI_URL = f"/{settings.SITE_ROOT()}report/policy_primary_operational_indicators/pdf/?yearMonth=2019-04-01"
    PR_URL = f"/{settings.SITE_ROOT()}report/policy_renewals/pdf/?date_start=2019-04-01&date_end=2019-04-30"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = create_test_interactive_user(username="testLocationAdmin")
        cls.admin_token = get_token(cls.admin_user, DummyContext(user=cls.admin_user))

    def test_primary_operational_indicators_report(self):
        if not connection.vendor == "postgresql":
            self.skipTest("This test can only be executed for MSSQL database")
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        response = self.client.get(self.POI_URL, format="application/pdf", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = b"".join(response.streaming_content)
        self.assertTrue(len(content) > 0)

    def test_policy_renewal_report(self):
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        response = self.client.get(self.PR_URL, format="application/pdf ", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = b"".join(response.streaming_content)
        self.assertTrue(len(content) > 0)
