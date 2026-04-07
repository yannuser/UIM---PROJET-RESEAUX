from rest_framework import permissions


def getNomRole(utilisateur):
    if not utilisateur or not utilisateur.is_authenticated:
        return None

    role = getattr(utilisateur, "idRole", None)
    if not role:
        return None

    nomRole = getattr(role, "nomRole", None)
    if not nomRole:
        return None

    return nomRole.strip().lower()


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, requete, vue):
        if not requete.user or not requete.user.is_authenticated:
            return False

        if requete.method in permissions.SAFE_METHODS:
            return True

        return getNomRole(requete.user) == "admin"

    def has_object_permission(self, requete, vue, objet):
        if not requete.user or not requete.user.is_authenticated:
            return False

        if requete.method in permissions.SAFE_METHODS:
            return True

        return getNomRole(requete.user) == "admin"


class IsNotEtudiantForWrite(permissions.BasePermission):
    def has_permission(self, requete, vue):
        if not requete.user or not requete.user.is_authenticated:
            return False

        if requete.method in permissions.SAFE_METHODS:
            return True

        return getNomRole(requete.user) != "etudiant"

    def has_object_permission(self, requete, vue, objet):
        if not requete.user or not requete.user.is_authenticated:
            return False

        if requete.method in permissions.SAFE_METHODS:
            return True

        return getNomRole(requete.user) != "etudiant"


class IsAdminOrSelfReadOnlyOthers(permissions.BasePermission):
    def has_permission(self, requete, vue):
        return bool(requete.user and requete.user.is_authenticated)

    def has_object_permission(self, requete, vue, objet):
        if not requete.user or not requete.user.is_authenticated:
            return False

        nomRole = getNomRole(requete.user)

        if nomRole == "admin":
            return True

        return objet == requete.user


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, requete, vue):
        if not requete.user or not requete.user.is_authenticated:
            return False

        return getNomRole(requete.user) == "admin"

    def has_object_permission(self, requete, vue, objet):
        if not requete.user or not requete.user.is_authenticated:
            return False

        return getNomRole(requete.user) == "admin"


class IsAdminProfesseurResponsableOrEtudiantInscritForCours(permissions.BasePermission):
    def has_permission(self, requete, vue):
        return bool(requete.user and requete.user.is_authenticated)

    def has_object_permission(self, requete, vue, objet):
        if not requete.user or not requete.user.is_authenticated:
            return False

        utilisateurActuel = requete.user
        nomRole = getNomRole(utilisateurActuel)

        if nomRole == "admin":
            return True

        if nomRole == "professeur":
            return objet.idProfesseurResponsable == utilisateurActuel

        if nomRole == "etudiant":
            estInscrit = objet.inscription_set.filter(idEtudiant=utilisateurActuel).exists()

            if requete.method in permissions.SAFE_METHODS:
                return estInscrit

            return False

        return False


class IsAdminProfesseurResponsableOrEtudiantInscritForRessourceCours(permissions.BasePermission):
    def has_permission(self, requete, vue):
        return bool(requete.user and requete.user.is_authenticated)

    def has_object_permission(self, requete, vue, objet):
        if not requete.user or not requete.user.is_authenticated:
            return False

        utilisateurActuel = requete.user
        nomRole = getNomRole(utilisateurActuel)
        cours = objet.idCours

        if nomRole == "admin":
            return True

        if nomRole == "professeur":
            return cours.idProfesseurResponsable == utilisateurActuel

        if nomRole == "etudiant":
            estInscrit = cours.inscription_set.filter(idEtudiant=utilisateurActuel).exists()

            if requete.method in permissions.SAFE_METHODS:
                return estInscrit

            return False

        return False


class IsAdminOrOwnerForInscriptionReadOnlyOthers(permissions.BasePermission):
    def has_permission(self, requete, vue):
        return bool(requete.user and requete.user.is_authenticated)

    def has_object_permission(self, requete, vue, objet):
        if not requete.user or not requete.user.is_authenticated:
            return False

        utilisateurActuel = requete.user
        nomRole = getNomRole(utilisateurActuel)

        if nomRole == "admin":
            return True

        if nomRole == "professeur":
            if requete.method in permissions.SAFE_METHODS:
                return objet.idCours.idProfesseurResponsable == utilisateurActuel
            return False

        if nomRole == "etudiant":
            if requete.method in permissions.SAFE_METHODS:
                return objet.idEtudiant == utilisateurActuel
            return False

        return False