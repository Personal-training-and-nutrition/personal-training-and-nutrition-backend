from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse_lazy
from rest_framework import status

import json

from api.serializers import ClientAddSerializer, ClientListSerializer
from api.views import ClientsViewSet
from users.models import SpecialistClient

User = get_user_model()


class ClientsViewSetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.specialist = User.objects.create_user(
            email="specialist@test.com", password="testpassword"
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
        cache.clear()

    def test_perform_create(self):
        response = self.client.post(
            path="/api/clients",
            data=json.dumps({
                "user": {
                    "first_name": "string",
                    "last_name": "string",
                    "middle_name": "string",
                    "role": "0",
                    "email": "user@example.com",
                    "phone_number": "344+70564583",
                    "dob": "2023-10-17",
                    "params": {"weight": 0, "height": 0, "waist_size": 0},
                    "capture": "string",
                },
                "diseases": "string",
                "exp_diets": "string",
                "exp_trainings": "string",
                "bad_habits": "string",
                "notes": "string",
                "food_preferences": "string",
            }),
            content_type="application/json",
        )
        print(dir(response), response.headers, response.context)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming there was one client already
        self.assertEqual(SpecialistClient.objects.count(), 2)

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
