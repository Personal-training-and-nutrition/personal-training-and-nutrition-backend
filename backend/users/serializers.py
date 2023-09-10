from rest_framework import serializers
from .models import User, Gender, Params


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


class ParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Params
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
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
