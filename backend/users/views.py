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

    @action(detail=False, methods=['get'])
    def client_profile(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'client':
            profile_data = {
                'initials': user.first_name[0] + user.last_name[0],
                'patronymic': user.patronymic,
                'birth_date': user.birth_date,
                'gender': user.gender,
                'weight': user.weight,
                'height': user.height
            }
            return Response(profile_data, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Вы не авторизованы или не являетесь клиентом'},
            status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['put'])
    def edit_client_profile(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'client':
            user.patronymic = request.data.get('patronymic', user.patronymic)
            user.birth_date = request.data.get('birth_date', user.birth_date)
            user.gender = request.data.get('gender', user.gender)
            user.weight = request.data.get('weight', user.weight)
            user.height = request.data.get('height', user.height)
            user.save()
            return Response(
                {'message': 'Профиль успешно отредактирован'},
                status=status.HTTP_200_OK)

        return Response(
            {'error': 'Вы не авторизованы или не являетесь клиентом'},
            status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['put'])
    def edit_password(self, request):
        user = request.user
        if user.is_authenticated:
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            confirm_new_password = request.data.get('confirm_new_password')

            if new_password != confirm_new_password:
                return Response(
                    {'error': 'Новый пароль и подтверждение не совпадают'},
                    status=status.HTTP_400_BAD_REQUEST)

            if not user.check_password(old_password):
                return Response(
                    {'error': 'Старый пароль неверен'},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'message': 'Пароль успешно обновлен'},
            status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_profile(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'client':
            user.delete()
            return Response(
                {'message': 'Профиль успешно удален'},
                status=status.HTTP_200_OK)

        return Response(
            {'error': 'Вы не авторизованы или не являетесь клиентом'},
            status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def specialist_profile(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'specialist':
            profile_data = {
                'name': user.first_name,
                'initial': user.first_name[0] + user.last_name[0]
            }
            return Response(profile_data, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Вы не авторизованы или не являетесь специалистом'},
            status=status.HTTP_401_UNAUTHORIZED)


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
