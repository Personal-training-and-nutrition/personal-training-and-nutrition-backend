from django.conf import settings
from rest_framework.fields import (CharField, ChoiceField, DateTimeField,
                                   IntegerField,)
from rest_framework.serializers import ModelSerializer, Serializer

from diets.models import DietPlan, DietPlanDiet, Diets


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
        if validated_data.get("diet") is None:
            return super().update(instance, validated_data)
        instance.diet.clear()
        diets = validated_data.pop("diet")
        instance = super().update(instance, validated_data)
        return self.add_diets(diets, instance)


class DietPlanLinkSerializer(Serializer):
    """Сериализатор для создания ссылки на план питания"""

    diet_plan_id = IntegerField()
    link = CharField()


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
