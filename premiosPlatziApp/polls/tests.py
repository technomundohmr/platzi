from django.test import TestCase
from django.utils import timezone
from django.urls import reverse 
from .models import Question
import datetime

class QuestionModelTests(TestCase):
    time = timezone.now()
    question = 'test qestion'
    
    def checkQuestionRecently(self, differenceDays):
        q_time = self.time + datetime.timedelta(days = differenceDays)
        future_question = Question(question_text='Pregunta de test de preguntas en el futuro', timstamp=q_time)
        return future_question.is_recently()
    
    def test_was_public_resently_with_future_questions(self):
        result = self.checkQuestionRecently(+30)
        self.assertIs(result, False)
    
    def test_was_public_resently_with_past_questions(self):
        result = self.checkQuestionRecently(-30)
        self.assertIs(result, False)
    
    def test_was_public_resently_with_present_questions(self):
        result = self.checkQuestionRecently(0)
        self.assertIs(result, True)
        
class QuestionIndexViewTest(TestCase):
    def create_questions(self, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text="test_question", timstamp=time)
        
    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas en este momento")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_future_question(self):
        self.create_questions(30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas en este momento")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_past_question(self):
        self.create_questions(-30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas en este momento")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_there_is_questions(self):
        question = self.create_questions(0)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        
class DetailViewTest(TestCase):
    def test_future_question_details(self):
        question = QuestionIndexViewTest.create_questions(self, 30)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 403)
        
    def test_past_question_details(self):
        question = QuestionIndexViewTest.create_questions(self, -30)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertContains(response, question.question_text)
        self.assertEqual(response.status_code, 200)