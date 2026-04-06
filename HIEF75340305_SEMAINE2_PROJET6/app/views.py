from rest_framework import permissions, viewsets, mixins
from .models import *
from .permissions import *
from .serializers import *


class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Utilisateur.objects.all().order_by("nom")
    serializer_class = UtilisateurSerializer

    permission_classes =  [permissions.IsAuthenticated, OnlyAdminModify]


class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows roles to be viewed or edited.
    """
    queryset = Role.objects.all().order_by("nomRole")
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, OnlyAdminModify]


class LogViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows logs to be viewed or deleted only.
    (Creating or updating logs is intentionally disabled).
    """
    queryset = Log.objects.all().order_by("-dateHeure")
    serializer_class = LogSerializer
    permission_classes = [permissions.IsAdminUser]


class CoursViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Cours.objects.all().order_by("titre")
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAuthenticated]


class RessourceCoursViewSet(viewsets.ModelViewSet, ReadOnlyEtudiant):
    """
    API endpoint that allows course resources to be viewed or edited.
    """
    queryset = RessourceCours.objects.all().order_by("-dateAjout")
    serializer_class = RessourceCoursSerializer
    permission_classes = [permissions.IsAuthenticated]


class InscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows enrollments to be viewed or edited.
    """
    queryset = Inscription.objects.all().order_by("-dateInscription")
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnlyProfesseur]
