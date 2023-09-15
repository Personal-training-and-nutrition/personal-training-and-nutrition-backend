from rest_framework import serializers

from .models import (Education, Gender, Institution, Params, Role, Specialists,
                     User,)


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = 'gender'


class ParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Params
        fields = ('weight',
                  'height',
                  'waist_size',
                  'created_at',
                  'updated_at',)

    def create(self, validated_data):
        return Params.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.height = validated_data.get('height', instance.height)
        instance.waist_size = validated_data.get('waist_size',
                                                 instance.waist_size)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = 'role'

    def create(self, validated_data):
        return Role.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('institution',
                  'graduate',
                  'completion_date',
                  'number',
                  'capture',
                  'created_at',
                  'updated_at',)

    def create(self, validated_data):
        return Education.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.institution = validated_data.get(
            'institution', instance.institution)
        instance.graduate = validated_data.get('graduate', instance.graduate)
        instance.completion_date = validated_data.get(
            'completion_date', instance.completion_date)
        instance.number = validated_data.get('number', instance.number)
        instance.capture = validated_data.get('capture', instance.capture)
        instance.save()
        return instance


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ('name',
                  'created_at',
                  'updated_at')

    def create(self, validated_data):
        return Institution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    gender = GenderSerializer()
    params = ParamsSerializer()

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'middle_name',
                  'role',
                  'email',
                  'phone_number',
                  'date_of_birth',
                  'gender',
                  'params',
                  'about',
                  'is_specialist',
                  'is_active',)

    def validate(self, data):
        if not data.get('email'):
            raise serializers.ValidationError("Требуется электронная почта!")
        if not data.get('phone_number'):
            raise serializers.ValidationError("Требуется номер телефона!")
        return data

    def create(self, validated_data):
        role_data = validated_data.pop('role')
        gender_data = validated_data.pop('gender')
        params_data = validated_data.pop('params')

        role, created = Role.objects.get_or_create(**role_data)
        gender, created = Gender.objects.get_or_create(**gender_data)
        params = Params.objects.create(**params_data)

        return User.objects.create(role=role,
                                   gender=gender,
                                   params=params,
                                   **validated_data)

    def update(self, instance, validated_data):
        role_data = validated_data.pop('role')
        gender_data = validated_data.pop('gender')
        params_data = validated_data.pop('params')

        role, created = Role.objects.get_or_create(**role_data)
        gender, created = Gender.objects.get_or_create(**gender_data)
        params = instance.params

        instance.role = role
        instance.gender = gender
        params.weight = params_data.get('weight', params.weight)
        params.height = params_data.get('height', params.height)
        params.waist_size = params_data.get('waist_size', params.waist_size)
        params.save()

        fields = ('first_name',
                  'last_name',
                  'middle_name',
                  'email',
                  'phone_number',
                  'date_of_birth',
                  'about',
                  'is_specialist',
                  'is_active',)
        for field in fields:
            setattr(instance, field, validated_data.get(
                    field, getattr(instance, field))
                    )
        instance.save()

        return instance


class SpecialistSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    education = EducationSerializer(many=True)

    class Meta:
        model = Specialists
        fields = ('experience',
                  'education',
                  'contacts',
                  'about',)

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
        instance.contacts = validated_data.get('contacts', instance.contacts)
        instance.about = validated_data.get('about', instance.about)

        instance.save()

        instance.education.all().delete()
        for education_item in education_data:
            Education.objects.create(specialist=instance, **education_item)

        return instance
