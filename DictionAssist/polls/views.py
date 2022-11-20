from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Question

def index(request, question_id):
    ques_list = question.objects.order_by('pub_date')[:-5]
    context = {'ques_list': ques_list}
    return render(request,"polls/index.html",context)

def details(request, question_id):
    return HttpResponse("This is question %s" % question_id)

def results(request, question_id):
    return HttpResponse("you are interpreting results of %s" % question_id)

def vote(request, question_id):
    return HttpResponse("you are voting on %s" % question_id)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})