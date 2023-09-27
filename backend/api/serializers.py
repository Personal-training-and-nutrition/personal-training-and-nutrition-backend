from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from djoser.serializers import UserSerializer
from users.models import Params
from workouts.models import Training, TrainingPlan, TrainingPlanTraining

from diets.models import DietPlan, DietPlanDiet, Diets

User = get_user_model()


class TrainingSerializer(serializers.ModelSerializer):
    weekday = serializers.ChoiceField(choices=settings.WEEKDAY_CHOICES)

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

    class Meta:
        model = TrainingPlan
        fields = (
            'id',
            'specialist',
            'user',
            'name',
            'describe',
            'training',
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


class DietsSerializer(serializers.ModelSerializer):
    weekday = serializers.ChoiceField(choices=settings.WEEKDAY_CHOICES)

    class Meta:
        model = Diets
        fields = (
            'id',
            'weekday',
            'spec_comment',
            'user_comment',
        )


class DietPlanSerializer(serializers.ModelSerializer):
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


class ParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Params
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей"""
    params = ParamsSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'password',
            'phone_number',
            'date_of_birth',
            'gender',
            'params',
            'capture',
            'is_staff',
            'is_superuser',
            'is_specialist',
            'specialist',
            'is_active',
        )


class CreateClientSerializer(serializers.ModelSerializer):
    """Сериализатор создания клиента"""

    class Meta:
        model = User
        fields = ('last_name',
                  'first_name',
                  'date_of_birth',
                  'gender',
                  # 'weight',
                  # 'height',
                  'phone_number',
                  'email',)
    # def to_representation(self, instance):
    #     return {
    #         'first_name': instance.first_name,
    #         'last_name': instance.last_name,
    #     }

        # exclude = ('is_active',
        #            'is_specialist',
        #            'role',
        #            'gender',
        #            'params',)
