from rest_framework import serializers

from .models import DietPlan


class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = ('id', 'user', 'describe ', 'create_dt')
