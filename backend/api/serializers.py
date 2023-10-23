from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import status
from rest_framework.serializers import (
    CharField, ChoiceField, DateField, DateTimeField, EmailField, FloatField,
    IntegerField, ModelSerializer, ReadOnlyField, Serializer,
    SerializerMethodField, ValidationError,)

import datetime

from config.settings import GENDER_CHOICES, SPECIALIST_ROLE_CHOICES
from djoser.serializers import UserSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from users.models import (Education, Institution, Params, SpecialistClient,
                          Specialists,)
from workouts.models import Training, TrainingPlan, TrainingPlanTraining

from diets.models import DietPlan, DietPlanDiet, Diets

User = get_user_model()


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
        instance.training.clear()
        trainings = validated_data.pop("training")
        instance = super().update(instance, validated_data)
        return self.add_trainings(trainings, instance)


class DietsSerializer(ModelSerializer):
    """Сериализатор диет"""

    weekday = ChoiceField(choices=settings.WEEKDAY_CHOICES)

    class Meta:
        model = Diets
        fields = (
            "id",
            "weekday",
            "spec_comment",
            "user_comment",
        )


class DietPlanSerializer(ModelSerializer):
    """Сериализатор плана питания"""

    diet = DietsSerializer(many=True, required=False)

    class Meta:
        model = DietPlan
        fields = (
            "id",
            "specialist",
            "user",
            "name",
            "kkal",
            "protein",
            "carbo",
            "fat",
            "describe",
            "diet",
        )

    def add_diets(self, diets, diet_plan):
        for diet in diets:
            current_diet = Diets.objects.create(**diet)
            DietPlanDiet.objects.create(diet=current_diet, diet_plan=diet_plan)
        return diet_plan

    def create(self, validated_data):
        if "diet" not in self.initial_data:
            return DietPlan.objects.create(**validated_data)
        diets = validated_data.pop("diet")
        diet_plan = DietPlan.objects.create(**validated_data)
        return self.add_diets(diets, diet_plan)

    def update(self, instance, validated_data):
        instance.diet.clear()
        diets = validated_data.pop("diet")
        instance = super().update(instance, validated_data)
        return self.add_diets(diets, instance)


class DietPlanLinkSerializer(Serializer):
    """Сериализатор для создания ссылки на план питания"""

    diet_plan_id = IntegerField()
    link = CharField()


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


class DietListSerializer(ModelSerializer):
    """Сериализатор списка программ питания"""

    create_dt = DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = DietPlan
        fields = (
            "id",
            "name",
            "create_dt",
        )

    def get_diet_program(self, obj):
        return DietPlan.objects.filter(user=obj.user).exists()


class ParamsSerializer(ModelSerializer):
    """Сериализатор параметров"""

    weight = FloatField(default=None)
    height = IntegerField(default=None)
    waist_size = IntegerField(default=None)
    created_at = DateTimeField(read_only=True)

    class Meta:
        model = Params
        fields = (
            "id",
            "weight",
            "height",
            "waist_size",
            "created_at",
        )


class InstitutionSerializer(ModelSerializer):
    class Meta:
        model = Institution
        fields = ("name",)


class EducationSerializer(ModelSerializer):
    """Сериализатор образования"""

    institution = InstitutionSerializer(
        required=False, many=True, default=None
    )
    graduate = CharField(required=False, allow_blank=True)
    completion_date = CharField(required=False, allow_blank=True)
    number = CharField(required=False, allow_blank=True)
    capture = Base64ImageField(required=False, default=None)

    class Meta:
        model = Education
        fields = (
            "id",
            "institution",
            "graduate",
            "completion_date",
            "number",
            "capture",
        )


class SpecialistSerializer(ModelSerializer):
    """Сериализатор информации о специалисте"""

    experience = CharField(required=False, allow_blank=True)
    contacts = CharField(required=False, allow_blank=True)
    about = CharField(required=False, allow_blank=True)

    class Meta:
        model = Specialists
        fields = (
            "id",
            "experience",
            "contacts",
            "about",
            "created_at",
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
            "specialist",
            "user",
            "diseases",
            "exp_diets",
            "exp_trainings",
            "bad_habits",
            "notes",
            "food_preferences",
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей"""

    params = ParamsSerializer(
        many=True, required=False, default=None, read_only=True, partial=True
    )
    gender = ChoiceField(
        required=False,
        choices=GENDER_CHOICES,
        default="0",
    )
    role = ChoiceField(
        required=False,
        choices=SPECIALIST_ROLE_CHOICES,
        default="0",
    )
    email = EmailField()
    dob = DateField(required=False, default=None)
    specialist = SpecialistSerializer(
        many=True, required=False, default=None, read_only=True, partial=True
    )
    # when we are ready to work with pictures we'll return the field
    # capture = Base64ImageField(required=False, default=None)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "role",
            "email",
            "phone_number",
            "dob",
            "gender",
            "params",
            "is_specialist",
            "specialist",
        )
        read_only_fields = ("email",)

    @transaction.atomic
    def create(self, validated_data):
        params_data = self.initial_data.get("params")
        specialist_data = self.initial_data.get("specialist")
        instance = super().create(validated_data)
        if params_data:
            Params.objects.bulk_create(
                [
                    Params(
                        weight=params["weight"],
                        height=params["height"],
                        waist_size=params["waist_size"],
                        user_id=instance.id,
                    )
                    for params in params_data
                    if params.get("weight")
                ]
            )
        if specialist_data:
            Specialists.objects.bulk_create(
                [
                    Specialists(
                        experience=specialist["experience"],
                        contacts=specialist["contacts"],
                        about=specialist["about"],
                        user_id=instance.id,
                    )
                    for specialist in specialist_data
                    if specialist.get("experience")
                ]
            )
        instance.save()
        return instance

    def update(self, instance, validated_data, partial=True):
        if self.initial_data.get("params"):
            params_data = self.initial_data.get("params")[0]
            if params_data:
                params_set = instance.params.all()
                params_obj, created = params_set.get_or_create(
                    weight=params_data.get("weight"),
                    height=params_data.get("height"),
                    waist_size=params_data.get("waist_size"),
                    user=instance,
                )
        if self.initial_data.get("specialist"):
            specialist_data = self.initial_data.get("specialist")[0]
            if specialist_data:
                specialist_set = instance.specialist.all()
                specialist_obj, created = specialist_set.get_or_create(
                    experience=specialist_data.get("experience"),
                    contacts=specialist_data.get("contacts"),
                    about=specialist_data.get("about"),
                    user=instance,
                )
        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class ShowUserSerializer(ModelSerializer):
    """Сериализатор для вывода данных пользователя"""

    params = ParamsSerializer(required=False, default=None)
    role = ChoiceField(
        required=False,
        choices=SPECIALIST_ROLE_CHOICES,
        default="0",
    )
    capture = CharField(required=False, default=None)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "role",
            "email",
            "phone_number",
            "dob",
            "gender",
            "params",
            "capture",
        )


class ClientListSerializer(ModelSerializer):
    """Сериализатор вывода списка клиентов специалиста"""

    client_id = ReadOnlyField(source="user.id")
    first_name = ReadOnlyField(source="user.first_name")
    last_name = ReadOnlyField(source="user.last_name")
    age = SerializerMethodField(read_only=True)

    class Meta:
        model = SpecialistClient
        fields = (
            "id",
            "client_id",
            "first_name",
            "last_name",
            "notes",
            "age",
        )

    @extend_schema_field(OpenApiTypes.INT)
    def get_age(self, obj):
        dob = obj.user.dob
        if not dob:
            return "Возраст не указан"
        today = datetime.date.today()
        if (today.month < dob.month) or (
            today.month == dob.month and today.day < dob.day
        ):
            return today.year - dob.year - 1
        return today.year - dob.year


class ClientAddSerializer(ModelSerializer):
    """
    Сериализатор для добавления нового клиента специалистом.

    Для фронтенда нужно было исключить необходимость передачи
    null для незаполненных полей.
    """

    specialist = ReadOnlyField(source="specialist.id")
    user = ShowUserSerializer()

    class Meta:
        model = SpecialistClient
        fields = (
            "user",
            "specialist",
            "diseases",
            "exp_diets",
            "exp_trainings",
            "bad_habits",
            "notes",
            "food_preferences",
        )

    @transaction.atomic
    def create(self, data):
        password = make_password(settings.STD_CLIENT_PASSWORD)
        specialist = data.get("specialist")
        user_data = data.get("user")
        params = user_data.pop("params")
        role = None
        gender = None
        if "role" in user_data:
            role_link = user_data.pop("role")
            if sum(
                [1 for x, y in SPECIALIST_ROLE_CHOICES if x == role_link]
            ) == 0:
                raise ValidationError(
                    (
                        "Пользователь может быть в роли с кодом из списка "
                        "0, 1 или 2 и никак иначе."
                    ),
                    code=status.HTTP_400_BAD_REQUEST,
                )
            role = role_link
        if "gender" in user_data:
            gender_link = user_data.pop("gender")
            if sum([1 for x, y in GENDER_CHOICES if x == gender_link]) == 0:
                raise ValidationError(
                    (
                        "Пользователь может быть мужчиной (2), женщиной (1) "
                        "или его пол может быть не указан (0)."
                    ),
                    code=status.HTTP_400_BAD_REQUEST,
                )
            gender = gender_link
        if params:
            user_params = Params.objects.create(**params)
        else:
            user_params = None
        client, created = User.objects.get_or_create(
            **user_data,
            password=password,
            role=role,
            gender=gender,
            is_specialist=False,
        )
        client.params.add(user_params)
        diseases = data.get("diseases")
        exp_diets = data.get("exp_diets")
        notes = data.get("notes")
        exp_trainings = data.get("exp_trainings")
        bad_habits = data.get("bad_habits")
        food_preferences = data.get("food_preferences")
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

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.diseases = validated_data.get("diseases")
        instance.exp_diets = validated_data.get("exp_diets")
        instance.notes = validated_data.get("notes")
        instance.exp_trainings = validated_data.get("exp_trainings")
        instance.bad_habits = validated_data.get("bad_habits")
        instance.food_preferences = validated_data.get("food_preferences")


class UpdateClientSerializer(ModelSerializer):
    class Meta:
        model = SpecialistClient
        fields = [
            "user",
            "specialist",
            "diseases",
            "exp_diets",
            "exp_trainings",
            "bad_habits",
            "notes",
            "food_preferences",
        ]


class ClientProfileSerializer(ModelSerializer):
    """Сериализатор для карточки клиента"""

    first_name = ReadOnlyField(source="user.first_name")
    last_name = ReadOnlyField(source="user.last_name")
    age = SerializerMethodField()
    phone_number = ReadOnlyField(source="user.phone_number")
    email = ReadOnlyField(source="user.email")
    params = ParamsSerializer(source="user.params")
    trainings = SerializerMethodField(required=False)
    diets = SerializerMethodField(required=False)

    class Meta:
        model = SpecialistClient
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "age",
            "params",
            "diseases",
            "exp_diets",
            "exp_trainings",
            "bad_habits",
            "food_preferences",
            "notes",
            "trainings",
            "diets",
        )

    @extend_schema_field(OpenApiTypes.INT)
    def get_age(self, obj):
        dob = obj.user.dob
        if not dob:
            return "Возраст не указан"
        today = datetime.date.today()
        if (today.month < dob.month) or (
            today.month == dob.month and today.day < dob.day
        ):
            return today.year - dob.year - 1
        return today.year - dob.year

    def get_trainings(self, obj):
        queryset = obj.user.user_training_plan.all()
        return TrainingPlanSerializer(queryset, many=True).data

    def get_diets(self, obj):
        queryset = obj.user.diet_plan_user.all()
        return DietPlanSerializer(queryset, many=True).data
