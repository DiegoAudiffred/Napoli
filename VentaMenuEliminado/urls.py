
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="VentaMenuEliminado"

urlpatterns = [
    path('',views.VentaMenuEliminadoIndex,name='VentaMenuEliminadoIndex'),


] 
