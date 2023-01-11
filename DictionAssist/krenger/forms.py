from django import forms

class inputForm(forms.Form):
    text = forms.CharField(max_length=5000)
    audio = forms.FileField()
    def __str__(self):
        return self.text