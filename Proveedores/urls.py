
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Proveedores"

urlpatterns = [
    path('',views.proveedoresIndex,name='proveedoresIndex'),



] 
