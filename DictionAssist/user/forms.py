from django import forms
from django.forms import ModelForm
from .models import user
class loginForm(ModelForm):
    class Meta:
        model=user
        fields=['username','password']
    def __str__(self):
        return self.text