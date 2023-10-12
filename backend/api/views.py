from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from djoser.conf import settings
from djoser.views import UserViewSet
from users.models import SpecialistClient
from workouts.models import TrainingPlan

from diets.models import DietPlan

from .permissions import ClientOrAdmin, SpecialistOrAdmin
from .serializers import (ClientListSerializer, DietListSerializer,
                          DietPlanLinkSerializer, DietPlanSerializer,
                          TrainingPlanSerializer, WorkoutListSerializer,)

User = get_user_model()


class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSerializer
    queryset = TrainingPlan.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']


class DietPlanViewSet(viewsets.ModelViewSet):
    serializer_class = DietPlanSerializer
    queryset = DietPlan.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(detail=True, methods=['post'])
    def send_link(self, request, pk=None):
        """
        Генерация ссылки и отправка плана питания.
        """
        diet_plan = self.get_object()
        link = "http://127.0.0.1:8000/api/diet-plans/{0}".format(diet_plan.pk)
        # В этой части нужно реализовать логику отправки, например,
        # отправку письма или сообщения
        serializer = DietPlanLinkSerializer(data={'diet_plan_id': diet_plan.pk,
                                                  'link': link})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(UserViewSet):
    permission_classes = settings.PERMISSIONS.user

    def destroy(self, request, *args, **kwargs):
        """Вместо удаления меняется флаг is_active"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=False)
        # if instance == request.user:
        #     utils.logout_user(self.request)
        request.user.is_active = False
        request.user.save()
        return Response(f'Пользователь {request.data["email"]}удалён.',
                        status=status.HTTP_200_OK)

    @action(["post"], detail=False, permission_classes=(AllowAny,))
    def user_restore(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=request.data["email"])
        if user.check_password(request.data["password"]):
            User.objects.activate_user(user)
            return Response(f'Пользователь {request.data["email"]} '
                            f'восстановлен.',
                            status=status.HTTP_200_OK)
        return Response("Неверный пароль", status=status.HTTP_400_BAD_REQUEST)

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        """Кастомная смена пароля"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        if settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[ClientOrAdmin])
    def get_workout_programs(self, serializer):
        """Вывод программ тренировок клиента"""
        programs = TrainingPlan.objects.filter(user=self.request.user)
        serializer = WorkoutListSerializer(programs, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'],
            permission_classes=[ClientOrAdmin])
    def get_diet_programs(self, serializer):
        """Вывод программ питания клиента"""
        programs = DietPlan.objects.filter(user=self.request.user)
        serializer = DietListSerializer(programs, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'],
            permission_classes=[SpecialistOrAdmin])
    def get_client_list(self, serializer):
        """Вывод всех клиентов специалиста"""
        clients = SpecialistClient.objects.filter(
            specialist=self.request.user)
        serializer = ClientListSerializer(clients, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)


class ActivateUser(UserViewSet):
    """Активация пользователя по ссылке в письме"""
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['data'] = {"uid": self.kwargs['uid'],
                          "token": self.kwargs['token']}
        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
