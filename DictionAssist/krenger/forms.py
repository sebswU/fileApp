from django import forms
from django.forms import ModelForm
from django.shortcuts import render

<<<<<<< HEAD
class inputForm(forms.Form):
    text = forms.CharField(max_length=5000)
    audio = forms.FileField()
    def __str__(self):
        return self.text
=======
class inputForm(ModelForm):
    class Meta:
        text = forms.CharField(max_length=5000)
        audio = forms.FileField()

   
>>>>>>> d2c730e375610cbb26386ebe26f13d98630e163b
