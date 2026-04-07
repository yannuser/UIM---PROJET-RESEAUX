from rest_framework.views import exception_handler
from rest_framework import status
from .models import Log


def getIpAdresse(requete):
    xForwardedFor = requete.META.get("HTTP_X_FORWARDED_FOR")

    if xForwardedFor:
        return xForwardedFor.split(",")[0].strip()

    return requete.META.get("REMOTE_ADDR", "")


def creerLogEchec(requete, action, resultat="echec"):
    utilisateurActuel = getattr(requete, "user", None)

    if not utilisateurActuel or not utilisateurActuel.is_authenticated:
        utilisateurActuel = None

    Log.objects.create(
        idUtilisateur=utilisateurActuel,
        action=action,
        resultat=resultat,
        ipAdresse=getIpAdresse(requete)
    )


def customExceptionHandler(exception, contexte):
    reponse = exception_handler(exception, contexte)

    requete = contexte.get("request")
    vue = contexte.get("view")

    if reponse is None or requete is None:
        return reponse

    if not requete.user or not requete.user.is_authenticated:
        return reponse

    methodeHttp = requete.method
    chemin = requete.path
    nomVue = vue.__class__.__name__ if vue else "VueInconnue"
    codeStatut = reponse.status_code

    if codeStatut >= 400:
        action = f"echec {methodeHttp} {chemin} dans {nomVue} code {codeStatut}"
        creerLogEchec(requete, action)

    return reponse