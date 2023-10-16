from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (CharField, ChoiceField, DateField,
                                        DateTimeField, EmailField, FloatField,
                                        IntegerField, ModelSerializer,
                                        ReadOnlyField, Serializer,
                                        SerializerMethodField,)

import datetime

from djoser.serializers import UserSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from users.models import (Education, Gender, Institution, Params, Role,
                          SpecialistClient, Specialists, User,)
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
    """Сериализатор для создания ссылки на план питания"""
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
    """Сериализатор параметров"""
    weight = FloatField(default=None)
    height = IntegerField(default=None)
    waist_size = IntegerField(default=None)

    class Meta:
        model = Params
        fields = (
            'weight',
            'height',
            'waist_size',
        )


class InstitutionSerializer(ModelSerializer):

    class Meta:
        model = Institution
        fields = ('name',)


class EducationSerializer(ModelSerializer):
    """Сериализатор образования"""
    institution = InstitutionSerializer(required=False,
                                        many=True, default=None)
    graduate = CharField(required=False, allow_blank=True)
    completion_date = CharField(required=False, allow_blank=True)
    number = CharField(required=False, allow_blank=True)
    capture = Base64ImageField(required=False, default=None)

    class Meta:
        model = Education
        fields = (
            'id',
            'institution',
            'graduate',
            'completion_date',
            'number',
            'capture',
        )


class SpecialistSerializer(ModelSerializer):
    """Сериализатор информации о специалисте"""
    education = EducationSerializer(many=True, required=False, default=None)
    experience = CharField(required=False, allow_blank=True)
    contacts = CharField(required=False, allow_blank=True)
    about = CharField(required=False, allow_blank=True)

    class Meta:
        model = Specialists
        fields = (
            'id',
            'experience',
            'education',
            'contacts',
            'about',
        )


class SpecialistClientSerializer(ModelSerializer):
    """Сериализатор для сущности SpecialistClient"""
    diseases = CharField(required=False, allow_blank=True)
    exp_diets = CharField(required=False, allow_blank=True)
    exp_trainings = CharField(required=False, allow_blank=True)
    bad_habits = CharField(required=False, allow_blank=True)
    notes = CharField(required=False, allow_blank=True)
    food_preferences = CharField(required=False, allow_blank=True)

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
            'food_preferences',
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей"""
    params = ParamsSerializer(required=False, default=None)
    gender = ChoiceField(
        required=False,
        choices=Gender.GENDER_CHOICES,
        default='0',
    )
    role = ChoiceField(
        required=False,
        choices=Role.SPECIALIST_ROLE_CHOICES,
        default='0',
    )
    email = EmailField()
    dob = DateField(required=False, default=None)
    specialist = SpecialistSerializer(required=False)
    capture = Base64ImageField(required=False, default=None)

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
        params_data = self.initial_data.get('params')
        specialist_data = self.initial_data.get('specialist')
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
        if specialist_data:
            Specialists.objects.bulk_create([
                Specialists(
                    experience=specialist['experience'],
                    contacts=specialist['contacts'],
                    about=specialist['about'],
                    user_id=instance.id
                ) for specialist in specialist_data if specialist.get(
                    'experience')
            ])
        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        params_data = self.initial_data.get('params')
        specialist_data = self.initial_data.get('specialist')
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
        if specialist_data:
            instance.specialist.clear()
            for specialist in specialist_data:
                specialist_id = specialist.get("id")
                if specialist_id:
                    specialist_obj = Specialists.objects.get(id=specialist_id)
                    specialist_obj.experience = specialist.get("experience")
                    specialist_obj.contacts = specialist.get("contacts")
                    specialist_obj.about = specialist.get("about")
                    specialist_obj.save()
                    instance.specialist.add(specialist_obj)
                else:
                    Specialists.objects.create(
                        experience=specialist['experience'],
                        contacts=specialist['contacts'],
                        about=specialist['about'],
                        user_id=instance.id
                    )
        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class ClientListSerializer(ModelSerializer):
    """Сериализатор вывода списка клиентов специалиста"""
    first_name = ReadOnlyField(source='user.first_name')
    last_name = ReadOnlyField(source='user.last_name')
    age = SerializerMethodField(read_only=True)

    class Meta:
        model = SpecialistClient
        fields = (
            'id',
            'first_name',
            'last_name',
            'notes',
            'age',
        )

    @extend_schema_field(OpenApiTypes.INT)
    def get_age(self, obj):
        if not obj.user.dob:
            return 'Возвраст не указан'
        today = datetime.date.today()
        return today.year - obj.user.dob.year


class ClientAddSerializer(ModelSerializer):
    """
    Сериализатор для добавления нового клиента специалистом.

    Для фронтенда нужно было исключить необходимость передачи
    null для незаполненных полей.
    """
    specialist = ReadOnlyField(source='specialist.id')
    first_name = CharField(required=False, allow_blank=True)
    last_name = CharField(required=False, allow_blank=True)
    middle_name = CharField(required=False, allow_blank=True)
    params = ParamsSerializer(required=False, default=None)
    phone_number = CharField(required=False, allow_blank=True)
    gender = ChoiceField(
        required=False,
        choices=Gender.GENDER_CHOICES,
        default='0',
    )
    role = ChoiceField(
        required=False,
        choices=Role.SPECIALIST_ROLE_CHOICES,
        default='0',
    )
    email = EmailField(required=False)
    dob = DateField(required=False)
    capture = Base64ImageField(required=False, default=None)

    class Meta:
        model = SpecialistClient
        fields = (
            'first_name',
            'last_name',
            'middle_name',
            'role',
            'email',
            'phone_number',
            'dob',
            'gender',
            'params',
            'capture',
            'specialist',
            'diseases',
            'exp_diets',
            'exp_trainings',
            'bad_habits',
            'notes',
            'food_preferences')

    @transaction.atomic
    def create(self, data):
        password = make_password(settings.STD_CLIENT_PASSWORD)
        specialist = data.pop('specialist')
        params = data.get('params')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        middle_name = data.get('middle_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        dob = data.get('dob')
        if params:
            user_params = Params.objects.create(**params)
        else:
            user_params = None
        user_gender = Gender.objects.get(id=data.get('gender'))
        client = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            password=password,
            email=email,
            phone_number=phone_number,
            dob=dob,
            params=user_params,
            gender=user_gender,
            is_specialist=False,
            specialist=None,
        )
        diseases = data.get('diseases')
        exp_diets = data.get('exp_diets')
        notes = data.get('notes')
        exp_trainings = data.get('exp_trainings')
        bad_habits = data.get('bad_habits')
        food_preferences = data.get('food_preferences')
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


class ClientProfileSerializer(ModelSerializer):
    """Сериализатор для карточки клиента"""
    first_name = ReadOnlyField(source='user.first_name')
    last_name = ReadOnlyField(source='user.last_name')
    age = SerializerMethodField()
    phone_number = ReadOnlyField(source='user.phone_number')
    email = ReadOnlyField(source='user.email')
    params = ParamsSerializer(source='user.params')
    trainings = SerializerMethodField(required=False)
    diets = SerializerMethodField(required=False)

    class Meta:
        model = SpecialistClient
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'age',
            'params',
            'diseases',
            'exp_diets',
            'exp_trainings',
            'bad_habits',
            'food_preferences',
            'notes',
            'trainings',
            'diets',
        )

    @extend_schema_field(OpenApiTypes.INT)
    def get_age(self, obj):
        if not obj.user.dob:
            return 'Возвраст не указан'
        today = datetime.date.today()
        return today.year - obj.user.dob.year

    def get_trainings(self, obj):
        queryset = obj.user.user_training_plan.all()
        return TrainingPlanSerializer(queryset, many=True).data

    def get_diets(self, obj):
        queryset = obj.user.diet_plan_user.all()
        return DietPlanSerializer(queryset, many=True).data
