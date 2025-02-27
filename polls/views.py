from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.db.models import F
from django.views import generic
from django.utils import timezone

from .models import Pregunta, Opcion




class IndiceVista(generic.ListView):
    template_name = "polls/index.html"
    context_object_name= "ultimas_preguntas"
    def get_queryset(self):
        """
        Regresa las últimas 5 preguntas sin incluir las fueron 
        publicadas en el futuro
        """
        return Pregunta.objects.filter(fecha_publicacion__lte=timezone.now()).order_by("-fecha_publicacion")[:5]

class DetallesVista(generic.DetailView):
    model= Pregunta
    template_name= "polls/detalles.html"

    def get_queryset(self):
        """
        Excluye cualquier pregunta que aún no se publique
        """
        return Pregunta.objects.filter(fecha_publicacion__lte=timezone.now())

class ResultadosVista(generic.DetailView):
    model = Pregunta
    template_name = "polls/resultados.html"

def votacion( request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        pk = request.POST["opcion"]
        selected_choice= pregunta.opcion_set.get(pk= pk)
    except (KeyError, Opcion.DoesNotExist):
        context= {
            "pregunta": pregunta,
            "error_message": "No seleccionaste una opción"
        }
        return render(request, "polls/detalles.html", context )
    else:
        selected_choice.votos =  F("votos") + 1 
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:resultados", args=(pregunta_id,)))


