from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Role(models.Model):
    idRole = models.BigAutoField(primary_key=True)
    nomRole = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.nomRole


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        if not password:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)

        # set_password hashes the password securely instead of saving plain text
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    idUtilisateur = models.BigAutoField(primary_key=True)
    idRole = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dateNaissance = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=100, null=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UtilisateurManager()

    # Tell Django to use email for logging in instead of a username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom}, {self.prenom}"


class Log(models.Model):
    class ChoixResultats(models.TextChoices):
        SUCCES = "succes"
        ECHEC = "echec"

    idLog = models.BigAutoField(primary_key=True)
    idUtilisateur = models.ForeignKey(Utilisateur, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=100)
    resultat = models.CharField(max_length=20, choices=ChoixResultats.choices)
    ipAdresse = models.CharField(max_length=100)
    dateHeure = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} : {self.resultat}"


class Cours(models.Model):
    idCours = models.BigAutoField(primary_key=True)
    idProfesseurResponsable = models.ForeignKey(Utilisateur, on_delete=models.DO_NOTHING)
    titre = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    duree = models.CharField(max_length=50)

    def __str__(self):
        return self.titre


class RessourceCours(models.Model):
    idRessource = models.BigAutoField(primary_key=True)
    idCours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    dateAjout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} : {self.type}"


class Inscription(models.Model):
    idInscription = models.BigAutoField(primary_key=True)
    idEtudiant = models.ForeignKey(Utilisateur, on_delete=models.DO_NOTHING)
    idCours = models.ForeignKey(Cours, on_delete=models.DO_NOTHING)
    dateInscription = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["idEtudiant", "idCours"],
                name="unique_inscription_etudiant_cours"
            )
        ]

    def __str__(self):
        return f"{self.idInscription} : {self.idCours}"