from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import (CharField, ChoiceField, DateField,
                                        DateTimeField, FloatField,
                                        IntegerField, ModelSerializer,
                                        ReadOnlyField, SerializerMethodField,)

import datetime

from djoser.serializers import UserSerializer
from users.models import GENDER_CHOICES, Gender, Params, SpecialistClient
from workouts.models import Training, TrainingPlan, TrainingPlanTraining

from diets.models import DietPlan, DietPlanDiet, Diets

User = get_user_model()


class TrainingSerializer(ModelSerializer):
    """Сериализатор тренировок"""
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
    """Сериализатор плана тренировок"""
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


class DietsSerializer(ModelSerializer):
    """Сериализатор диет"""
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
    """Сериализатор плана питания"""
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


class DietPlanLinkSerializer(serializers.Serializer):
    diet_plan_id = serializers.IntegerField()
    link = serializers.CharField()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей"""
    class Meta:
        model = User
        fields = '__all__'

    def get_diet_program(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return DietPlan.objects.filter(user=user, author=obj).exists()
        return False


class WorkoutListSerializer(ModelSerializer):
    """Сериализатор списка программ тренировок"""
    create_dt = DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = TrainingPlan
        fields = (
            'id',
            'name',
            'create_dt',
        )

    def get_workout_program(self, obj):
        return TrainingPlan.objects.filter(user=obj.user).exists()


class DietListSerializer(ModelSerializer):
    """Сериализатор списка программ питания"""
    create_dt = DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = DietPlan
        fields = (
            'id',
            'name',
            'create_dt',
        )

    def get_diet_program(self, obj):
        return DietPlan.objects.filter(user=obj.user).exists()


class ParamsSerializer(ModelSerializer):
    weight = FloatField(required=False)
    height = IntegerField(required=False)

    class Meta:
        model = Params
        fields = ('weight', 'height')


class ClientListSerializer(ModelSerializer):
    id = ReadOnlyField(source='user.id')
    first_name = ReadOnlyField(source='user.first_name')
    last_name = ReadOnlyField(source='user.last_name')
    dob = ReadOnlyField(source='user.dob')
    notes = CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'dob',
            'notes',
        )


class SpecialistClientReadSerializer(ModelSerializer):
    first_name = ReadOnlyField(source='user.first_name')
    last_name = ReadOnlyField(source='user.last_name')
    notes = CharField()
    age = SerializerMethodField(read_only=True)

    class Meta:
        model = SpecialistClient
        fields = ('id', 'first_name', 'last_name',
                  'notes', 'age')

    def get_age(self, obj):
        today = datetime.date.today()
        age = (today.year - obj.user.dob.year)
        return age


class UserInfoSerializer(ModelSerializer):
    params = ParamsSerializer(required=False)
    gender = ChoiceField(
        required=False,
        choices=GENDER_CHOICES
    )
    age = SerializerMethodField(read_only=True)
    dob = DateField(write_only=True,
                    required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email',
                  'phone_number', 'dob', 'params', 'gender', 'age')

    def get_age(self, obj):
        today = datetime.date.today()
        age = (today.year - obj.dob.year)
        return age


class SpecialistAddClientSerializer(ModelSerializer):
    user = UserInfoSerializer(required=False)

    class Meta:
        model = SpecialistClient
        fields = ('id', 'user', 'diseases',
                  'exp_diets', 'exp_trainings',
                  'bad_habits', 'notes',
                  'food_preferences')

    def create(self, data):
        specialist = data.pop('specialist')
        user = data.pop('user')
        user_params = Params.objects.create(
            weight=user['params']['weight'],
            height=user['params']['height']
        )
        user_gender = Gender.objects.get(
            gender=user["gender"]
        )
        client = User.objects.create(
            email=user['email'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            middle_name=user['middle_name'],
            phone_number=user['phone_number'],
            dob=user['dob'],
            params=user_params,
            gender=user_gender
        )
        diseases = data.pop('diseases')
        exp_diets = data.pop('exp_diets')
        notes = data.pop('notes')
        exp_trainings = data.pop('exp_trainings')
        bad_habits = data.pop('bad_habits')
        food_preferences = data.pop('food_preferences')
        specialist_client = SpecialistClient.objects.create(
            user=client,
            specialist=specialist,
            diseases=diseases,
            exp_diets=exp_diets,
            notes=notes,
            exp_trainings=exp_trainings,
            bad_habits=bad_habits,
            food_preferences=food_preferences
        )
        return specialist_client

    # def update(self, instance, validated_data):
    #     instance.diseases = validated_data.get(
    #         'diseases', instance.diseases)
    #     instance.exp_diets = validated_data.get(
    #         'exp_diets', instance.exp_diets)
    #     instance.notes = validated_data.get(
    #         'notes', instance.notes)
    #     instance.diseases = validated_data.get(
    #         'exp_trainings', instance.exp_trainings)
    #     instance.diseases = validated_data.get(
    #         'bad_habits', instance.bad_habits)
    #     instance.diseases = validated_data.get(
    #         'food_preferences', instance.food_preferences)
    #     instance.save()
    #     return instance
