from rest_framework import permissions, viewsets, mixins
from .models import *
from .permissions import *
from .serializers import *


class JournalisationMixin:
    def getIpAdresse(self):
        requete = self.request
        xForwardedFor = requete.META.get("HTTP_X_FORWARDED_FOR")

        if xForwardedFor:
            return xForwardedFor.split(",")[0].strip()

        return requete.META.get("REMOTE_ADDR", "")

    def creerLog(self, action, resultat="succes"):
        utilisateurActuel = getattr(self.request, "user", None)

        if not utilisateurActuel or not utilisateurActuel.is_authenticated:
            utilisateurActuel = None

        Log.objects.create(
            idUtilisateur=utilisateurActuel,
            action=action,
            resultat=resultat,
            ipAdresse=self.getIpAdresse()
        )


class UtilisateurViewSet(JournalisationMixin, viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all().order_by("nom")
    serializer_class = UtilisateurSerializer
    permission_classes = [IsAdminOrSelfReadOnlyOthers]

    def getNomRole(self, utilisateur):
        role = getattr(utilisateur, "idRole", None)
        if role is None:
            return None

        nomRole = getattr(role, "nomRole", None)
        if nomRole is None:
            return None

        return nomRole.lower()

    def get_queryset(self):
        utilisateurActuel = self.request.user
        nomRole = self.getNomRole(utilisateurActuel)

        if nomRole == "admin":
            return Utilisateur.objects.all().order_by("nom")

        return Utilisateur.objects.filter(idUtilisateur=utilisateurActuel.idUtilisateur).order_by("nom")

    def perform_create(self, serializer):
        objet = serializer.save()
        self.creerLog(f"creation utilisateur {objet.idUtilisateur}")

    def perform_update(self, serializer):
        objet = serializer.save()
        self.creerLog(f"modification utilisateur {objet.idUtilisateur}")

    def perform_destroy(self, instance):
        idUtilisateur = instance.idUtilisateur
        instance.delete()
        self.creerLog(f"suppression utilisateur {idUtilisateur}")


class RoleViewSet(JournalisationMixin, viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("nomRole")
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Role.objects.all().order_by("nomRole")

    def perform_create(self, serializer):
        objet = serializer.save()
        self.creerLog(f"creation role {objet.nomRole}")

    def perform_update(self, serializer):
        objet = serializer.save()
        self.creerLog(f"modification role {objet.nomRole}")

    def perform_destroy(self, instance):
        nomRole = instance.nomRole
        instance.delete()
        self.creerLog(f"suppression role {nomRole}")


class LogViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Log.objects.all().order_by("-dateHeure")
    serializer_class = LogSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return Log.objects.all().order_by("-dateHeure")


class CoursViewSet(JournalisationMixin, viewsets.ModelViewSet):
    queryset = Cours.objects.all().order_by("titre")
    serializer_class = CoursSerializer
    permission_classes = [IsAdminProfesseurResponsableOrEtudiantInscritForCours]

    def getNomRole(self, utilisateur):
        role = getattr(utilisateur, "idRole", None)
        if role is None:
            return None

        nomRole = getattr(role, "nomRole", None)
        if nomRole is None:
            return None

        return nomRole.lower()

    def get_queryset(self):
        utilisateurActuel = self.request.user
        nomRole = self.getNomRole(utilisateurActuel)

        if nomRole == "admin":
            return Cours.objects.all().order_by("titre")

        if nomRole == "professeur":
            return Cours.objects.filter(
                idProfesseurResponsable=utilisateurActuel
            ).order_by("titre")

        if nomRole == "etudiant":
            return Cours.objects.filter(
                inscription__idEtudiant=utilisateurActuel
            ).distinct().order_by("titre")

        return Cours.objects.none()

    def perform_create(self, serializer):
        objet = serializer.save()
        self.creerLog(f"creation cours {objet.idCours}")

    def perform_update(self, serializer):
        objet = serializer.save()
        self.creerLog(f"modification cours {objet.idCours}")

    def perform_destroy(self, instance):
        idCours = instance.idCours
        instance.delete()
        self.creerLog(f"suppression cours {idCours}")


class RessourceCoursViewSet(JournalisationMixin, viewsets.ModelViewSet):
    queryset = RessourceCours.objects.all().order_by("-dateAjout")
    serializer_class = RessourceCoursSerializer
    permission_classes = [IsAdminProfesseurResponsableOrEtudiantInscritForRessourceCours]

    def getNomRole(self, utilisateur):
        role = getattr(utilisateur, "idRole", None)
        if role is None:
            return None

        nomRole = getattr(role, "nomRole", None)
        if nomRole is None:
            return None

        return nomRole.lower()

    def get_queryset(self):
        utilisateurActuel = self.request.user
        nomRole = self.getNomRole(utilisateurActuel)

        if nomRole == "admin":
            return RessourceCours.objects.all().order_by("-dateAjout")

        if nomRole == "professeur":
            return RessourceCours.objects.filter(
                idCours__idProfesseurResponsable=utilisateurActuel
            ).order_by("-dateAjout")

        if nomRole == "etudiant":
            return RessourceCours.objects.filter(
                idCours__inscription__idEtudiant=utilisateurActuel
            ).distinct().order_by("-dateAjout")

        return RessourceCours.objects.none()

    def perform_create(self, serializer):
        objet = serializer.save()
        self.creerLog(f"creation ressourceCours {objet.idRessource}")

    def perform_update(self, serializer):
        objet = serializer.save()
        self.creerLog(f"modification ressourceCours {objet.idRessource}")

    def perform_destroy(self, instance):
        idRessource = instance.idRessource
        instance.delete()
        self.creerLog(f"suppression ressourceCours {idRessource}")


class InscriptionViewSet(JournalisationMixin, viewsets.ModelViewSet):
    queryset = Inscription.objects.all().order_by("-dateInscription")
    serializer_class = InscriptionSerializer
    permission_classes = [IsAdminOrOwnerForInscriptionReadOnlyOthers]

    def getNomRole(self, utilisateur):
        role = getattr(utilisateur, "idRole", None)
        if role is None:
            return None

        nomRole = getattr(role, "nomRole", None)
        if nomRole is None:
            return None

        return nomRole.lower()

    def get_queryset(self):
        utilisateurActuel = self.request.user
        nomRole = self.getNomRole(utilisateurActuel)

        if nomRole == "admin":
            return Inscription.objects.all().order_by("-dateInscription")

        if nomRole == "professeur":
            return Inscription.objects.filter(
                idCours__idProfesseurResponsable=utilisateurActuel
            ).order_by("-dateInscription")

        if nomRole == "etudiant":
            return Inscription.objects.filter(
                idEtudiant=utilisateurActuel
            ).order_by("-dateInscription")

        return Inscription.objects.none()

    def perform_create(self, serializer):
        objet = serializer.save()
        self.creerLog(f"creation inscription {objet.idInscription}")

    def perform_update(self, serializer):
        objet = serializer.save()
        self.creerLog(f"modification inscription {objet.idInscription}")

    def perform_destroy(self, instance):
        idInscription = instance.idInscription
        instance.delete()
        self.creerLog(f"suppression inscription {idInscription}")