from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from krenger.models import Person,TxtRec, WordCard
from krenger.forms import inputForm
from django.urls import reverse
import boto3
import requests
import time
import os
import json
import io
# Create your views here

def view(request):
    """POST function: upload file to s3 bucket, start transcription, go to s3 bucket where aws transcribe saved, get file, compare"""
    model = TxtRec
    form = inputForm()
    if request.method == "POST":
    #TODO:find a way to check if its an audio file
    #TODO: if project is up for OS dev, all vars must be configurable
        fileFormat = "mp3"
        location = "us-east-1"
        s3URI = "s3://webapp2012/"
        lang = "en-US"
        form = inputForm(request.POST, request.FILES)
        data = request.FILES['audio']
        text = request.POST['text']
        #will only process if csrf token and session id is valid
        if form.is_valid():
            #open txt file in 'down' folder and put the inputted text inside
            open(os.path.join(os.path.dirname(__file__),"down/textRef.txt"), 'w').write(text)
            #initiates client connection to Amazon S3
            s3 = boto3.client('s3')
            #get a unique nearest-integer-rounded time in seconds
            Key=f'{int(time.time())}'
            #upload to a hard-coded bucket address for IAM user
            s3.upload_fileobj(data,'webapp2012',f'{Key}.mp3')
            #initiate client connection with AWS Transcribe
            client = boto3.client('transcribe',region_name=location)
            jobName = Key
            #transcribe and save to s3 bucket
            #TODO: add functionality for .webm
            try:
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
            except:
                return HttpResponseNotFound("<h1>file must be in .mp3 or .webm format</h1>")
            #transcription job will take about 20 seconds
            #TODO: make website get length of audio file and put in time.sleep()
            time.sleep(20)
            #download transcript file
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('webapp2012')
            with open(os.path.join(os.path.dirname(__file__),"down/transcript.json"),'wb') as dt:
                try:
                    #returns in binary format but encoding is json
                    bucket.download_fileobj(f'transcription_results/{Key}.json', dt)
                except:
                    #if the same form is submitted twice, the same file 
                    #will be uploaded to AWS twice
                    #there will be a HeadObject error returned
                    return HttpResponseNotFound("<h1>Try reloading the previous page and reentering form</h1>")

            #get the content of the file and then return it
            #aws returns binary format, view must put all binary stuffs in 
            #transcript file and then load via json encoding
            content = json.load(open(os.path.join(os.path.dirname(__file__),"down/transcript.json"),'rb'))
            #content is then set to the actual transcript via json traversal
            content=content['results']['transcripts'][0]['transcript']
            diff = 0
            #diff measures the difference in len() of two strings
            text1 = content
            text2 = text
            #algorithm purpose: detect all of the mispronounced words via iter
            #set all as iterable list
            text1 = text1.split()
            text2 = text2.split()
            #checks if transcript is longer than reference inputted text 
            if len(text1)>len(text2):
                diff = len(text1)-len(text2)
            for i in range(len(text2)):
                #differences in the length of text/transcript is diff variable
                #there could either be stuttering by the user or faulty transcription
                #if the word is not the same, program will rely off of diff variable
                #if diff is 0 and the word is still wrong that means
                #the word is actually mispronounced; i returns to original pos
                #and a word card will be saved in the database
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
                            content = json.loads(requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{text2[i]}").content)
                            w = WordCard.objects.create(name=text2[i],pronunc=content[0]['phonetics'][0]['audio'],textPr=content[0]['phonetic'],define=content[0]['meanings'][0]['definitions'][0]['definition'])
                            w.save()
                            
                            print(f"you did not pronounce {text2[i]} correctly")
                            i-=len(text1)-len(text2)
                        except:
                            raise ValueError
            #take user to the page with the missed words
            return HttpResponseRedirect(reverse('krenger:archive'))           
            
        else:
            form=inputForm();

            #TODO: word cards in detail view
        return render(request,'krenger/templates/index.html',{'form':form})  
    return render(request,'krenger/templates/index.html',{'form':form})

#TODO:decide whether to remove or keep and develop configurations
class Settings(TemplateView):
    template_name = 'krenger/templates/user_site.html'
    def view(request, template_name):
        
        if HttpResponseNotFound:
            return HttpResponseNotFound("<h1>Page not found. Try double checking the URL.</h1>")
        else:
            
            model = Person
            return render(request, template_name)
    def __str__(self):
        return self.name
    
class WordCardView(ListView):
    template_name="user_site.html"
    model = WordCard
    context_object_name="db"

    def __str__(self):
        return self.name

