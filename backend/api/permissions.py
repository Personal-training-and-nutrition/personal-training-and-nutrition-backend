from rest_framework.permissions import SAFE_METHODS, BasePermission


class ClientOrAdmin(BasePermission):
    """Права доступа для клиентов или администраторов"""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_specialist is False
                    and request.user == obj.user)
                or request.user.is_superuser)
