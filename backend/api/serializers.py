from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework.serializers import (CharField, ChoiceField, DateField,
                                        DateTimeField, FloatField,
                                        IntegerField, ModelSerializer,
                                        ReadOnlyField, Serializer,
                                        SerializerMethodField)

import datetime

from djoser.serializers import UserSerializer
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


class ParamsSerializer(ModelSerializer):
    weight = FloatField(required=False)
    height = IntegerField(required=False)
    waist_size = IntegerField(required=False)

    class Meta:
        model = Params
        fields = (
            'weight',
            'height',
            'waist_size',
        )

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.height = validated_data.get('height', instance.height)
        instance.waist_size = validated_data.get('waist_size', instance.waist_size)
        instance.save()


class SpecialistSerializer(ModelSerializer):
    experience = CharField(required=False)
    education = CharField(required=False)
    contacts = CharField(required=False)
    about = CharField(required=False)

    class Meta:
        model = Specialists
        fields = (
            'experience',
            'education',
            'contacts',
            'about',
        )

    def update(self, instance, validated_data):
        instance.experience = validated_data.get('experience', instance.experience)
        instance.education = validated_data.get('education', instance.education)
        instance.contacts = validated_data.get('contacts', instance.contacts)
        instance.about = validated_data.get('about', instance.about)
        instance.save()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей"""
    params = ParamsSerializer(required=False)
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
    specialist = SpecialistSerializer(required=False)

    class Meta:
        model = User
        fields = (
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
        params_data = validated_data.pop('params')
        specialist_data = validated_data.pop('specialist')
        user = User.objects.create(**validated_data)
        for data in params_data:
            Params.objects.create(user=user, **data)
        for data in specialist_data:
            Specialists.objects.create(id=id, **data)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.middle_name = validated_data.get(
            'middle_name', instance.middle_name)
        instance.password = validated_data.get(
            'password', instance.password)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.dob = validated_data.get('dob', instance.dob)

        params_data = validated_data.pop('params')
        super(self.__class__, self).update(instance, validated_data)
        super(ParamsSerializer, ParamsSerializer()).update(
            instance.params, params_data)
        
        # spec_data = validated_data.pop('specialist')
        # super(self.__class__, self).update(instance, validated_data)
        # super(SpecialistSerializer, SpecialistSerializer()).update(
        #     instance.specialist, spec_data)

        instance.save()
        return instance


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


class ClientAddSerializer(ModelSerializer):
    user = CustomUserSerializer()
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
