from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.db.models import F
from django.views import generic
from .models import Question, Choice



class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name= "ultimas_preguntas"
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model= Question
    template_name= "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

"""

def index(request):
    ultimas_preguntas= Question.objects.order_by("-pub_date")[:5]
    #template = loader.get_template("polls/index.html")
    context = {
        "ultimas_preguntas": ultimas_preguntas,
    }
    #output= ", ".join([q.question_text for q in ultimas_preguntas])
    #return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context )

def detail(request, question_id):

    #try:
    #    question = Question.objects.get(id=question_id)
    #except:
    #    raise Http404("La pregunta no existe")
    #return HttpResponse(f"La pregunta es {question_id} es: {question}")

    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
"""
def vote( request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice= question.choice_set.get(pk= request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        context= {
            "question": question,
            "error_message": "No seleccionaste una opción"
        }
        return render(request, "polls/detail.html", context )
    else:
        selected_choice.votes = F("votes") +1 
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


