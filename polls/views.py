from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from .models import Pregunta, Opcion

import json


def top_encuestas(min=3):
    mas_votadas = Pregunta.objects.filter(
    fecha_publicacion__lte=timezone.now()
    ).annotate(
        total_votos=Coalesce(Sum('opcion__votos'), Value(0))
    ).order_by('-total_votos')[:min]


    votadas_reciente = Pregunta.objects.order_by('-fecha_votacion')[:min]
    context = {
        #'ultimas_preguntas': ultimas_preguntas,
        'mas_votadas': mas_votadas,
        'votadas_reciente': votadas_reciente, 
    }

    return context

def indice_vista(request):
    ultimas_preguntas = Pregunta.objects.filter(
        fecha_publicacion__lte=timezone.now()
    ).order_by('-fecha_publicacion')
    context = top_encuestas()

    context["ultimas_preguntas"] = ultimas_preguntas


    return render(request, 'polls/index.html', context)

def mapa2(request):
    context = top_encuestas()
    return render(request, 'polls/mapa2.html', context)

def mapa(request):
    with open("polls/static/polls/alcaldias.geojson", 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    context = top_encuestas()
    context["geojson_data"] = geojson_data
    return render(request, 'polls/mapa.html', context)


class CrearPregunta(generic.CreateView):
    model= Pregunta
    fields = ["texto_pregunta", "fecha_publicacion"]
    template_name = "polls/crear_pregunta.html"


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
    """
    Actualiza los votos, en la base de datos, de la opción seleccionada para la pregunta indicada,
    y redirige a la página de resultados. 
    Si el usario no seleccionada una opción, vuelve a renderizar la página.
    """
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        pk = request.POST["opcion"]
        opcion_seleccionada= pregunta.opcion_set.get(pk= pk)
    except (KeyError, Opcion.DoesNotExist):
        context= {
            "pregunta": pregunta,
            "error_message": "No seleccionaste una opción"
        }
        return render(request, "polls/detalles.html", context )
    else:
        opcion_seleccionada.votos =  F("votos") + 1 
        opcion_seleccionada.save()
        pregunta.fecha_votacion = timezone.now()
        pregunta.save()
        return HttpResponseRedirect(reverse("polls:resultados", args=(pregunta_id,)))


