from django.urls import path

from . import views

app_name ="polls"

urlpatterns = [
    path("", views.IndiceVista.as_view(), name="indice"),
    path("<int:pk>/", views.DetallesVista.as_view(), name="detalles"),
    path("<int:pk>/resultados/", views.ResultadosVista.as_view(), name="resultados"),
    path("<int:pregunta_id>/votacion/", views.votacion, name="votacion")
]