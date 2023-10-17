import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.serializers import ClientAddSerializer, ClientListSerializer
from api.views import ClientsViewSet
from users.models import SpecialistClient

User = get_user_model()


class ClientsViewSetTests(TestCase):
    def setUp(self):
        # Set up a test user and client data for testing
        self.specialist = User.objects.create_user(
            email='specialist@test.com',
            password='testpassword'
        )
        self.client_user = User.objects.create_user(
            first_name="user_name",
            last_name="user_surname",
            email='client@test.com',
            password='testpassword'
        )
        self.client_obj = SpecialistClient.objects.create(
            specialist=self.specialist, user=self.client_user
        )

        # Set up an API client for making requests
        self.client = APIClient()

    def test_perform_create(self):
        # Log in the specialist user
        self.client.login(
            email='specialist@test.com', password='testpassword'
        )
        print("CLIENT USER: ", dir(self.client_user), self.client_user)
        response = self.client.post(
            '/api/clients/', {'user': self.client_user.id}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming there was one client already
        self.assertEqual(SpecialistClient.objects.count(), 2)

    def test_get_serializer_class_list(self):
        view = ClientsViewSet()
        view.action = 'list'
        serializer_class = view.get_serializer_class()

        self.assertEqual(serializer_class, ClientListSerializer)

    def test_get_serializer_class_other_actions(self):
        view = ClientsViewSet()
        # Assuming this is an action where ClientAddSerializer should be used
        view.action = 'create'
        serializer_class = view.get_serializer_class()

        self.assertEqual(serializer_class, ClientAddSerializer)

    def test_retrieve(self):
        # Log in the specialist user
        self.client.login(
            email='specialist@test.com', password='testpassword'
        )
        response = self.client.get(f'/api/clients/{self.client_user.id}/')
        serialized_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = {
            'first_name': serialized_response.get("first_name"),
            'last_name': serialized_response.get("last_name"),
            'email': serialized_response.get("email"),
            'age': serialized_response.get("age"),
        }
        expected_data = {
            'first_name': self.client_user.first_name,
            'last_name': self.client_user.last_name,
            'email': self.client_user.email,
            'age': "Возраст не указан",
        }
        print(serialized_response, expected_data)
        self.assertEqual(response_data, expected_data)

    def test_get_queryset(self):
        # Log in the specialist user
        self.client.login(
            email='specialist@test.com', password='testpassword'
        )

        response = self.client.get('/api/clients/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming only one client for this specialist
        self.assertEqual(len(response.data), 1)
