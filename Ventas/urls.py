
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Ventas"

urlpatterns = [
    path('',views.ventasIndex,name='ventasIndex'),
    path('crear/',views.ventasCrear,name='ventasCrear'),
    path('modificarVenta/<int:id>',views.modificarVenta,name='modificarVenta'),

    path('cerrarVenta/<int:id>',views.cerrarVenta,name='cerrarVenta'),


] 
