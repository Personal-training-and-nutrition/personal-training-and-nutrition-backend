from django.contrib.auth import get_user_model
from rest_framework import serializers

from workouts.models import Training, TrainingPlan, TrainingPlanTraining

User = get_user_model()

WEEKDAY_CHOICES = ('1',
                   '2',
                   '3',
                   '4',
                   '5',
                   '6',
                   '7',
                   )


class TrainingSerializer(serializers.ModelSerializer):
    weekday = serializers.ChoiceField(choices=WEEKDAY_CHOICES)

    class Meta:
        model = Training
        fields = (
            'id',
            'weekday',
            'spec_comment',
            'user_comment',
        )


class TrainingPlanSerializer(serializers.ModelSerializer):
    training = TrainingSerializer(many=True, required=False)
    specialist = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = TrainingPlan
        fields = (
            'id',
            'specialist',
            'user',
            'name',
            'describe',
            'training'
        )
        read_only_fields = ('specialist',)

    def add_trainings(self, trainings, training_plan):
        for training in trainings:
            current_training, status = Training.objects.get_or_create(
                **training)
            TrainingPlanTraining.objects.create(
                training=current_training, training_plan=training_plan)
        return training_plan

    def create(self, validated_data):
        if 'training' not in self.initial_data:
            return TrainingPlan.objects.create(**validated_data)
        trainings = validated_data.pop('training')
        training_plan = TrainingPlan.objects.create(**validated_data)
        return self.add_trainings(trainings, training_plan)

    def update(self, instance, validated_data):
        instance.training.clear()
        trainings = validated_data.pop('training')
        instance = super().update(instance, validated_data)
        return self.add_trainings(trainings, instance)
