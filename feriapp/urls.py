"""Rutas raíz del proyecto y delegación hacia la app principal."""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import urls as auth_urls

handler404 = "app.views.notfound_view.custom_404"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls", namespace="ferias")),
    path("users/", include("usuarios.urls", namespace="usuarios")),
    path("accounts/", include(auth_urls)),
    
    
]

