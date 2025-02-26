import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Pregunta
# Create your tests here.


class PreguntaModelTests(TestCase):
    def test_publicado_recientemente_with_future_question(self):
        """
            Devuelve False para preguntas cuyo pub_date esté en el futuro
        """
        time= timezone.now() + datetime.timedelta(days=30)
        future_question= Pregunta(fecha_publicacion=time)
        self.assertIs(future_question.publicado_recientemente(), False)
    
    def test_publicado_recientemente_with_old_question(self):
        """
            Devuelve False para preguntas cuyo fecha_publicacion sea mayor a un día
        """
        time= timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question= Pregunta(fecha_publicacion=time)
        self.assertIs(old_question.publicado_recientemente(), False)

    def test_publicado_recientemente_with_recent_question(self):
        """
            Devuelve True para preguntas cuyo fecha_publicacion sea del último día
        """
        time= timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question= Pregunta(fecha_publicacion=time)
        self.assertIs(recent_question.publicado_recientemente(), True)

def create_question(question_text, days):
    """
    Crea una preguntas con el question_text y la publica x días apartir de
    hoy (negativo para el pasado y positivo para el futuro)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Pregunta.objects.create(question_text=question_text, fecha_publicacion=time)


class PreguntaIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Si la pregunta no existe muestra un mesaje
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["ultimas_preguntas"], [])

    def test_past_question(self):
        """
        Si la pregunta fue publicada en el pasado se muestra
        el index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["ultimas_preguntas"],
            [question],
        )

    def test_future_question(self):
        """
        Si la pregunta fue publicada en el futuro no muestra
        el index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["ultimas_preguntas"], [])

    def test_future_question_and_past_question(self):
        """
        Solo muestra preguntas pasadas, aunque existan futuras
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["ultimas_preguntas"],
            [question],
        )

    def test_two_past_questions(self):
        """
        La página index puede mostrar varias preguntas
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["ultimas_preguntas"],
            [question2, question1],
        )


class PreguntaDetailViewTests(TestCase):
    def test_future_question(self):
        """
        la view de una pregunta publicada en el futuro, 
        regresara un un 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        la view de una pregunta publicada en el pasado 
        regresara el texto de la pregunta
        """
        past_question = create_question(question_text="Past Pregunta.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
