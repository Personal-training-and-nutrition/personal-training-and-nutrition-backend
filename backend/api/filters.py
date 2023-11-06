from django_filters import rest_framework as filters


class TrainingPlanFilter(filters.FilterSet):
    """Обязательный query parameter для get запросов."""

    user = filters.CharFilter(field_name="user__id")


class DietPlanFilter(filters.FilterSet):
    """Обязательный query parameter для get запросов."""

    user = filters.CharFilter(field_name="user__id")
