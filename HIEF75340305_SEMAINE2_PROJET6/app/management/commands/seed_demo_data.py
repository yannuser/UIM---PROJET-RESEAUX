from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from app.models import Role, Utilisateur, Log, Cours, RessourceCours, Inscription


class Command(BaseCommand):
    help = "Insère des données de démonstration cohérentes pour le projet UIM"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Supprime d'abord les données existantes avant d'insérer les nouvelles"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        reset = options["reset"]

        if reset:
            self.stdout.write(self.style.WARNING("Suppression des données existantes..."))
            Log.objects.all().delete()
            Inscription.objects.all().delete()
            RessourceCours.objects.all().delete()
            Cours.objects.all().delete()
            Utilisateur.objects.all().delete()
            Role.objects.all().delete()

        self.stdout.write("Création / récupération des rôles...")
        role_admin, _ = Role.objects.get_or_create(nomRole="Admin")
        role_prof, _ = Role.objects.get_or_create(nomRole="Professeur")
        role_etudiant, _ = Role.objects.get_or_create(nomRole="Etudiant")

        self.stdout.write("Création / récupération des utilisateurs...")

        admin, _ = Utilisateur.objects.get_or_create(
            email="admin@uim.com",
            defaults={
                "idRole": role_admin,
                "nom": "Admin",
                "prenom": "Systeme",
                "motDePasse": "hashed_admin_pwd",
                "dateNaissance": date(1990, 1, 1),
            }
        )

        prof_jean, _ = Utilisateur.objects.get_or_create(
            email="jean.dupont@uim.com",
            defaults={
                "idRole": role_prof,
                "nom": "Dupont",
                "prenom": "Jean",
                "motDePasse": "hashed_prof_pwd",
                "dateNaissance": date(1985, 3, 12),
            }
        )

        prof_claire, _ = Utilisateur.objects.get_or_create(
            email="claire.martin@uim.com",
            defaults={
                "idRole": role_prof,
                "nom": "Martin",
                "prenom": "Claire",
                "motDePasse": "hashed_prof_pwd",
                "dateNaissance": date(1988, 7, 22),
            }
        )

        etu_aminata, _ = Utilisateur.objects.get_or_create(
            email="aminata.diallo@uim.com",
            defaults={
                "idRole": role_etudiant,
                "nom": "Diallo",
                "prenom": "Aminata",
                "motDePasse": "hashed_etu_pwd",
                "dateNaissance": date(2000, 5, 10),
            }
        )

        etu_moussa, _ = Utilisateur.objects.get_or_create(
            email="moussa.kone@uim.com",
            defaults={
                "idRole": role_etudiant,
                "nom": "Kone",
                "prenom": "Moussa",
                "motDePasse": "hashed_etu_pwd",
                "dateNaissance": date(1999, 11, 20),
            }
        )

        etu_john, _ = Utilisateur.objects.get_or_create(
            email="john.smith@uim.com",
            defaults={
                "idRole": role_etudiant,
                "nom": "Smith",
                "prenom": "John",
                "motDePasse": "hashed_etu_pwd",
                "dateNaissance": date(2001, 2, 14),
            }
        )

        etu_kevin, _ = Utilisateur.objects.get_or_create(
            email="kevin.lee@uim.com",
            defaults={
                "idRole": role_etudiant,
                "nom": "Lee",
                "prenom": "Kevin",
                "motDePasse": "hashed_etu_pwd",
                "dateNaissance": date(2002, 8, 9),
            }
        )

        self.stdout.write("Création / récupération des cours...")

        cours_reseaux, _ = Cours.objects.get_or_create(
            titre="Reseaux",
            defaults={
                "idProfesseurResponsable": prof_jean,
                "description": "Cours sur les concepts fondamentaux des reseaux informatiques",
                "duree": "40h",
            }
        )

        cours_securite, _ = Cours.objects.get_or_create(
            titre="Securite",
            defaults={
                "idProfesseurResponsable": prof_claire,
                "description": "Cours sur la securite informatique et la protection des acces",
                "duree": "35h",
            }
        )

        cours_ia, _ = Cours.objects.get_or_create(
            titre="Introduction a l IA",
            defaults={
                "idProfesseurResponsable": prof_jean,
                "description": "Cours introductif sur les principes de l intelligence artificielle",
                "duree": "30h",
            }
        )

        self.stdout.write("Création / récupération des ressources...")

        RessourceCours.objects.get_or_create(
            idCours=cours_reseaux,
            titre="Slides Reseaux - Chapitre 1",
            defaults={
                "type": "pdf",
                "url": "https://cloud.example.com/reseaux/chapitre1.pdf",
            }
        )

        RessourceCours.objects.get_or_create(
            idCours=cours_reseaux,
            titre="TP Reseaux - Introduction",
            defaults={
                "type": "pdf",
                "url": "https://cloud.example.com/reseaux/tp1.pdf",
            }
        )

        RessourceCours.objects.get_or_create(
            idCours=cours_securite,
            titre="Slides Securite - Authentification",
            defaults={
                "type": "slides",
                "url": "https://cloud.example.com/securite/authentification.pdf",
            }
        )

        RessourceCours.objects.get_or_create(
            idCours=cours_securite,
            titre="Manuel Securite - Controle d'acces",
            defaults={
                "type": "manuel",
                "url": "https://cloud.example.com/securite/manuel_acces.pdf",
            }
        )

        RessourceCours.objects.get_or_create(
            idCours=cours_ia,
            titre="Slides IA - Introduction",
            defaults={
                "type": "slides",
                "url": "https://cloud.example.com/ia/introduction.pdf",
            }
        )

        self.stdout.write("Création / récupération des inscriptions...")

        Inscription.objects.get_or_create(
            idEtudiant=etu_aminata,
            idCours=cours_reseaux,
            defaults={"dateInscription": date.today() - timedelta(days=20)}
        )

        Inscription.objects.get_or_create(
            idEtudiant=etu_moussa,
            idCours=cours_reseaux,
            defaults={"dateInscription": date.today() - timedelta(days=18)}
        )

        Inscription.objects.get_or_create(
            idEtudiant=etu_john,
            idCours=cours_securite,
            defaults={"dateInscription": date.today() - timedelta(days=15)}
        )

        Inscription.objects.get_or_create(
            idEtudiant=etu_kevin,
            idCours=cours_ia,
            defaults={"dateInscription": date.today() - timedelta(days=12)}
        )

        Inscription.objects.get_or_create(
            idEtudiant=etu_aminata,
            idCours=cours_securite,
            defaults={"dateInscription": date.today() - timedelta(days=10)}
        )

        self.stdout.write("Création des logs de démonstration...")

        now = timezone.now()

        logs = [
            {
                "idUtilisateur": etu_aminata,
                "action": "login",
                "resultat": Log.ChoixResultats.SUCCES,
                "ipAdresse": "192.168.1.10",
                "dateHeure": now - timedelta(hours=2),
            },
            {
                "idUtilisateur": etu_moussa,
                "action": "login",
                "resultat": Log.ChoixResultats.SUCCES,
                "ipAdresse": "192.168.1.11",
                "dateHeure": now - timedelta(hours=1),
            },
            {
                "idUtilisateur": etu_aminata,
                "action": "consultation_cours_reseaux",
                "resultat": Log.ChoixResultats.SUCCES,
                "ipAdresse": "192.168.1.10",
                "dateHeure": now - timedelta(minutes=40),
            },
            {
                "idUtilisateur": etu_aminata,
                "action": "telechargement_ressource",
                "resultat": Log.ChoixResultats.SUCCES,
                "ipAdresse": "192.168.1.10",
                "dateHeure": now - timedelta(minutes=35),
            },
            {
                "idUtilisateur": prof_jean,
                "action": "ajout_ressource_cours",
                "resultat": Log.ChoixResultats.SUCCES,
                "ipAdresse": "192.168.1.5",
                "dateHeure": now - timedelta(hours=3),
            },
            {
                "idUtilisateur": etu_john,
                "action": "login",
                "resultat": Log.ChoixResultats.ECHEC,
                "ipAdresse": "192.168.1.20",
                "dateHeure": now - timedelta(minutes=10),
            },
            {
                "idUtilisateur": etu_john,
                "action": "login",
                "resultat": Log.ChoixResultats.ECHEC,
                "ipAdresse": "192.168.1.20",
                "dateHeure": now - timedelta(minutes=9),
            },
            {
                "idUtilisateur": etu_john,
                "action": "login",
                "resultat": Log.ChoixResultats.ECHEC,
                "ipAdresse": "192.168.1.20",
                "dateHeure": now - timedelta(minutes=8),
            },
            {
                "idUtilisateur": etu_john,
                "action": "login",
                "resultat": Log.ChoixResultats.SUCCES,
                "ipAdresse": "45.33.32.156",
                "dateHeure": now - timedelta(minutes=5),
            },
            {
                "idUtilisateur": etu_aminata,
                "action": "acces_zone_admin",
                "resultat": Log.ChoixResultats.ECHEC,
                "ipAdresse": "192.168.1.10",
                "dateHeure": now - timedelta(minutes=3),
            },
        ]

        for log_data in logs:
            existe = Log.objects.filter(
                idUtilisateur=log_data["idUtilisateur"],
                action=log_data["action"],
                resultat=log_data["resultat"],
                ipAdresse=log_data["ipAdresse"],
            ).exists()

            if not existe:
                # auto_now_add empêche normalement de fixer facilement dateHeure à la création
                log = Log.objects.create(
                    idUtilisateur=log_data["idUtilisateur"],
                    action=log_data["action"],
                    resultat=log_data["resultat"],
                    ipAdresse=log_data["ipAdresse"],
                )
                Log.objects.filter(pk=log.pk).update(dateHeure=log_data["dateHeure"])

        self.stdout.write(self.style.SUCCESS("Données de démonstration insérées avec succès."))