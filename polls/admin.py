from django.contrib import admin
from .models import Pregunta, Opcion

# Register your models here.

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra=1

class PreguntaAdmin (admin.ModelAdmin):
    fieldsets = [
        ("Pregunta", {"fields": ["texto_pregunta"]}),
        ("Fecha information", {"fields": ["fecha_publicacion"]}),
    ]
    inlines=[OpcionInline]
    list_display = ["texto_pregunta", "fecha_publicacion", "publicado_recientemente"]
    list_filter = ["fecha_publicacion"]
    search_fields = ["texto_pregunta"]

admin.site.register(Pregunta, PreguntaAdmin)
#admin.site.register(Opcion)
