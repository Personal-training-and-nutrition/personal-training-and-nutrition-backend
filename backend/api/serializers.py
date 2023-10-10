from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import (CharField, ChoiceField, DateField,
                                        DateTimeField, IntegerField,
                                        ModelSerializer, ReadOnlyField,
                                        Serializer, SerializerMethodField,)

import datetime

from users.models import (Gender, Params, Role, SpecialistClient, Specialists,
                          User,)
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


class DietPlanLinkSerializer(Serializer):
    diet_plan_id = IntegerField()
    link = CharField()


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


class ClientListSerializer(ModelSerializer):
    first_name = ReadOnlyField(source='user.first_name')
    last_name = ReadOnlyField(source='user.last_name')
    age = SerializerMethodField(read_only=True)
    notes = CharField()

    class Meta:
        model = SpecialistClient
        fields = (
            'id',
            'first_name',
            'last_name',
            'notes',
            'age',
        )

    def get_age(self, obj):
        if not obj.user.dob:
            return 'Возвраст не указан'
        today = datetime.date.today()
        return today.year - obj.user.dob.year


class ParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Params
        fields = ['id', 'weight', 'height', 'waist_size']


class SpecialistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialists
        fields = (
            'id',
            'experience',
            'contacts',
            'about',
        )


class UserSerializer(serializers.ModelSerializer):
    params = ParamsSerializer(many=True, read_only=True)
    specialist = SpecialistsSerializer(many=True, read_only=True)
    gender = ChoiceField(
        read_only=True,
        required=False,
        choices=Gender.GENDER_CHOICES,
    )
    role = ChoiceField(
        required=False,
        read_only=True,
        choices=Role.SPECIALIST_ROLE_CHOICES,
    )
    dob = DateField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'password',
            'role',
            'email',
            'phone_number',
            'dob',
            'gender',
            'params',
            'capture',
            'is_specialist',
            'specialist',
        )
        read_only_fields = ('email',)

    @transaction.atomic
    def create(self, validated_data):
        params_data = self.initial_data.get('params')
        instance = super().create(validated_data)
        if params_data:
            Params.objects.bulk_create([
                Params(
                    weight=params['weight'],
                    height=params['height'],
                    waist_size=params['waist_size'],
                    user_id=instance.id
                ) for params in params_data if params.get('name')
            ])
        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        params_data = self.initial_data.get('params')
        if params_data:
            instance.params.clear()
            for params in params_data:
                params_id = params.get("id")
                if params_id:
                    params_obj = Params.objects.get(id=params_id)
                    params_obj.weight = params.get("weight")
                    params_obj.height = params.get("height")
                    params_obj.waist_size = params.get("waist_size")
                    params_obj.save()
                    instance.params.add(params_obj)
                else:
                    Params.objects.create(
                        weight=params['weight'],
                        height=params['height'],
                        waist_size=params['waist_size'],
                        user_id=instance.id
                    )

        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class ClientAddSerializer(ModelSerializer):
    user = UserSerializer()
    specialist = ReadOnlyField(source='specialist.id')

    class Meta:
        model = SpecialistClient
        fields = (
            'specialist',
            'user',
            'diseases',
            'exp_diets',
            'exp_trainings',
            'bad_habits',
            'notes',
            'food_preferences')
        succ_messages = {"username": {"required": "Give yourself a username"}}

    @transaction.atomic
    def create(self, data):
        password = make_password(settings.STD_CLIENT_PASSWORD)
        specialist = data.pop('specialist')
        user = data.pop('user')
        user_params = Params.objects.create(
            weight=user['params']['weight'],
            height=user['params']['height'],
            waist_size=user['params']['waist_size'],
        )
        user_gender = Gender.objects.get(id=user['gender'])
        client = User.objects.create(
            first_name=user['first_name'],
            last_name=user['last_name'],
            middle_name=user['middle_name'],
            password=password,
            email=user['email'],
            phone_number=user['phone_number'],
            dob=user['dob'],
            params=user_params,
            gender=user_gender,
            is_specialist=False,
        )
        diseases = data.pop('diseases')
        exp_diets = data.pop('exp_diets')
        notes = data.pop('notes')
        exp_trainings = data.pop('exp_trainings')
        bad_habits = data.pop('bad_habits')
        food_preferences = data.pop('food_preferences')
        return SpecialistClient.objects.create(
            user=client,
            specialist=specialist,
            diseases=diseases,
            exp_diets=exp_diets,
            notes=notes,
            exp_trainings=exp_trainings,
            bad_habits=bad_habits,
            food_preferences=food_preferences,
        )
