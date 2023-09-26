from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from djoser import utils
from djoser.conf import settings
from djoser.views import UserViewSet
from users.models import SpecialistClient, Specialists
from workouts.models import TrainingPlan

from diets.models import DietPlan

from .serializers import (CreateClientSerializer, DietPlanSerializer,
                          TrainingPlanSerializer, CustomUserSerializer)

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


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = settings.PERMISSIONS.user
    permission_classes = (AllowAny,)

    # def update(self, request, pk=None):
    #     user = self.get_object()

    #     # Переключение в режим специалиста
    #     if request.data.get('is_specialist'):
    #         user.is_specialist = True
    #         user.save()
    #         return Response({'detail': 'Режим специалиста включен'})
    #     return super().update(request, pk)

    # @action(detail=True, methods=['post'])
    # def become_specialist(self, request, pk=None):
    #     """Пользователь хочет стать тренером"""
    #     user = self.get_object()
    #     user.is_specialist = True
    #     specialist = Specialists.objects.create()
    #     user.specialist = specialist
    #     user.save()
    #     return Response({'status': 'Стал специалистом'})

    # @action(detail=False, methods=['post'])
    # def create_client(self, request, pk=None):
    #     """Специалист создает клиента"""
    #     specialist = self.get_object()
    #     if not specialist.is_specialist:
    #         return Response(
    #             {'error': 'Вы не специалист.'}, status.HTTP_400_BAD_REQUEST)
    #     client_data = request.data
    #     # создание нового пользователя
    #     client = User.objects.create(**client_data)
    #     # создание связи между клиентом и специалистом
    #     SpecialistClient.objects.create(user=client, specialist=specialist)
    #     return Response({'status': 'Клиент создан.'})

    # def specialist_clients(self, request):
    #     """Получение клиентов текущего специалиста"""
    #     specialist = request.user
    #     clients = SpecialistClient.objects.filter(specialist=specialist)
    #     page = self.paginate_queryset(clients)
    #     serializer = SpecialistClient(page, many=True)
    #     return self.get_paginated_response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     """Получение планов питания и тренеровок"""
    #     queryset = User.objects.prefetch_related(
    #         'diet_plans', 'training_plans')
    #     user = get_object_or_404(queryset, pk=pk)
    #     self.check_object_permissions(self.request, user)
    #     serializer = self.get_serializer(user)

    #     return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         """Вместо удаления меняем флаг is_active"""
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if instance == request.user:
#             utils.logout_user(self.request)
#         request.user.is_active = False
#         request.user.save()
#         messages.success(request, 'Профиль отключён')
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(["post"], detail=False)
#     def set_password(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.request.user.set_password(serializer.data["new_password"])
#         self.request.user.save()
#         if settings.CREATE_SESSION_ON_LOGIN:
#             update_session_auth_hash(self.request, self.request.user)
#         return Response(status=status.HTTP_204_NO_CONTENT)


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


# class SubscribeViewSet(viewsets.ModelViewSet):
#     queryset = SpecialistClient.objects.all()
#     serializer_class = CreateClientSerializer

#     def create(self, request):
#         """Подписка клиента на специалиста"""
#         specialist_id = request.data.get('specialist_id')
#         user_id = request.data.get('user_id')

#         # Проверка наличия требуемых данных
#         if not user_id or not specialist_id:
#             return Response({
#                 'error': 'Не указаны данные пользователя или специалиста'},
#                 status=status.HTTP_400_BAD_REQUEST)

#         # Проверка, что специалист существует и активен
#         try:
#             specialist = User.objects.get(
#                 id=specialist_id, is_specialist=True, is_active=True)
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'Специалист не найден или неактивен'},
#                 status=status.HTTP_404_NOT_FOUND)

#         # Создание связи между клиентом и специалистом
#         specialist_client = SpecialistClient.objects.filter(
#             user_id=user_id, specialist=specialist).first()
#         if specialist_client:
#             return Response({'error': 'Подписка уже существует'},
#                             status=status.HTTP_400_BAD_REQUEST)

#         specialist_client = SpecialistClient.objects.create(
#             user_id=user_id, specialist=specialist)

#         # Дополнительная логика, если необходимо

#         return Response(
#             {'message': 'Подписка успешно создана'},
#             status=status.HTTP_201_CREATED)
