
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Ventas"

urlpatterns = [
    path('',views.ventasIndex,name='ventasIndex'),
    path('crear/<int:id>',views.ventasCrear,name='ventasCrear'),
    path('modificarVenta/<int:id>',views.modificarVenta,name='modificarVenta'),
    path('agregarVenta/<int:id>',views.agregarVenta,name='agregarVenta'),
    path('cerrarVenta/<int:id>',views.cerrarVenta,name='cerrarVenta'),
    path('ventasTodas/AjaxSearch', views.ventasCard, name='ventasCard'),
    path('modificarVenta/AjaxSearch', views.clienteRow, name='clienteRow'),

    path('ventasTodas/',views.ventasTodas,name='ventasTodas'),

] 
