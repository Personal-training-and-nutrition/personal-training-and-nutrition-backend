from rest_framework.permissions import SAFE_METHODS, BasePermission


class SpecialistOrAdmin(BasePermission):
    """Права доступа для специалиста или администраторов"""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_specialist is True
                    and request.user == obj.specialist)
                or request.user.is_superuser)
