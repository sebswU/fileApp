from django.db import models
from django.forms import ModelForm
# Create your models here.
class TxtRec(models.Model):
    text = models.CharField(max_length=5000)
    audio = models.FileField()

    def __str__(self):
        return self.name

class WordCard(models.Model):
    word = models.CharField(max_length=100)
    pronunc = models.FileField()
    textPr = models.CharField(max_length=5120)
    define = models.CharField(max_length = 1000)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=50)    
    words = models.ManyToManyField(WordCard)
    recs = models.ManyToManyField(TxtRec)
    #groups = models.ManyToManyField(WordCard)
    
    def __str__(self):
        return self.name
class inputForm(ModelForm):
    class Meta:
        model=TxtRec
        fields=['text','audio']

#TODO: test if working with the MW API and AWS 