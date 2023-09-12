from rest_framework import status
from api.pagination import CustomPagination
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomUserSerializer, RoleSerializer


class CustomUserViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['post'])
    def register(self, request):
        data = request.data
        serializer = RoleSerializer(data={'role': data.get('role')})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = self.get_serializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        send_mail(
            'Успешная регистрация',
            'Добро пожаловать!',
            'from@example.com',
            [data.get('email')],
            fail_silently=False,
        )
        return Response(user_serializer.data, status=201)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            return Response({'error': 'Wrong email or password.'}, status=400)
        refresh = RefreshToken.for_user(user)
        return Response(
            {'refresh': str(refresh), 'access': str(refresh.access_token)}
        )

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        password = request.data.get('password')
        user = self.get_object()
        user.password = make_password(password)
        user.save()
        return Response({'message': 'Пароль изменен успешно'})
