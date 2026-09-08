
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Corte"

urlpatterns = [
    path('',views.corteDeCajaIndex,name='corteDeCajaIndex'),
    path('enviarCorreo/',views.enviarCorreo,name='enviarCorreo'),
    path('cortesPasados/',views.cortesPasados,name='cortesPasados'),

] 
