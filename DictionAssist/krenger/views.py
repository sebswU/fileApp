from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView, DetailView,DayArchiveView
from krenger.models import Person,TxtRec, WordCard
from krenger.forms import inputForm
from django.urls import reverse
import boto3
import datetime
import time
import os
# Create your views here

def view(request):
    """POST function: upload file to s3 bucket, start transcription, go to s3 bucket where aws transcribe saved, get file, compare"""
    model = TxtRec
    form = inputForm()
    if request.method == "POST":
    #TODO:find a way to check if its an audio file
    #TODO: troubleshoot api for aws
        fileFormat = "mp3"
        location = "us-east-1"
        s3URI = f"s3://webapp2012/audio_files/"
        lang = "en-US"
        form = inputForm(request.POST, request.FILES)
        data = request.FILES['audio']
        text = request.POST['text']
        if form.is_valid():
            open('DictionAssist/down/transcripts.txt', 'w').write(text)
                
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('webapp2012')
            Key=f'{time.time()}'
            bucket.put_object(Key=Key, Body=data)
            client = boto3.client('transcribe',region_name=location)
            jobName = Key
            #transcribe and save to s3 bucket
            client.start_transcription_job(
                TranscriptionJobName = jobName,
                Media={
                    'MediaFileUri': s3URI+Key+'/'
                },
                MediaFormat=fileFormat,
                LanguageCode = lang,
                OutputBucketName = 'webapp2012',
                OutputKey = 'transcription_results/'
            )
            chances = 60
            #get the location of the saved transcript file
            while chances > 0:
                chances -= 1
                job = client.get_transcription_job(TranscriptionJobName=jobName)
                jobLoc = job['Transcript']['TranscriptFileUri']
                print(f"job {jobLoc}")
                break
            #download transcript file
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('webapp2012')
            with open('DictionAssist/down/transcripts.txt','wb') as data:
                bucket.download_file('down', data)
            #get the content of the file and then return it
            content = open('../down/transcripts/txt','r').read()
            print(content)
            return HttpResponseRedirect(reverse('krenger:home'))
        else:
            form=inputForm();
            #FIXME:web content delivery
            #TODO: add a button for signup/login
            #TODO: register app on Merriam-webster
            #TODO: develop merriam webster api call
            #TODO: word cards in detail view
        return render(request,'krenger/templates/index.html',{'form':form})  
    return render(request,'krenger/templates/index.html',{'form':form})


class Settings(TemplateView):
    template_name = 'krenger/templates/user_site.html'
    def view(request, template_name):
        
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.</h1>")
        else:
            
            model = Person
            return render(request, template_name)
    def __str__(self):
        return self.name
    
class WordArchive(TemplateView):
    template_name = 'krenger/templates/words.html'
    def view(request, template_name):
        
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.</h1>")
        else:
            
            model = WordCard
            return render(request,template_name)
    
    
    def __str__(self):
        return self.name

#'Traceback (most recent call last):\n  File "/Users/sebastianwu/.vscode/extensions/ms-python.python-2022.8.1/pythonFiles/lib/python/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_resolver.py", line 192, in _get_py_dictionary\n    attr = getattr(var, name)\n  File "/opt/homebrew/lib/python3.10/site-packages/django/core/files/utils.py", line 37, in <lambda>\n    encoding = property(lambda self: self.file.encoding)\nAttributeError: \'_io.BytesIO\' object has no attribute \'encoding\'\n'