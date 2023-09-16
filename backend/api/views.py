from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from workouts.models import TrainingPlan

from .serializers import TrainingPlanSerializer


User = get_user_model()


class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSerializer
    queryset = TrainingPlan.objects.all()
    permission_classes = (AllowAny,)

    # def perform_create(self, serializer):
    #     serializer.save(specialist=self.request.user)

