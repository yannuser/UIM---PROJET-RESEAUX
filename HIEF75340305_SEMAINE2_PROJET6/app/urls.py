from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'user', UtilisateurViewSet)
router.register(r'role', RoleViewSet)
router.register(r'log', LogViewSet)
router.register(r'course', CoursViewSet)
router.register(r'resource', RessourceCoursViewSet)
router.register(r'inscription', InscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]