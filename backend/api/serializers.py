from django.contrib.auth import get_user_model
from rest_framework import serializers

from workouts.models import TrainingPlan

User = get_user_model()


class TrainingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlan
        fields = (
            'specialist',
            'user',
            'name',
            'training',
            'describe'
        )
