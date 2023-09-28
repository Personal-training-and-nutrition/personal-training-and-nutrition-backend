from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.serializers import (CharField, ChoiceField, DateField,
                                        DateTimeField, EmailField, Field,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        Serializer, SerializerMethodField,)

from djoser.serializers import UserSerializer
from users.models import Gender, Specialists
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


class SpecialistSerializer(ModelSerializer):
    """Сериализатор для данных о специалисте"""
    user = CustomUserSerializer
    id = ReadOnlyField(source='user.id')
    last_name = CharField(source='user.last_name')
    first_name = CharField(source='user.first_name')
    date_of_birth = DateField(source='user.dob')
    gender = PrimaryKeyRelatedField(
        source='user.gender', queryset=Gender.objects.all())
    about = SerializerMethodField()
    weight = SerializerMethodField()
    height = SerializerMethodField()
    email = EmailField(source='user.email')
    phone_number = CharField(source='user.phone_number')
    password = CharField(source='user.password')

    def get_about(self, obj):
        specialist = obj.user.specialist if obj.user.specialist and obj.user.specialist.is_specialist else None
        return specialist.about if specialist else None

    def get_weight(self, obj):
        return obj.user.params.weight if obj.user.params else None

    def get_height(self, obj):
        return obj.user.params.height if obj.user.params else None

    class Meta:
        model = Specialists
        fields = ('user',
                  'id',
                  'last_name',
                  'first_name',
                  'date_of_birth',
                  'gender',
                  'about',
                  'weight',
                  'height',
                  'email',
                  'phone_number',
                  'password',
                  )
