
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Empleados"

urlpatterns = [
    path('',views.empleadosIndex,name='empleadosIndex'),
    path('<int:id>',views.empleadosEditar,name='empleadosEditar'),




] 
