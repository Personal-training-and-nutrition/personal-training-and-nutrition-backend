from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import TrainingPlanSerializer
from workouts.models import TrainingPlan

User = get_user_model()


class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSerializer
    queryset = TrainingPlan.objects.all()
