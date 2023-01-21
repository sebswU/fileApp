from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def signin(request):
    """login/register"""
    
    if request.method!="POST":
        form =UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('krenger:home')
    return render(request,'form.html', {'form':form})
def profile(request):
    template_name="profile.html"
    return(request, template_name)