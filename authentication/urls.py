
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="authentication"

urlpatterns = [
    path('', include('django.contrib.auth.urls'), name="login"),

    path('index',views.index,name='index'),
    path('signout',views.signout,name='signout'),

    path('signin',views.signin, name="signin"),

] 
