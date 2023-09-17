from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from workouts.models import TrainingPlan

from .serializers import TrainingPlanSpecSerializer

User = get_user_model()


class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSpecSerializer
    queryset = TrainingPlan.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'put', 'delete']
