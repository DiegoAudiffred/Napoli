
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Stock"

urlpatterns = [
    path('',views.stockIndex,name='stockIndex'),
    path('crear/',views.stockCrear,name='stockCrear'),
    path('compraCrear/',views.compraCrear,name='compraCrear'),
    path('compraEditar/<int:id>',views.compraEditar,name='compraEditar'),
    path('compraEditar/agregarCompra/<int:id>',views.agregarCompra,name='agregarCompra'),

    path('AjaxSearch', views.stockCard, name='stockCard'),
    path('AjaxSearch2', views.comprasCard, name='comprasCard'),


] 
