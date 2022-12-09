from django.urls import include, path

from . import views#TODO:clarify URL Patterns
from kranger.views import FormView

app_name = 'polls'
urlpatterns = [
    path('', views.index),
    path('<str:username>/', views.index),
]