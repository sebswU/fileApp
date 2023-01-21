from django.urls import include,path
from django.shortcuts import HttpResponseRedirect
from . import views
from user.views import signin

app_name='user'
urlpatterns=[
    path('',include('django.contrib.auth.urls')),
    path('signup/',views.signin,name='signup')
]