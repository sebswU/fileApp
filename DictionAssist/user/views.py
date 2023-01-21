from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def signin(request):
    """register"""
    
    if request.method!="POST":
        form =UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('krenger:home')
    return render(request,'form.html', {'form':form})
def login_view(request):
    """sign in if already signed up"""
    if request.method!="POST":
        form =AuthenticationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            user = authenticate
            if user is not None:
                login(request, user)
                return redirect('krenger:home')
            else:
                form = AuthenticationForm()
                return render(request, 'form.html',{'form':form})
        return render(request,'login.html',{'form':form})
def logout_view(request):
    logout(request)
    return redirect('user:signup')
def profile_view(request):
    template_name="profile.html"
    return redirect('krenger:home')