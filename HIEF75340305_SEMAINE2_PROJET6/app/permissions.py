from rest_framework import permissions

class ReadOnlyEtudiant(permissions.BasePermission):
    """
    Custom permission to prevent users with a specific role from modifying data.
    They will only be allowed to view (GET) the data.
    """
    def has_permission(self, request, view):
        # 1. SAFE_METHODS are GET, HEAD, and OPTIONS.
        # We always allow these so the user can view the data.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 2. Safety check: ensure the user is actually logged in and has a role
        if not request.user or not request.user.is_authenticated or not request.user.idRole:
            return False

        # 3. Check the role. Replace 'NomDuRoleAExclure' with the actual role name
        # (e.g., 'Etudiant', 'Invite', etc.)
        if request.user.idRole.nomRole == 'Etudiant':
            return False # Deny POST, PUT, PATCH, DELETE

        # Allow modification for everyone else
        return True