from typing import Reversible
from home.api.v1.viewsets import AppViewSet, PlanViewSet, SubscriptionViewSet
from home.models import App, Plan, Subscription
from rest_framework import status
from django.test import TestCase, Client


class AppTestCase(TestCase):
    def setUp(self):

        App.objects.create(
            id="999",
            name="apptest1",
            description="app decsription 1",
            type="web",
            framework="django",
            domain_name="google"
        )

        App.objects.create(
            id="9999",
            name="apptest2",
            description="app decsription 2",
            type="web",
            framework="django",
            domain_name="google"
        )

    def test_get_apps(self):
        client = Client()
        response = client.get('/api/v1/apps/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'apptest1')

    def test_get_app_by_id(self):
        client = Client()
        response = client.get('/api/v1/apps/999/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'apptest1')

    def test_create_app(self):
        client = Client()
        test_app_object = {
            "name": "testapp",
            "description": "test app decsription",
            "type": "web",
            "framework": "django",
            "domain_name": "yahoo"
        }
        response = client.post('/api/v1/apps/', test_app_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'testapp')

    def test_update_app(self):
        client = Client()
        test_app_object = {
            "name": "updatedname",
            "description": "updated desc",
            "type": "web",
            "framework": "django",
            "domain_name": "bing"
        }
        response = client.put('/api/v1/apps/999/',
                              test_app_object, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updatedname')

    def test_delete_app_by_id(self):
        client = Client()
        response = client.delete('/api/v1/apps/999/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PlanTestCase(TestCase):
    def setUp(self):
        Plan.objects.create(
            id="999",
            name="plantest1",
            description="plan decsription 1",
            price=10
        )

    def test_get_plans(self):
        client = Client()
        response = client.get('/api/v1/plans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'plantest1')

    def test_get_plan_by_id(self):
        client = Client()
        response = client.get('/api/v1/plans/999/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'plantest1')

    def test_create_plan(self):
        client = Client()
        test_app_object = {
            "name": "testplan",
            "description": "test plan decsription",
            "price": 0
        }
        response = client.post('/api/v1/plans/', test_app_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'testplan')


class SubscriptionTestCase(TestCase):
    def setUp(self):
        Plan.objects.create(
            id="199",
            name="plantest101",
            description="plan decsription 101",
            price=10
        )
        Plan.objects.create(
            id="999",
            name="plantest1",
            description="plan decsription 1",
            price=10
        )
        App.objects.create(
            id="9999",
            name="apptest2",
            description="app decsription 2",
            type="web",
            framework="django",
            domain_name="google"
        )
        Subscription.objects.create(
            id="999",
            plan=Plan.objects.get(id="999"),
            app=App.objects.get(id="9999"),
            active=True
        )

    def test_get_apps(self):
        client = Client()
        response = client.get('/api/v1/subscriptions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_subscription_by_id(self):
        client = Client()
        response = client.get('/api/v1/subscriptions/999/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 999)

    def test_create_subscription(self):
        client = Client()
        test_subs_object = {
            "plan": 199,
            "app": 9999,
            "active": True
        }
        response = client.post('/api/v1/subscriptions/',
                               test_subs_object, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['plan'], 199)

    def test_update_app(self):
        client = Client()
        test_subs_object = {
            "plan": 999,
            "app": 9999,
            "active": True
        }
        response = client.put('/api/v1/subscriptions/999/',
                              test_subs_object, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plan'], 999)

    def test_delete_subscription_by_id(self):
        client = Client()
        response = client.delete('/api/v1/subscriptions/999/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
