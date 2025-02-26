import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Pregunta(models.Model):
    texto_pregunta= models.CharField(max_length=200)
    fecha_publicacion= models.DateTimeField("date published")
    
    @admin.display(
        boolean=True,
        ordering="fecha_publicacion",
        description="Publicado recientemente?",
    )
    def publicado_recientemente(self):
        fecha_actual = timezone.now()
        return fecha_actual - datetime.timedelta(days=1) <= self.fecha_publicacion <= fecha_actual

    def __str__(self):
        return self.texto_pregunta

class Opcion (models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_opcion= models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
    
    def __str__(self):
        return self.texto_opcion
    
