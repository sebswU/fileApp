from django.urls import include,path
from django.shortcuts import HttpResponseRedirect
from . import views
from user.views import signin, login_view,logout_view

app_name='user'
urlpatterns=[
    path('',include('django.contrib.auth.urls')),
    path('signup/',views.signin,name='signup'),
    path('login/', views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout')
]