
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="authentication"

urlpatterns = [
    path('',views.index,name='index'),
    path('createAccount/',views.createAccount,name='createAccount')


] 
