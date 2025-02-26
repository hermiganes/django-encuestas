from django.contrib import admin
from .models import Question, Choice

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra=1

class QuestionAdmin (admin.ModelAdmin):
    fieldsets = [
        ("Pregunta", {"fields": ["question_text"]}),
        ("Fecha information", {"fields": ["fecha_publicacion"]}),
    ]
    inlines=[ChoiceInline]
    list_display = ["question_text", "fecha_publicacion", "was_published_recently"]
    list_filter = ["fecha_publicacion"]
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)
