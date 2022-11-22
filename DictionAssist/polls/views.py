from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.views import generic

#get the question and choice child objects with their respective methods
from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """return last 5 published question"""
        return Question.objects.order_by('question_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    template_name = "polls/results.html"
    model=Question

def vote(request, question_id):
    question = get_object_or_404(question_id)
    try:
        #request.POST is a dictionary
        #
        choice_select = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        #user did not select correctly
        return render(question, {
            'question': question,
            'error_message': 'no current choice selected',
        })
    else:
        choice_select += 1
        choice_select.save()
        #make sure the response is not posted twice
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
