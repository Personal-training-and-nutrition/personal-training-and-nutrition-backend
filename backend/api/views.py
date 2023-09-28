from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from djoser import utils
from djoser.conf import settings
from djoser.views import UserViewSet
from users.models import SpecialistClient
from workouts.models import TrainingPlan

from diets.models import DietPlan

from .permissions import ClientOrAdmin, SpecialistOrAdmin
from .serializers import (ClientListSerializer, CustomUserSerializer, DietListSerializer,
                          DietPlanSerializer, TrainingPlanSerializer,
                          WorkoutListSerializer, SpecialistSerializer)

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


class CustomUserViewSet(UserViewSet):
    # permission_classes = settings.PERMISSIONS.user
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'pk'

    @action(detail=True, methods=['get', 'put'])
    def profile(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user.specialist)
        profile_data = serializer.data
        return Response(profile_data)

    def destroy(self, request, *args, **kwargs):
        """Вместо удаления меняется флаг is_active"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        if instance == request.user:
            utils.logout_user(self.request)
        request.user.is_active = False
        request.user.save()
        messages.success(request, 'Профиль отключён')
        return Response(status=status.HTTP_204_NO_CONTENT)

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
