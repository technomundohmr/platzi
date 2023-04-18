from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime


class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter( timstamp__lte = timezone.now(), timstamp__gte = timezone.now() - datetime.timedelta(5)).order_by("-timstamp")[:5]
    
class DetailView(generic.DetailView):
    template_name = 'polls/details.html'
    model = Question
    def get_queryset(self):
        question = Question.objects.filter( timstamp__lte = timezone.now())
        if question.exists():
            return Question.objects.filter( timstamp__lte = timezone.now())
        else: 
            raise PermissionDenied
    
    
class ResultView(DetailView):
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            "error_message": "No elegiste una respuesta correcta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:result", args=(question.id,)))
