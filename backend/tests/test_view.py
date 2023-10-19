from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

import json

from api.serializers import ClientAddSerializer, ClientListSerializer, Gender, Role
from api.views import ClientsViewSet, TrainingPlanViewSet, DietPlanViewSet
from users.models import SpecialistClient
from workouts.models import TrainingPlan
from diets.models import DietPlan

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ClientsViewSetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gender = Gender.objects.create(id=0)
        cls.role = Role.objects.create(role=0)
        cls.specialist = User.objects.create_user(
            email="specialist@test.com",
            password="testpassword",
            is_superuser=True,
            is_specialist=True,
            is_staff=True
        )
        cls.client_user = User.objects.create_user(
            first_name="user_name",
            last_name="user_surname",
            email="client@test.com",
            password="testpassword",
        )
        cls.client_obj = SpecialistClient.objects.create(
            specialist=ClientsViewSetTests.specialist,
            user=ClientsViewSetTests.client_user,
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(ClientsViewSetTests.specialist)
        self.factory = APIRequestFactory()
        cache.clear()

    def test_api_client_create(self):
        request = self.factory.post(
            "/api/clients/",
            data={
                "user": {
                    "first_name": "string",
                    "last_name": "string",
                    "middle_name": "string",
                    "role": "0",
                    "email": "user@exa.com",
                    "phone_number": ")74)51815(28+)+",
                    "dob": "2023-10-18",
                    "gender": 0,
                    "params": {
                        "weight": 0,
                        "height": 0,
                        "waist_size": 0
                    },
                    "capture": "string"
                },
                "diseases": "string",
                "exp_diets": "string",
                "exp_trainings": "string",
                "bad_habits": "string",
                "notes": "string",
                "food_preferences": "string"
            },
            format='json'
        )
        view = ClientsViewSet.as_view({"get": "detail", "post": "create"})
        force_authenticate(request, user=ClientsViewSetTests.specialist)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpecialistClient.objects.count(), 2)

    def test_api_diet_plans_create(self):
        request = self.factory.post(
            "/api/diet-plans/",
            {
                "specialist": ClientsViewSetTests.specialist.id,
                "user": ClientsViewSetTests.client_user.id,
                "name": "some string",
                "kkal": 10000,
                "protein": 500,
                "carbo": 1000,
                "fat": 300,
                "describe": "another string",
                "diet": [
                    {
                        "weekday": "1",
                        "spec_comment": "string",
                        "user_comment": "string"
                    }
                ]
            },
            format='json'
        )
        view = DietPlanViewSet.as_view({"get": "detail", "post": "create"})
        force_authenticate(request, user=ClientsViewSetTests.specialist)
        response = view(request)
        self.assertEqual(DietPlan.objects.count(), 1)
        self.assertEqual(response.status_code, 201)

    def test_api_training_plans_create(self):
        request = self.factory.post(
            "/api/training-plans/",
            {
                "specialist": ClientsViewSetTests.specialist.id,
                "user": ClientsViewSetTests.client_user.id,
                "name": "some string",
                "describe": "another string",
                "training": [
                    {
                        "weekday": "1",
                        "spec_comment": "string",
                        "user_comment": "string"
                    }
                ]
            },
            format='json'
        )
        view = TrainingPlanViewSet.as_view({"get": "detail", "post": "create"})
        force_authenticate(request, user=ClientsViewSetTests.specialist)
        response = view(request)
        self.assertEqual(TrainingPlan.objects.count(), 1)
        self.assertEqual(response.status_code, 201)

    def test_api_users_create(self):
        response = self.client.post(
            "/api/users/",
            {
                "password": "stringwithsomerandoMneSs",
                "email": "user@ex.com",
                "re_password": "stringwithsomerandoMneSs"
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_get_serializer_class_list(self):
        view = ClientsViewSet()
        view.action = "list"
        serializer_class = view.get_serializer_class()

        self.assertEqual(serializer_class, ClientListSerializer)

    def test_get_serializer_class_other_actions(self):
        view = ClientsViewSet()
        # Assuming this is an action where ClientAddSerializer should be used
        view.action = "create"
        serializer_class = view.get_serializer_class()

        self.assertEqual(serializer_class, ClientAddSerializer)

    def test_retrieve(self):
        response = self.client.get(f"/api/clients/{self.client_user.id}/")
        serialized_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = {
            "first_name": serialized_response.get("first_name"),
            "last_name": serialized_response.get("last_name"),
            "email": serialized_response.get("email"),
            "age": serialized_response.get("age"),
        }
        expected_data = {
            "first_name": self.client_user.first_name,
            "last_name": self.client_user.last_name,
            "email": self.client_user.email,
            "age": "Возраст не указан",
        }
        self.assertEqual(response_data, expected_data)

    def test_get_queryset(self):
        response = self.client.get("/api/clients/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming only one client for this specialist
        self.assertEqual(len(response.data), 1)
