import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Preguntas(models.Model):
    texto_pregunta= models.CharField(max_length=200)
    fecha_publicacion= models.DateTimeField("fecha de publicación")
    
    @admin.display(
        boolean=True,
        ordering="fecha_publicacion",
        description="Publicado recientemente?",
    )
    def publicado_recientemente(self):
        ahora = timezone.now()
        return ahora - datetime.timedelta(days=1) <= self.fecha_publicacion <= now

    def __str__(self):
        return self.question_text

class Choice (models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text= models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
    
