from django.contrib import admin
from .models import *

# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    list_display = ("idRole", "nomRole")
    search_fields = ("nomRole",)

admin.site.register(Role, RoleAdmin)


class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "email", "dateNaissance", "idRole")
    list_editable = ("nom", "prenom", "dateNaissance")
    list_display_links = ("email",)
    search_fields = ("email", "nom", "prenom")
    list_filter = ("idRole",)
    ordering = ("nom",)
    readonly_fields = ("email",)

admin.site.register(Utilisateur, UtilisateurAdmin)


class CoursAdmin(admin.ModelAdmin):
    list_display = ("titre", "idProfesseurResponsable", "description", "duree")
    list_editable = ("description", "duree")
    search_fields = ("titre",)
    list_filter = ("duree",)
    ordering = ("titre",)

admin.site.register(Cours, CoursAdmin)


class RessourceCoursAdmin(admin.ModelAdmin):
    list_display = ("titre", "idCours", "type", "url", "dateAjout")
    list_filter = ("type", "idCours")
    search_fields = ("titre", "type")
    readonly_fields = ("dateAjout",)
    ordering = ("-dateAjout", )

admin.site.register(RessourceCours, RessourceCoursAdmin)


class InscriptionAdmin(admin.ModelAdmin):
    list_display = ("idInscription", "idEtudiant", "idCours", "dateInscription")
    list_filter = ("idCours", "dateInscription")

    search_fields = ("idEtudiant__nom", "idEtudiant__prenom", "idCours__titre")

admin.site.register(Inscription, InscriptionAdmin)


class LogAdmin(admin.ModelAdmin):
    list_display = ("action", "idUtilisateur", "resultat", "ipAdresse", "dateHeure")
    list_filter = ("resultat", "dateHeure")
    search_fields = ("action", "ipAdresse", "idUtilisateur__email")
    readonly_fields = ("dateHeure",)

    ordering = ("-dateHeure", )

admin.site.register(Log, LogAdmin)