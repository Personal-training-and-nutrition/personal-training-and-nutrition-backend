from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from workouts.models import TrainingPlan
from workouts.serializers import TrainingPlanSerializer


class TrainingPlanViewSet(viewsets.ModelViewSet):
    """Функции для работы с планами тренировок"""
    serializer_class = TrainingPlanSerializer
    queryset = TrainingPlan.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']
