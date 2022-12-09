from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import TemplateView, DetailView,DayArchiveView
from krenger.models import Person, TxtRec, WordCard

# Create your views here.
class Form(TemplateView):
    def view(request):
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.")
        else:
            template = 'templates/templates/index.html'
            model = TxtRec
            return render(request,template)
    def __str__(self):
        return self.name

class Settings(DetailView):
    def view(request):
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.")
        else:
            template = 'krenger/templates/user_site.html'
            model = Person
            return render(request, template)
    def __str__(self):
        return self.name
    
class WordArchive(DayArchiveView):
    def view(request):
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.")
        else:
            template = 'krenger/templates/words.html'
            model = WordCard
            return render(request,template)
    def __str__(self):
        return self.name