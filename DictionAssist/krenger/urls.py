from django.urls import include, path
from django.shortcuts import render
from krenger.views import view, Settings, WordArchive
from . import views

app_name='krenger'
urlpatterns=[
    path('home/',views.view, name='home'),#name={namespace}
    path('<str:username>/', Settings.as_view(),name='user_settings'),
    path('history/',WordArchive.as_view(),name='archive'),
]
#namespace url format: {% url {app_name}:{namespace} {**context_obj} %}