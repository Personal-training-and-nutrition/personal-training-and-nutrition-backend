import json

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from rest_framework import status

from api.serializers import ClientAddSerializer, ClientListSerializer
from api.views import ClientsViewSet
from users.models import Gender, SpecialistClient

User = get_user_model()


class ClientsViewSetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gender = Gender.objects.create()
        cls.specialist = User.objects.create_user(
            email='specialist@test.com',
            password='testpassword'
        )
        cls.client_user = User.objects.create_user(
            first_name="user_name",
            last_name="user_surname",
            email='client@test.com',
            password='testpassword'
        )
        cls.client_obj = SpecialistClient.objects.create(
            specialist=ClientsViewSetTests.specialist,
            user=ClientsViewSetTests.client_user
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(ClientsViewSetTests.specialist)
        cache.clear()

    def test_perform_create(self):
        print("CLIENT USER: ", dir(ClientsViewSetTests.client_user),
              ClientsViewSetTests.client_user,
              ClientsViewSetTests.gender.__dict__
              )
        response = self.client.post(
            '/api/clients/', {'specialist': ClientsViewSetTests.specialist.id}
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
        self.assertEqual(response_data, expected_data)

    def test_get_queryset(self):
        response = self.client.get('/api/clients/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming only one client for this specialist
        self.assertEqual(len(response.data), 1)
