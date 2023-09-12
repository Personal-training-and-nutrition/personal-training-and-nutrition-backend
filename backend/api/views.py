from django.contrib.auth import get_user_model
from rest_framework import viewsets

from workouts.models import TrainingPlan

from .serializers import TrainingPlanSerializer

User = get_user_model()


class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSerializer
    queryset = TrainingPlan.objects.all()
