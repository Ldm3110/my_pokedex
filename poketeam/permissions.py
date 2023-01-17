from rest_framework.permissions import BasePermission


class PoketeamPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.method == "PATCH":
            if obj.trainer.id == request.user.id:
                return True
            else:
                return False
