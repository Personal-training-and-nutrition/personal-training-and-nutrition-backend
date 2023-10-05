from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework import status, viewsets

# from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from djoser import utils
from djoser.conf import settings
from djoser.views import UserViewSet
from users.models import SpecialistClient, Specialists
from workouts.models import TrainingPlan

from diets.models import DietPlan

from .permissions import ClientOrAdmin, SpecialistOrAdmin
from .serializers import (ClientListSerializer, ClientSerializer,
                          CustomUserSerializer, DietListSerializer,
                          DietPlanLinkSerializer, DietPlanSerializer,
                          SpecialistAddClientSerializer,
                          SpecialistClientReadSerializer, SpecialistSerializer,
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
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'pk'

    # @action(detail=True, methods=['get', 'put'])
    # def client_profile(self, request, pk=None):
    #     client = get_object_or_404(User, pk=pk)
    #     if request.method == 'GET':
    #         serializer = ClientSerializer(client)
    #         return Response(serializer.data)
    #     if request.method == 'PUT':
    #         serializer = ClientSerializer(client, data=request.data)
    #         if serializer.is_valid():
    #             client.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=400)

    # @action(detail=True, methods=['get', 'put'])
    # def specialist_profile(self, request, pk=None):
    #     specialist = get_object_or_404(Specialists, pk=pk)
    #     if request.method == 'GET':
    #         serializer = SpecialistSerializer(specialist)
    #         return Response(serializer.data)
    #     if request.method == 'PUT':
    #         serializer = SpecialistSerializer(specialist, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors, status=400)

    @action(detail=True, methods=['get', 'put'])
    def profile(self, request, pk=None):

        user = self.get_object()

        if user.is_specialist:
            try:
                specialist_profile = user.specialist
                serializer = SpecialistSerializer(specialist_profile)
                profile_data = serializer.data
                return Response(profile_data, status=status.HTTP_200_OK)
            except Specialists.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            client_profile = user.specialist_client_user.first()
            serializer = ClientSerializer(client_profile)
            profile_data = serializer.data
            return Response(profile_data, status=status.HTTP_200_OK)

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


# class SpecialistClientsViewSet(viewsets.ModelViewSet):
#     serializer_class = SpecialistAddClientSerializer
#     queryset = SpecialistClient.objects.all()
#     permission_classes = (SpecialistOrAdmin,)

#     def perform_create(self, serializer):
#         return serializer.save(specialist=self.request.user)

#     def get_serializer_class(self):
#         if self.action in ['list']:
#             return SpecialistClientReadSerializer
#         return SpecialistAddClientSerializer


class SpecialistClientsViewSet(viewsets.ModelViewSet):
    serializer_class = SpecialistAddClientSerializer
    queryset = SpecialistClient.objects.all()
    permission_classes = (SpecialistOrAdmin,)

    def perform_create(self, serializer):
        return serializer.save(specialist=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list']:
            return SpecialistClientReadSerializer
        return SpecialistAddClientSerializer


# class CustomSpecialistViewSet(viewsets.ModelViewSet):
#     permission_classes = settings.PERMISSIONS.user
#     queryset = User.objects.all()
#     serializer_class = CustomUserSerializer
#     lookup_field = 'pk'

#     @action(detail=True, methods=['get', 'put'])
#     def specialist_profile(self, request, pk=None):
#         specialist = get_object_or_404(Specialists, pk=pk)
#         if request.method == 'GET':
#             serializer = SpecialistSerializer(specialist)
#             return Response(serializer.data)
#         if request.method == 'PUT':
#             serializer = SpecialistSerializer(specialist, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             else:
#                 return Response(serializer.errors, status=400)
