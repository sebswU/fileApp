from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import TemplateView, DetailView,DayArchiveView
from krenger.models import Person, TxtRec, WordCard

# Create your views here.
class Form(TemplateView):
    template_name = 'krenger/templates/index.html'
    def view(request, template_name):
        
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.")
        else:
            
            model = TxtRec
            return render(request,template_name)
    def __str__(self):
        return self.name

class Settings(DetailView):
    template_name = 'krenger/templates/user_site.html'
    def view(request, template_name):
        
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.")
        else:
            
            model = Person
            return render(request, template_name)
    def __str__(self):
        return self.name
    
class WordArchive(DetailView):
    template_name = 'krenger/templates/words.html'
    def view(request, template_name):
        
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.")
        else:
            
            model = WordCard
            return render(request,template_name)
    def __str__(self):
        return self.name