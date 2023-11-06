from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.serializers import ValidationError

User = get_user_model()


class ClientOrAdmin(BasePermission):
    """Права доступа для клиентов или администраторов"""

    def is_safe_request(self, request):
        return request.method in SAFE_METHODS

    def is_client_owner(self, request, obj):
        return not request.user.is_specialist and request.user == obj.user

    def has_object_permission(self, request, view, obj):
        return (
            self.is_safe_request(request)
            or self.is_client_owner(request, obj)
            or request.user.is_superuser
        )


class SpecialistOrAdmin(BasePermission):
    """Права доступа для специалиста или администраторов"""

    def is_safe_request(self, request):
        return request.method in SAFE_METHODS

    def is_client_owner(self, request, obj):
        return request.user.is_specialist and request.user == obj.specialist

    def has_object_permission(self, request, view, obj):
        return (
            self.is_safe_request(request)
            or self.is_client_owner(request, obj)
            or request.user.is_superuser
        )


class IsCurUserOrTheirSpecialistPermission(BasePermission):
    """Класс разрешений для DietPlanViewSet и TrainingPlanViewSet.

    Ищем пользователя, которого мы получили в query parameters or
    our request payload в списке пользователей, привязанных к автору
    запроса через модель SpecialistClient и выдаем разрешение на
    использование данного вьюсета, если находим.
    """

    def has_permission(self, request, view):
        if all(
            (
                not request.query_params.get("user"),
                not request.data.get("user")
            )
        ):
            raise ValidationError(
                (
                    "Query parameter user is compulsory for any get request."
                    "Your request should look as:"
                    "GET http://127.0.0.1:8000/api/diet-plans/"
                    "?user=9181b013-a5ee-4ff8-a855-c1decd01c322 to get a list "
                    "or GET http://127.0.0.1:8000/api/diet-plans/7/?"
                    "user=9181b013-a5ee-4ff8-a855-c1decd01c322 to get one "
                    "object."
                )
            )
        if request.method == "POST":
            return request.user.specialist_client_spec.filter(
                user=request.data["user"]
            ).exists()
        return request.user.specialist_client_spec.filter(
            user=request.query_params.get("user")
        ).exists()
