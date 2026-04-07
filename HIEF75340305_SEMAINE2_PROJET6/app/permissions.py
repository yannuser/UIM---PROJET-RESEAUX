from rest_framework import permissions


def get_role_name(user):
    if not user or not user.is_authenticated:
        return None

    role = getattr(user, "idRole", None)
    if not role:
        return None

    nom_role = getattr(role, "nomRole", None)
    if not nom_role:
        return None

    return nom_role.strip().lower()


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return get_role_name(request.user) == "admin"


class IsNotEtudiantForWrite(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return get_role_name(request.user) != "etudiant"


class IsAdminOrSelfReadOnlyOthers(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        role_name = get_role_name(request.user)

        if role_name == "admin":
            return True

        return obj == request.user


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return get_role_name(request.user) == "admin"