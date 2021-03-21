from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission



class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser