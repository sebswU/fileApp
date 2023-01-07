import boto3
import os
import datetime
import time
from dotenv import load_dotenv
load_dotenv()


def transcribe(self, s3URI, format, lang='en', location="us-east-1"):
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
    return content

