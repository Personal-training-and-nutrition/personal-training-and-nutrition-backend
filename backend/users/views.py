from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.forms import LoginForm

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    # Функция регистрации
    @action(detail=False, methods=['post'])
    def register(self, request):
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'password_confirmation': request.data.get('password_confirmation'),
            # По умолчанию is_specialist=False
            'is_specialist': request.data.get('is_specialist', False)
        }

        # Проверка пользователя с переданным email
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {'error': 'Пользователь с таким email уже существует.'},
                status=status.HTTP_400_BAD_REQUEST)

        # Проверка на совпадения паролей
        if data['password'] != data['password_confirmation']:
            return Response({'error': 'Пароли не совпадают.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Создание пользователя
        user, _ = User.objects.get_or_create(email=data['email'],
                                             defaults={
            'is_specialist': data['is_specialist'],
            'last_name': request.data.get('last_name'),
            'first_name': request.data.get('first_name'),
            'date_of_birth': request.data.get('date_of_birth'),
            'gender': request.data.get('gender'),
            'weight': request.data.get('weight'),
            'height': request.data.get('height'),
            'phone_number': request.data.get('phone_number'),
            'password': data['password'],
        })

        send_mail(
            'Успешная регистрация',
            f'Добро пожаловать, '
            f'Ваш адрес электронной почты: {data.get("email")}.',
            'from@example.com',
            [data.get('email')],
            fail_silently=False,
        )

        return Response(UserSerializer(user).data,
                        status=status.HTTP_201_CREATED)

    # Функция для входа
    @action(detail=False, methods=['post'])
    def login(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            email_or_phone = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']
            user = authenticate(
                request, email=email_or_phone, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Успешный вход'})

            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
