from rest_framework import permissions, viewsets, mixins
from .models import *
from .permissions import *
from .serializers import *


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all().order_by("nom")
    serializer_class = UtilisateurSerializer
    permission_classes = [IsAdminOrSelfReadOnlyOthers]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("nomRole")
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrReadOnly]


class LogViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Log.objects.all().order_by("-dateHeure")
    serializer_class = LogSerializer
    permission_classes = [IsAdminOnly]


class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all().order_by("titre")
    serializer_class = CoursSerializer
    permission_classes = [IsNotEtudiantForWrite]


class RessourceCoursViewSet(viewsets.ModelViewSet):
    queryset = RessourceCours.objects.all().order_by("-dateAjout")
    serializer_class = RessourceCoursSerializer
    permission_classes = [IsNotEtudiantForWrite]


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all().order_by("-dateInscription")
    serializer_class = InscriptionSerializer
    permission_classes = [IsAdminOrReadOnly]