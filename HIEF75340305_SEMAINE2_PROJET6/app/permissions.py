from rest_framework import permissions

class ReadOnlyEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated or not request.user.idRole:
            return False

        if request.user.idRole.nomRole == 'Etudiant':
            return False

        return True


class OnlyAdminModify(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return  True

        if not request.user or not request.user.is_authenticated or not request.user.idRole:
            return False

        if request.user.idRole.nomRole == 'Admin':
            return True

        return  False

class ReadOnlyProfesseur(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return  True

        if not request.user or not request.user.is_authenticated or not request.user.idRole:
            return False

        if request.user.idRole.nomRole == 'Professeur':
            return False

        return False
