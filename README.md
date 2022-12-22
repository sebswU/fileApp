# zhEng
App that demonstrates audio speech recognition and gives feedback on developing language learners' lexical dictionary

# What Users Do:
Users input an audio file of an enunciation into the dropbox. Below the dropbox is a text field in which they are to submit the text version of the enunciation.
Users are responsible for making sure that all words are identifiable using a published dictionary (no slang terms or abbreviations).
If they want to save a group of vocabulary words for further reference, they may sign up for an account.

# What this Web App (Will Be Doing):
Takes the audio and text input as a form to be passed to an AWS Transcribe service. Based on the transcribed word identity and the confidence score given by the service, 
the app will return cards of all the words that have not been transcribed confidently or accurately, using the Merriam-Webster Dictionary API for audio pronounciations 
and definitions.
