from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPagination
from users.forms import LoginForm

from .models import User
from .serializers import SpecialistSerializer, UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['post'])
    def register(self, request):
        data = {
            # 'first_name': request.data.get('first_name'),
            # 'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'password_confirmation': request.data.get('password_confirmation'),
            'is_specialist': request.data.get('is_specialist', False)
        }

        user = User.objects.create_user(
            email=data['email'], password=data['password'])

        if data['is_specialist']:
            # Создание профиль специалиста
            specialist_data = {
                'user': user,
                # Добавление доп полей, относящиеся к профилю специалиста
            }
            specialist_serializer = SpecialistSerializer(data=specialist_data)
            if specialist_serializer.is_valid():
                specialist_serializer.save()
            else:
                user.delete()
                return Response(specialist_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            # Создание профиля клиента и сохранения доп инф
            client_data = {
                'user': user,
            }
            client_serializer = UserSerializer(data=client_data)
            if client_serializer.is_valid():
                client_serializer.save()
            else:
                user.delete()
                return Response(client_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

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
