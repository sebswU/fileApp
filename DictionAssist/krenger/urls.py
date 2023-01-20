from django.urls import include, path
from django.shortcuts import render
from krenger.views import view, Settings, WordCardView
from . import views

app_name='krenger'
urlpatterns=[
    path('home/',views.view, name='home'),#name={namespace}
    path('history/',WordCardView.as_view(),name='archive'),
    path('<str:username>/', Settings.as_view(),name='user_settings'),
    
]
#namespace url format: {% url {app_name}:{namespace} {**context_obj} %}