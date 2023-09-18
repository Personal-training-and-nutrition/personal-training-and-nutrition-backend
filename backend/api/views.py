from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from djoser.views import UserViewSet
from users.models import User
from workouts.models import TrainingPlan

from diets.models import DietPlan

from .serializers import (DietPlanSerializer, TrainingPlanSerializer,
                          UserPasswordSerializer, UsersSerializer,)


class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSerializer
    queryset = TrainingPlan.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'put', 'delete']


class DietPlanViewSet(viewsets.ModelViewSet):
    serializer_class = DietPlanSerializer
    queryset = DietPlan.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'put', 'delete']


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (AllowAny,)


class SetPasswordView(APIView):
    def post(self, request):
        """Изменить пароль."""
        serializer = UserPasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Пароль изменен!'},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'error': 'Ошибка при вводе данных!'},
            status=status.HTTP_400_BAD_REQUEST,
        )
