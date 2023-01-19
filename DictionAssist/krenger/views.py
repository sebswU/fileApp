from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView, DetailView,DayArchiveView
from krenger.models import Person,TxtRec, WordCard
from krenger.forms import inputForm
from django.urls import reverse
import boto3
import requests
import time
import os
import json
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
        s3URI = "s3://webapp2012/"
        lang = "en-US"
        form = inputForm(request.POST, request.FILES)
        data = request.FILES['audio']
        text = request.POST['text']
        if form.is_valid():

            open(os.path.join(os.path.dirname(__file__),"down/textRef.txt"), 'w').write(text)
            print(data.chunks())
            s3 = boto3.client('s3')
            Key=f'{int(time.time())}'

            s3.upload_fileobj(data,'webapp2012',f'{Key}.mp3')
            
            client = boto3.client('transcribe',region_name=location)
            jobName = Key
            #transcribe and save to s3 bucket
            client.start_transcription_job(
                TranscriptionJobName = jobName,
                Media={
                    'MediaFileUri': s3URI+Key+'.mp3'
                },
                MediaFormat=fileFormat,
                LanguageCode = lang,
                OutputBucketName = 'webapp2012',
                OutputKey = 'transcription_results/'
            )
            #transcription job will take about 20 seconds
            time.sleep(20)
            #download transcript file
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('webapp2012')
            with open(os.path.join(os.path.dirname(__file__),"down/transcript.json"),'wb') as dt:
                try:
                    bucket.download_fileobj(f'transcription_results/{Key}.json', dt)
                except:
                    return HttpResponseNotFound("<h1>Try reloading the previous page and reentering form</h1>")

            #get the content of the file and then return it
            content = json.load(open(os.path.join(os.path.dirname(__file__),"down/transcript.json"),'rb'))
            content=content['results']['transcripts'][0]['transcript']
            stutterBool = False
            diff = 0
            #measure the difference in two strings
            text1 = content
            text2 = text

            text1 = text1.split()
            text2 = text2.split()
            if len(text1)>len(text2):
                diff = len(text1)-len(text2)
            for i in range(len(text2)):
                #differences in the length of text/transcript accounted for
                if text1[i]!=text2[i]: 
                    while diff!=0:
                        if text1[i] == text2[i+1]:
                            i+=1
                            break
                        else:
                            diff-=1
                            i+=1
                    if diff==0:
                        try:
                            content = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{text2[i]}").content
                            w = WordCard(word=text2[i],pronunc=content[0]['phonetics'][0]['audio'],textPronunc=content[0]['phonetic'],define=content[0]['meanings'][0]['definitions'][0]['definition'])
                            w.save()
                            
                            print(f"you did not pronounce {text2[i]} correctly")
                            i-=len(text1)-len(text2)
                        except:
                            raise ValueError
            #take user to the page with the missed words
            return HttpResponseRedirect(reverse('krenger:archive'))           
            
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
    
class WordArchive(DetailView):
    template_name = 'krenger/templates/words.html'
    def view(request, template_name):
        
        if HttpResponseNotFound:#TODO: change this to an actual condition abt http errors
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.</h1>")
        else:
            
            model = WordCard
            return render(request,template_name,context={'db':model})
    
    
    def __str__(self):
        return self.name

#'Traceback (most recent call last):\n  File "/Users/sebastianwu/.vscode/extensions/ms-python.python-2022.8.1/pythonFiles/lib/python/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_resolver.py", line 192, in _get_py_dictionary\n    attr = getattr(var, name)\n  File "/opt/homebrew/lib/python3.10/site-packages/django/core/files/utils.py", line 37, in <lambda>\n    encoding = property(lambda self: self.file.encoding)\nAttributeError: \'_io.BytesIO\' object has no attribute \'encoding\'\n'