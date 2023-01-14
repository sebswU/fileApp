from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView, DetailView,DayArchiveView
from krenger.models import Person,TxtRec, WordCard, inputForm
from django.urls import reverse
import boto3
import datetime
import time
import os
# Create your views here

def view(request):
    """POST function: upload file to s3 bucket, start transcription, go to s3 bucket where aws transcribe saved, get file, compare"""
    model = TxtRec
    if request.method == "POST":
    #TODO:find a way to check if its an audio file
    #TODO: troubleshoot api for aws
        fileFormat = "mp3"
        location = "us-east-1"
        s3URI = f"s3://webapp2012/audio_files/"
        lang = "en-US"
        form = inputForm(request.POST)
        data = form['audio']
        if form.is_valid():
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('webapp2012')
            Key=f'{datetime.fromtimestamp(time.time())}'
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
            with open('../down/transcripts.txt','wb') as data:
                bucket.download_file('down', data)
            #get the content of the file and then return it
            content = open('../down/transcripts/txt','r').read()
            print(content)
            return HttpResponseRedirect(reverse('krenger:home'))
        else:
            form=inputForm();
            
    return render(request,'krenger/templates/index.html')


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

