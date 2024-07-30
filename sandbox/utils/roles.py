from rest_framework.permissions import BasePermission


class IsAuthorized(BasePermission):
    """
    Allow access only for authorized users
    """
    def simple_permission_check(self, request, view):
        base_permission_check = request.user and request.user.is_authenticated

        return base_permission_check

    def has_permission(self, request, view):
        return self.simple_permission_check(request, view)
