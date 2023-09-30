from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from djoser import utils
from djoser.conf import settings
from djoser.views import UserViewSet
from users.models import (Education, Institution, Params, SpecialistClient,
                          Specialists,)
from workouts.models import TrainingPlan

from diets.models import DietPlan

from .serializers import (CustomUserSerializer, ClientSerializer,
                          DietPlanSerializer, SpecialistSerializer,
                          TrainingPlanSerializer,)

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
    permission_classes = settings.PERMISSIONS.user
    serializer_class = CustomUserSerializer
    lookup_field = 'pk'

    @action(detail=True, methods=['get', 'put'])
    def client_profile(self, request, pk=None):
        client = get_object_or_404(User, pk=pk)
        if request.method == 'GET':
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        if request.method == 'PUT':
            serializer = ClientSerializer(client, data=request.data)
            if serializer.is_valid():
                client.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    @action(detail=True, methods=['get', 'put'])
    def specialist_profile(self, request, pk=None):
        specialist = get_object_or_404(Specialists, pk=pk)
        if request.method == 'GET':
            serializer = SpecialistSerializer(specialist)
            return Response(serializer.data)
        if request.method == 'PUT':
            serializer = SpecialistSerializer(specialist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        """Вместо удаления меняем флаг is_active"""
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        if settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['data'] = {"uid": self.kwargs['uid'],
                          "token": self.kwargs['token']}
        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
