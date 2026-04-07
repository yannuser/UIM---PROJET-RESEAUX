from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *


class UtilisateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ["idUtilisateur", "idRole", "nom", "prenom", "email", "password", "dateNaissance"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def getNomRole(self, utilisateur):
        role = getattr(utilisateur, "idRole", None)
        if role is None:
            return None
        nomRole = getattr(role, "nomRole", None)
        if nomRole is None:
            return None
        return nomRole.lower()

    def create(self, donneesValidees):
        password = donneesValidees.pop("password", None)
        utilisateur = Utilisateur(**donneesValidees)

        if password is not None:
            if hasattr(utilisateur, "set_password"):
                utilisateur.set_password(password)
            else:
                utilisateur.password = password

        utilisateur.save()
        return utilisateur

    def update(self, instance, donneesValidees):
        requete = self.context.get("request")
        utilisateurActuel = getattr(requete, "user", None)

        if utilisateurActuel is not None:
            nomRole = self.getNomRole(utilisateurActuel)

            if nomRole != "admin":
                donneesValidees.pop("idRole", None)

        password = donneesValidees.pop("password", None)

        for attribut, valeur in donneesValidees.items():
            setattr(instance, attribut, valeur)

        if password is not None:
            if hasattr(instance, "set_password"):
                instance.set_password(password)
            else:
                instance.password = password

        instance.save()
        return instance


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ["idRole", "nomRole"]


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ["idLog", "idUtilisateur", "action", "resultat", "ipAdresse", "dateHeure"]
        read_only_fields = ["idLog", "idUtilisateur", "action", "resultat", "ipAdresse", "dateHeure"]


class CoursSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cours
        fields = ["idCours", "idProfesseurResponsable", "titre", "description", "duree"]

    def getNomRole(self, utilisateur):
        role = getattr(utilisateur, "idRole", None)
        if role is None:
            return None
        nomRole = getattr(role, "nomRole", None)
        if nomRole is None:
            return None
        return nomRole.lower()

    def create(self, donneesValidees):
        requete = self.context.get("request")
        utilisateurActuel = getattr(requete, "user", None)

        if utilisateurActuel is not None:
            nomRole = self.getNomRole(utilisateurActuel)

            if nomRole == "professeur":
                donneesValidees["idProfesseurResponsable"] = utilisateurActuel

        return super().create(donneesValidees)

    def update(self, instance, donneesValidees):
        requete = self.context.get("request")
        utilisateurActuel = getattr(requete, "user", None)

        if utilisateurActuel is not None:
            nomRole = self.getNomRole(utilisateurActuel)

            if nomRole == "professeur":
                donneesValidees["idProfesseurResponsable"] = instance.idProfesseurResponsable

        return super().update(instance, donneesValidees)


class RessourceCoursSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RessourceCours
        fields = ["idRessource", "idCours", "titre", "type", "url", "dateAjout"]

    def getNomRole(self, utilisateur):
        role = getattr(utilisateur, "idRole", None)
        if role is None:
            return None
        nomRole = getattr(role, "nomRole", None)
        if nomRole is None:
            return None
        return nomRole.lower()

    def validate_idCours(self, valeur):
        requete = self.context.get("request")
        utilisateurActuel = getattr(requete, "user", None)

        if utilisateurActuel is not None:
            nomRole = self.getNomRole(utilisateurActuel)

            if nomRole == "professeur":
                if valeur.idProfesseurResponsable != utilisateurActuel:
                    raise serializers.ValidationError(
                        "Vous ne pouvez pas ajouter une ressource à un cours qui ne vous appartient pas."
                    )

        return valeur


class InscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inscription
        fields = ["idInscription", "idEtudiant", "idCours", "dateInscription"]

    def getNomRole(self, utilisateur):
        role = getattr(utilisateur, "idRole", None)
        if role is None:
            return None
        nomRole = getattr(role, "nomRole", None)
        if nomRole is None:
            return None
        return nomRole.lower()

    def create(self, donneesValidees):
        requete = self.context.get("request")
        utilisateurActuel = getattr(requete, "user", None)

        if utilisateurActuel is not None:
            nomRole = self.getNomRole(utilisateurActuel)

            if nomRole == "etudiant":
                donneesValidees["idEtudiant"] = utilisateurActuel

        return super().create(donneesValidees)

    def update(self, instance, donneesValidees):
        requete = self.context.get("request")
        utilisateurActuel = getattr(requete, "user", None)

        if utilisateurActuel is not None:
            nomRole = self.getNomRole(utilisateurActuel)

            if nomRole == "etudiant":
                donneesValidees["idEtudiant"] = instance.idEtudiant

        return super().update(instance, donneesValidees)