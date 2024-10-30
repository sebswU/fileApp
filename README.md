# zhEng
App that demonstrates audio speech recognition and gives feedback on developing language learners' lexical dictionary

# Setup
- `git clone` the repository
- navigate to the zheng folder and run `pip install -r requirements.txt`
- 

# What Users Do:
Users input an audio file of an enunciation into the dropbox. Below the dropbox is a text field in which they are to submit the text version of the enunciation.
Users are responsible for making sure that all words are identifiable using a published dictionary (no slang terms or abbreviations).
If they want to save a group of vocabulary words for further reference, they may sign up for an account.

# What this Web App Does:
Takes the audio and text input as a form to be passed to an AWS Transcribe service. Based on the transcribed word identity and the confidence score given by the service, 
the app will return cards of all the words that have not been transcribed confidently or accurately, using the Free Dictionary API for audio pronounciations 
and definitions.
# Tech Used:
- Django (Backend processes, routing, views, authentication)
- Bootstrap (Styling the UI)
- AWS boto3 module (S3 and Transcribe services)
- Free Dictionary API (Get info and audio pronunciation of mispronounced word)
- requests module (Used to make REST calls)

