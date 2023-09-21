from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, validators

from djoser.serializers import UserCreateSerializer, UserSerializer

from config.settings import WEEKDAY_CHOICES
from workouts.models import Training, TrainingPlan, TrainingPlanTraining

from diets.models import DietPlan, DietPlanDiet, Diets

User = get_user_model()


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
    if User.is_specialist:
        specialist = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=serializers.CurrentUserDefault()
        )
    else:
        user = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=serializers.CurrentUserDefault()
        )

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
    weekday = serializers.ChoiceField(choices=WEEKDAY_CHOICES)

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
    if User.is_specialist:
        specialist = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=serializers.CurrentUserDefault()
        )
    else:
        user = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=serializers.CurrentUserDefault()
        )

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


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    email = serializers.EmailField(
        validators=[validators.UniqueValidator(
            queryset=User.objects.all())])

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class UsersSerializer(UserSerializer):
    """Сериализатор пользователей"""
    class Meta:
        model = User
        fields = '__all__'


class UserPasswordSerializer(serializers.Serializer):
    """Сериализатор для изменения пароля"""
    new_password = serializers.CharField(
        label='Новый пароль')
    current_password = serializers.CharField(
        label='Текущий пароль')

    def validate_current_password(self, current_password):
        user = self.context['request'].user
        if not authenticate(
                username=user.email,
                password=current_password):
            raise serializers.ValidationErrorCreateUserSerializer(
                'Ошибка при вводе логина/пароля',
                code='authorization')
        return current_password

    def validate_new_password(self, new_password):
        validators.validate_password(new_password)
        return new_password

    def create(self, validated_data):
        user = self.context['request'].user
        password = make_password(
            validated_data.get('new_password'))
        user.password = password
        user.save()
        return validated_data
