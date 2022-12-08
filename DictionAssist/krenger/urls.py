from django.urls import include, path
from django.shortcuts import render
from krenger.views import Form, Settings, WordArchive
from . import views

app_name='polls'
urlpatterns=[
    path('home/',Form.as_view()),
    path('<str:username>/', Settings.as_view()),
    path('history/',WordArchive.as_view()),
]