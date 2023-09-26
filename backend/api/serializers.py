from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.serializers import (ChoiceField, Field,
                                        ReadOnlyField,
                                        ModelSerializer)

from djoser.serializers import UserSerializer
from workouts.models import Training, TrainingPlan, TrainingPlanTraining

from diets.models import DietPlan, DietPlanDiet, Diets

User = get_user_model()


class TrainingSerializer(ModelSerializer):
    weekday = ChoiceField(choices=settings.WEEKDAY_CHOICES)

    class Meta:
        model = Training
        fields = (
            'id',
            'weekday',
            'spec_comment',
            'user_comment',
        )


class TrainingPlanSerializer(ModelSerializer):
    training = TrainingSerializer(many=True, required=False)

    class Meta:
        model = TrainingPlan
        fields = (
            'id',
            'specialist',
            'user',
            'name',
            'describe',
            'training',
            'create_dt',
        )

    def add_trainings(self, trainings, training_plan):
        for training in trainings:
            current_training = Training.objects.create(
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


class DietsSerializer(ModelSerializer):
    weekday = ChoiceField(choices=settings.WEEKDAY_CHOICES)

    class Meta:
        model = Diets
        fields = (
            'id',
            'weekday',
            'spec_comment',
            'user_comment',
        )


class DietPlanSerializer(ModelSerializer):
    diet = DietsSerializer(many=True, required=False)

    class Meta:
        model = DietPlan
        fields = (
            'id',
            'specialist',
            'user',
            'name',
            'kkal',
            'protein',
            'carbo',
            'fat',
            'describe',
            'diet',
            'create_dt',
        )

    def add_diets(self, diets, diet_plan):
        for diet in diets:
            current_diet = Diets.objects.create(
                **diet)
            DietPlanDiet.objects.create(
                diet=current_diet, diet_plan=diet_plan)
        return diet_plan

    def create(self, validated_data):
        if 'diet' not in self.initial_data:
            return DietPlan.objects.create(**validated_data)
        diets = validated_data.pop('diet')
        diet_plan = DietPlan.objects.create(**validated_data)
        return self.add_diets(diets, diet_plan)

    def update(self, instance, validated_data):
        instance.diet.clear()
        diets = validated_data.pop('diet')
        instance = super().update(instance, validated_data)
        return self.add_diets(diets, instance)


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей"""
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'password',
            'role',
            'phone_number',
            'dob',
            'gender',
            'params',
            'capture',
            'is_staff',
            'is_superuser',
            'is_specialist',
            'specialist',
            'is_active',
        )


class TrainingProgramUserField(Field):
    """Сериализатор для вывода программ тренировок клиента"""
    def get_attribute(self, instance):
        return TrainingPlan.objects.filter(user=instance.user)

    def to_representation(self, workout_list):
        workout_data = []
        for workout in workout_list:
            workout_data.append(
                {
                    "id": workout.id,
                    "name": workout.name,
                    "create_dt": workout.create_dt,
                }
            )
        return workout_data


class WorkoutListSerializer(ModelSerializer):
    workout = TrainingProgramUserField()

    class Meta:
        model = TrainingPlan
        fields = (
            'id',
            'name',
            'create_dt',
        )
    
    def get_workout_program(self, obj):
        return TrainingPlan.objects.filter(user=obj.user).exists()


class DietProgramUserField(Field):
    """Сериализатор для вывода программ питания клиента"""
    def get_attribute(self, instance):
        return DietPlan.objects.filter(user=instance.user)

    def to_representation(self, diet_list):
        diet_data = []
        for diet in diet_list:
            diet_data.append(
                {
                    "id": diet.id,
                    "name": diet.name,
                    "create_dt": diet.create_dt,
                }
            )
        return diet_data


class DietListSerializer(ModelSerializer):
    diet = DietProgramUserField()

    class Meta:
        model = DietPlan
        fields = (
            'id',
            'name',
            'create_dt',
        )

    def get_diet_program(self, obj):
        return DietPlan.objects.filter(user=obj.user).exists()
