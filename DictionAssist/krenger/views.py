from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import TemplateView, DetailView,DayArchiveView
from krenger.models import Person, TxtRec, WordCard
import boto3
import datetime
import time
import os
from dotenv import load_dotenv
load_dotenv()
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
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.</h1>")
        else:
            
            model = Person
            return render(request, template_name)
    def __str__(self):
        return self.name
    
class WordArchive(DetailView):
    template_name = 'krenger/templates/words.html'
    def view(request, template_name):
        
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.</h1>")
        else:
            
            model = WordCard
            return render(request,template_name)
    
    def get_queryset(request, format='wav', lang='en', location='us-east-1', s3URI='s3://webapp2012/audio_files/'):
        model=TxtRec
        """upload file to s3 bucket, start transcription, go to s3 bucket where aws transcribe saved, get file, compare"""
        if request == 'POST':
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('webapp2012')
            Key=f'{datetime.fromtimestamp(time.time())}'
            bucket.put_object(Key=Key, Body=data)
            client = boto3.client('transcribe',region_name=location)
            jobName = Key
            #transcribe and save to s3 bucket
            client.start_transcription_job(
                region = location,
                TranscriptionJobName = jobName,
                #TODO: complete code to perform a transcription job
                Media={
                    'MediaFileUri': s3URI
                },
                mediaFormat=format,
                LanguageCode = lang,
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
            return content
    def __str__(self):
        return self.name
