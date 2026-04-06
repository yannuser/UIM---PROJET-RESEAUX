from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *


class UtilisateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ["idUtilisateur", "idRole", "nom", "prenom", "email", "password", "dateNaissance"]

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ["idRole", "nomRole"]

class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ["idLog", "idUtilisateur", "action", "resultat", "ipAdresse", "dateHeure"]

class CoursSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cours
        fields = ["idCours", "idProfesseurResponsable", "titre", "description", "duree"]

class RessourceCoursSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RessourceCours
        fields = ["idRessource", "idCours", "titre", "type", "url", "dateAjout"]

class InscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inscription
        fields = ["idInscription", "idEtudiant", "idCours", "dateInscription"]