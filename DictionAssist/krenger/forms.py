from django import forms
class inputForm(forms.Form):
    text = forms.CharField(label='Text input', max_length=200,required=True)
    audio = forms.FileField(required=True)
    