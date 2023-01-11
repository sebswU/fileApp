from django import forms
from django.forms import ModelForm
from django.shortcuts import render

class inputForm(ModelForm):
    class Meta:
        text = forms.CharField(max_length=5000)
        audio = forms.FileField()

   