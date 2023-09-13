from django.contrib.auth import get_user_model
from rest_framework import serializers

from workouts.models import Training, TrainingPlan

User = get_user_model()

WEEKDAY_CHOICES = (
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
    )


class TrainingPlanSerializer(serializers.ModelSerializer):
    trainings = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = TrainingPlan
        fields = (
            'id',
            'specialist',
            'user',
            'name',
            'describe',
            'trainings'
        )


class TrainingSerializer(serializers.ModelSerializer):
    weekday = serializers.ChoiceField(choices=WEEKDAY_CHOICES)

    class Meta:
        model = Training
        fields = (
            'weekday',
            'spec_comment',
            'user_comment',
            'training_plan'
        )
