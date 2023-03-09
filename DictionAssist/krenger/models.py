from django.db import models
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
# Create your models here.
class TxtRec(models.Model):
    text = models.CharField(max_length=5000)
    audio = models.FileField()

    def __str__(self):
        return self.name

class WordCard(models.Model):
    name = models.CharField(max_length=100)
    pronunc = models.FileField()
    textPr = models.CharField(max_length=5120)
    define = models.CharField(max_length = 1000)
    #foreign key is to user profile as char is to string/char
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=False)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=50)    
    words = models.ManyToManyField(WordCard)
    recs = models.ManyToManyField(TxtRec)
    #groups = models.ManyToManyField(WordCard)
    
    def __str__(self):
        return self.name

