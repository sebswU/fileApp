from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from krenger.models import Person,TxtRec, WordCard
from krenger.forms import inputForm
from django.urls import reverse
import boto3
import requests
import time
import os
import json
import io
import wave


# Create your views here
@login_required
def view(request):
    """
    POST function: upload file to s3 bucket, 
    start transcription, go to s3 bucket where 
    aws transcribe saved, get file, compare
    """
    model = TxtRec
    form = inputForm()
    if request.method == "POST":
    #TODO:find a way to check if its an audio file
    #TODO: if project is up for OS dev, all vars must be configurable
        
        location = "us-east-1"
        s3URI = "s3://webapp2012/"
        lang = "en-US"
        form = inputForm(request.POST, request.FILES)
        data = request.FILES['audio']
        text = request.POST['text']
        fileFormat = "mp3"
        if data.content_type == 'video/webm':
            fileFormat = "webm"

        #will only process if csrf token and session id is valid
        if form.is_valid():
            #open txt file in 'down' folder and put the inputted text inside
            open(os.path.join(os.path.dirname(__file__),"down/textRef.txt"), 'w').write(text)
            #initiates client connection to Amazon S3
            s3 = boto3.client('s3')
            #get a unique nearest-integer-rounded time in seconds
            Key=f'{int(time.time())}'
            #upload to a hard-coded bucket address for IAM user
            s3.upload_fileobj(data,'webapp2012',f'{Key}.{fileFormat}')
            #initiate client connection with AWS Transcribe
            client = boto3.client('transcribe',region_name=location)
            jobName = Key

            #transcribe and save to s3 bucket
            try:
                client.start_transcription_job(
                    TranscriptionJobName = jobName,
                    Media={
                        'MediaFileUri': s3URI+Key+'.'+fileFormat
                    },
                    MediaFormat=fileFormat,
                    LanguageCode = lang,
                    OutputBucketName = 'webapp2012',
                    OutputKey = 'transcription_results/'
                )
            except:
                return HttpResponseNotFound("<h1>file must be in .mp3 or .webm format</h1>")
            
            #transcription job will take about 20 seconds
            #TODO: send a signal for React to get the website to wait for the transcription
            time.sleep(20)
            #download transcript file
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('webapp2012')
            with open(os.path.join(os.path.dirname(__file__),"down/transcript.json"),'wb') as dt:
                try:
                    #returns in binary format but data is encoded in json
                    bucket.download_fileobj(f'transcription_results/{Key}.json', dt)
                except:
                    #wait an extra 5 seconds and redo if transcript not present on first try
                    time.sleep(5)
                    try:
                        bucket.download_fileobj(f'transcription_results/{Key}.json', dt)
                    except:
                    #if that doesn't work then print out the AWS inconvenience page
                        return HttpResponseNotFound("<h1>Audio should be <= 5 seconds</h1>")

            #get the content of the file and then return it
            #aws returns binary format, view must put all binary stuffs in 
            #transcript file and then load via json encoding
            content = json.load(open(os.path.join(os.path.dirname(__file__),"down/transcript.json"),'rb'))
            #content is then set to the actual transcript via json traversal
            content=content['results']['transcripts'][0]['transcript']
            diff = 0
            #diff measures the difference in len() of two strings

            #algorithm purpose: detect all of the mispronounced words via iter
            #set all as iterable list
                #take out punctuation that can interfere
                #with the dictionary API calls
            content = content.split()
            text = text.split()
            for j in content:
                j.replace('!','')
                j.replace('?','')
                j.replace('.','')
                j.replace(',','')
            for j in text:
                j.replace('!','')
                j.replace('?','')
                j.replace('.','')
                j.replace(',','')
                
            #split text into string for iteration
            
            #checks if transcript is longer than reference inputted text
            # or vv: longer one set to one, shorter set to short
            # if not then just set variables to whatever 
            if len(content)>len(text):
                diff = len(content)-len(text)
                longStr = content
                shortStr = text
            elif len(content)<len(text):
                diff = len(text)-len(content)
                longStr = text
                shortStr = content
            else:
                longStr = content
                shortStr = text

            for i in range(len(shortStr)):
                #first, everything changes to lowercase
                #differences in the length of text/transcript is diff variable
                #there could either be stuttering by the user or faulty transcription
                #if the word is not the same, program will rely off of diff variable
                #if diff is 0 and the word is still wrong that means
                #the word is actually mispronounced; i returns to original pos
                #and a word card will be saved in the database
                longStr[i] = longStr[i].lower()
                shortStr[i] = shortStr[i].lower()
                if longStr[i]!=shortStr[i]: 
                    while diff!=0:
                        if longStr[i] == shortStr[i+1]:
                            i+=1
                            break
                        else:
                            diff-=1
                            i+=1
                    if diff==0:
                        try:
                            content = json.loads(requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{shortStr[i]}").content)
                            w = WordCard.objects.create(name=shortStr[i],
                                                        pronunc=content[0]['phonetics'][0]['audio'],
                                                        textPr=content[0]['phonetic'],
                                                        define=content[0]['meanings'][0]['definitions'][0]['definition'],
                                                        user=request.user)
                            w.save()
                            
                            print(f"you did not pronounce {shortStr[i]} correctly")
                            i-=len(longStr)-len(shortStr)
                        except:
                            return HttpResponseRedirect(reverse("user:signup"))
            #take user to the page with the missed words
            return HttpResponseRedirect(reverse('krenger:archive'))           

    return render(request,'krenger/templates/index.html',{'form':form, 'user':request.user.username})

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
    model = WordCard
    template_name="krenger/templates/wordcard_list.html"
    def get_queryset(self):
        try:
            #search for words for the specific user
            return WordCard.objects.filter(user=self.request.user)
        except:
            return HttpResponseRedirect(reverse('user:signup'))
    #debugging method: rewrite the view again and pay attention to 
    #documentation

    def __str__(self):
        return self.name

