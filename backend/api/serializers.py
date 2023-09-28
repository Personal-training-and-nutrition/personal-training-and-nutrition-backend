from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.serializers import (CharField, ChoiceField, DateField,
                                        DateTimeField, EmailField, Field,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        Serializer, SerializerMethodField,)

from djoser.serializers import UserSerializer
from users.models import Education, Gender, Specialists, Params, Role
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


class EducationSerializer(ModelSerializer):
    class Meta:
        model = Education
        fields = ('institution',
                  'graduate',
                  'completion_date',
                  'number',
                  'capture',
                  'created_at',
                  'updated_at',)


class ParamsSerializer(ModelSerializer):
    class Meta:
        model = Params
        fields = ('weight',
                  'height',
                  )

    def create(self, validated_data):
        return Params.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.height = validated_data.get('height', instance.height)

        instance.save()
        return instance


class SpecialistSerializer(ModelSerializer):
    education = EducationSerializer(many=True)

    class Meta:
        model = Specialists
        fields = ('experience',
                  'education',
                  'contacts',
                  'about',
                  )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        education_data = validated_data.pop('education')

        user = User.objects.create(**user_data, is_specialist=True)
        specialist = Specialists.objects.create(
            user=user, **validated_data)

        for education_item in education_data:
            Education.objects.create(specialist=specialist, **education_item)

        return specialist

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        education_data = validated_data.pop('education')

        user_serializer = self.fields['user']
        user_serializer.update(instance.user, user_data)

        instance.experience = validated_data.get(
            'experience', instance.experience)
        instance.contacts = validated_data.get(
            'contacts', instance.contacts)
        instance.about = validated_data.get(
            'about', instance.about)
        instance.diseases = validated_data.get(
            'diseases', instance.diseases)
        instance.exp_diets = validated_data.get(
            'exp_diets', instance.exp_diets)
        instance.exp_trainings = validated_data.get(
            'exp_trainings', instance.exp_trainings)
        instance.bad_habits = validated_data.get(
            'bad_habits', instance.bad_habits)
        instance.food_preferences = validated_data.get(
            'food_preferences', instance.food_preferences)
        instance.notes = validated_data.get(
            'notes', instance.notes)

        instance.save()

        instance.education.all().delete()
        for education_item in education_data:
            Education.objects.create(specialist=instance, **education_item)

        return instance


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей"""
    params = ParamsSerializer(many=False)
    specialists = SpecialistSerializer(source='specialist')

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # role_data = validated_data.pop('role')
        # gender_data = validated_data.pop('gender')
        params_data = validated_data.pop('params')

        # role, created = Role.objects.get_or_create(**role_data)
        # gender, created = Gender.objects.get_or_create(**gender_data)
        params = Params.objects.create(**params_data)

        return User.objects.create(
            # role=role,
            # gender=gender,
            params=params,
            **validated_data)

    def update(self, instance, validated_data):
        # Обновление связанной модели Params
        params_data = validated_data.pop('params')
        params_serializer = self.fields['params']
        params_instance = instance.params
        params_serializer.update(params_instance, params_data)

        # Обновление связанной модели Specialist
        specialist_data = validated_data.pop('specialists')
        specialist_serializer = self.fields['specialists']
        specialist_instance = instance.specialist
        specialist_serializer.update(specialist_instance, specialist_data)

        # Обновление остальных полей пользователя
        fields = ('first_name',
                  'last_name',
                  'middle_name',
                  'email',
                  'phone_number',
                  'dob',
                  'gender',
                  'capture',
                  'is_active',
                  )
        for field in fields:
            setattr(instance, field, validated_data.get(
                field, getattr(instance, field)))

        instance.save()
        return instance

    def get_diet_program(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return DietPlan.objects.filter(user=user, author=obj).exists()
        return False
