from django.conf import settings
from rest_framework.fields import ChoiceField, DateTimeField
from rest_framework.serializers import ModelSerializer

from workouts.models import Training, TrainingPlan, TrainingPlanTraining


class TrainingSerializer(ModelSerializer):
    """Сериализатор тренировок"""

    weekday = ChoiceField(choices=settings.WEEKDAY_CHOICES)

    class Meta:
        model = Training
        fields = (
            "id",
            "weekday",
            "spec_comment",
            "user_comment",
        )


class TrainingPlanSerializer(ModelSerializer):
    """Сериализатор плана тренировок"""

    training = TrainingSerializer(many=True, required=False)

    class Meta:
        model = TrainingPlan
        fields = (
            "id",
            "specialist",
            "user",
            "name",
            "describe",
            "training",
        )

    def add_trainings(self, trainings, training_plan):
        for training in trainings:
            current_training = Training.objects.create(**training)
            TrainingPlanTraining.objects.create(
                training=current_training, training_plan=training_plan
            )
        return training_plan

    def create(self, validated_data):
        if "training" not in self.initial_data:
            return TrainingPlan.objects.create(**validated_data)
        trainings = validated_data.pop("training")
        training_plan = TrainingPlan.objects.create(**validated_data)
        return self.add_trainings(trainings, training_plan)

    def update(self, instance, validated_data):
        if validated_data.get("training") is None:
            return super().update(instance, validated_data)
        instance.training.clear()
        trainings = validated_data.pop("training")
        instance = super().update(instance, validated_data)
        return self.add_trainings(trainings, instance)


class WorkoutListSerializer(ModelSerializer):
    """Сериализатор списка программ тренировок"""

    create_dt = DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = TrainingPlan
        fields = (
            "id",
            "name",
            "create_dt",
        )

    def get_workout_program(self, obj):
        return TrainingPlan.objects.filter(user=obj.user).exists()
