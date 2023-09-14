from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPagination
from users.forms import LoginForm

from .serializers import CustomUserSerializer, RoleSerializer


class CustomUserViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['post'])
    def register(self, request):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'password_confirmation': request.data.get('password_confirmation'),
            'role': request.data.get('role')
        }

        serializer = RoleSerializer(data={'role': data.get('role')})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = self.get_serializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        if data.get('password') != data.get('password_confirmation'):
            return Response(
                {'error': 'Пароли не совпадают'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_serializer.save()

        send_mail(
            'Успешная регистрация',
            f'Добро пожаловать, {data.get("first_name")} '
            f'{data.get("last_name")}! '
            f'Ваш адрес электронной почты: {data.get("email")}.',
            'from@example.com',
            [data.get('email')],
            fail_silently=False,
        )

        return Response(user_serializer.data, status=201)


class LoginView(APIView):
    def post(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            email_or_phone = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']
            user = authenticate(
                request, email=email_or_phone, password=password
            )
            if user is not None:
                login(request, user)
                return Response({'message': 'Успешный вход'})

            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
