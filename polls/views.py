from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.db.models import F
from django.views import generic
from django.utils import timezone

from .models import Pregunta, Opcion




class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name= "ultimas_preguntas"
    def get_queryset(self):
        """
        Regresa las últimas 5 preguntas sin incluir las fueron 
        publicadas en el futuro
        """
        return Pregunta.objects.filter(fecha_publicacion__lte=timezone.now()).order_by("-fecha_publicacion")[:5]

class DetailView(generic.DetailView):
    model= Pregunta
    template_name= "polls/detail.html"

    def get_queryset(self):
        """
        Exclute cualquier pregunta que aun no se publique
        """
        return Pregunta.objects.filter(fecha_publicacion__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Pregunta
    template_name = "polls/results.html"

"""

def index(request):
    ultimas_preguntas= Pregunta.objects.order_by("-fecha_publicacion")[:5]
    #template = loader.get_template("polls/index.html")
    context = {
        "ultimas_preguntas": ultimas_preguntas,
    }
    #output= ", ".join([q.texto_pregunta for q in ultimas_preguntas])
    #return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context )

def detail(request, pregunta_id):

    #try:
    #    pregunta = Pregunta.objects.get(id=pregunta_id)
    #except:
    #    raise Http404("La pregunta no existe")
    #return HttpResponse(f"La pregunta es {pregunta_id} es: {pregunta}")

    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, "polls/detail.html", {"pregunta": pregunta})

def results(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, "polls/results.html", {"pregunta": pregunta})
"""
def vote( request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        selected_choice= pregunta.choice_set.get(pk= request.POST["choice"])
    except (KeyError, Opcion.DoesNotExist):
        context= {
            "pregunta": pregunta,
            "error_message": "No seleccionaste una opción"
        }
        return render(request, "polls/detail.html", context )
    else:
        selected_choice.votos =  F("votos") + 1 
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(pregunta_id,)))


