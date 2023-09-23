
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Stock"

urlpatterns = [
    path('',views.stockIndex,name='stockIndex'),
    path('crear/',views.stockCrear,name='stockCrear'),


    path('AjaxSearch', views.stockCard, name='stockCard'),



] 
