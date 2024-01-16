from rest_framework.permissions import SAFE_METHODS, BasePermission


class ClientOrAdmin(BasePermission):
    """Права доступа для клиентов или администраторов"""
    def is_safe_request(self, request):
        return request.method in SAFE_METHODS

    def is_client_owner(self, request, obj):
        return not request.user.is_specialist and request.user == obj.user

    def has_object_permission(self, request, view, obj):
        return (self.is_safe_request(request)
                or self.is_client_owner(request, obj)
                or request.user.is_superuser)


class SpecialistOrAdmin(BasePermission):
    """Права доступа для специалиста или администраторов"""
    def is_safe_request(self, request):
        return request.method in SAFE_METHODS

    def is_client_owner(self, request, obj):
        return request.user.is_specialist and request.user == obj.specialist

    def has_object_permission(self, request, view, obj):
        return (self.is_safe_request(request)
                or self.is_client_owner(request, obj)
                or request.user.is_superuser)
