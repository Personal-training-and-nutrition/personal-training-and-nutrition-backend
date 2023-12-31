from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.filters import DietPlanFilter, TrainingPlanFilter
from djoser.conf import settings
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema
from users.models import SpecialistClient
from workouts.models import TrainingPlan

from diets.models import DietPlan

from .permissions import (ClientOrAdmin, IsCurUserOrTheirSpecialistPermission,
                          SpecialistOrAdmin,)
from .serializers import (ClientAddSerializer, ClientListSerializer,
                          ClientProfileSerializer, CustomUserSerializer,
                          DietListSerializer, DietPlanLinkSerializer,
                          DietPlanSerializer, TrainingPlanSerializer,
                          UpdateClientSerializer, WorkoutListSerializer,)

User = get_user_model()


class TrainingPlanViewSet(viewsets.ModelViewSet):
    """Функции для работы с планами тренировок"""

    serializer_class = TrainingPlanSerializer
    queryset = TrainingPlan.objects.all()
    permission_classes = [IsCurUserOrTheirSpecialistPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TrainingPlanFilter
    http_method_names = ["get", "post", "put", "delete"]


class DietPlanViewSet(viewsets.ModelViewSet):
    """Функции для работы с планами питания"""

    serializer_class = DietPlanSerializer
    queryset = DietPlan.objects.all()
    permission_classes = [IsCurUserOrTheirSpecialistPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DietPlanFilter
    http_method_names = ["get", "post", "put", "delete"]

    @action(detail=True, methods=["post"])
    def send_link(self, request, pk=None):
        """Генерация ссылки и отправка плана питания."""
        diet_plan = self.get_object()
        link = "http://127.0.0.1:8000/api/diet-plans/{0}".format(diet_plan.pk)
        # В этой части нужно реализовать логику отправки, например,
        # отправку письма или сообщения
        serializer = DietPlanLinkSerializer(
            data={"diet_plan_id": diet_plan.pk, "link": link}
        )
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(UserViewSet):
    """Функции для работы с пользователями"""

    serializer_class = CustomUserSerializer
    permission_classes = settings.PERMISSIONS.user

    def get_queryset(self):
        return User.objects.all()

    def destroy(self, request, *args, **kwargs):
        """Вместо удаления меняется флаг is_active"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=False)
        # if instance == request.user:
        #     utils.logout_user(self.request)
        request.user.is_active = False
        request.user.save()
        return Response(
            f'Пользователь {request.data["email"]}удалён.',
            status=status.HTTP_200_OK
        )

    @action(["post"], detail=False, permission_classes=(AllowAny,))
    def user_restore(self, request, *args, **kwargs):
        """Восстановление пользователя (меняется флаг is_active)"""
        user = get_object_or_404(User, email=request.data["email"])
        if user.check_password(request.data["password"]):
            User.objects.activate_user(user)
            return Response(
                f'Пользователь {request.data["email"]} ' f"восстановлен.",
                status=status.HTTP_200_OK,
            )
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
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[ClientOrAdmin])
    def get_workout_programs(self, serializer):
        """Вывод программ тренировок клиента"""
        programs = TrainingPlan.objects.filter(user=self.request.user)
        serializer = WorkoutListSerializer(programs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[ClientOrAdmin])
    def get_diet_programs(self, serializer):
        """Вывод программ питания клиента"""
        programs = DietPlan.objects.filter(user=self.request.user)
        serializer = DietListSerializer(programs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ActivateUser(UserViewSet):
    """Активация пользователя по ссылке в письме"""

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        kwargs["data"] = {
            "uid": self.kwargs["uid"],
            "token": self.kwargs["token"]
        }
        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)


class ClientsViewSet(viewsets.ModelViewSet):
    """Функции для работы с клиентами"""

    permission_classes = (SpecialistOrAdmin,)

    def perform_create(self, serializer):
        return serializer.save(specialist=self.request.user)

    def get_serializer_class(self):
        """Список клиентов специалиста и создание нового клиента"""
        if self.action == "list":
            return ClientListSerializer
        if self.action == "partial_update":
            return UpdateClientSerializer
        return ClientAddSerializer

    @extend_schema(
        responses={
            200: ClientProfileSerializer,
        },
    )
    def retrieve(self, request, pk=None):
        """Получения карточки клиента"""
        user = get_object_or_404(
            SpecialistClient, id=pk, specialist=request.user
        )
        serializer = ClientProfileSerializer(
            user, context={"request": request}
        )
        profile_data = serializer.data
        return Response(profile_data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        return SpecialistClient.objects.filter(specialist=user)
