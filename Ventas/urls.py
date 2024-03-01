
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Ventas"

urlpatterns = [
    path('',views.ventasIndex,name='ventasIndex'),
    #path('crear/<int:id>',views.ventasCrear,name='ventasCrear'),
    path('crear/<str:mesa>',views.ventasCrearMesa,name='ventasCrearMesa'),

    path('modificarVenta/<int:id>',views.modificarVenta,name='modificarVenta'),
    #path('modificarVenta/<str:mesa>',views.modificarVenta,name='modificarVenta'),
    path('modificarVenta/agregarPlatillosVenta/<int:id>', views.agregarPlatillosVenta, name='agregarPlatillosVenta'),

    path('agregarVenta/<int:id>',views.agregarVenta,name='agregarVenta'),
    path('cerrarVenta/<int:id>',views.cerrarVenta,name='cerrarVenta'),
    path('abrirVenta/<int:id>',views.abrirVenta,name='abrirVenta'),

    path('ventasTodas/AjaxSearch', views.ventasCard, name='ventasCard'),
    path('modificarVenta/AjaxSearch', views.clienteRow, name='clienteRow'),
    path('modificarVenta/AjaxSearch2', views.menuRow, name='menuRow'),
    path('modificarVenta/AjaxSearch3', views.menuRow2, name='menuRow2'),


    path('modificarVenta/cambiarFactura/<int:id>/',views.cambiarFactura,name='cambiarFactura'),
    path('modificarVenta/guardarCambios/<int:compra_id>/<int:list_id>/<str:operacion>/', views.guardarCambios, name='guardarCambios'),
    path('modificarVenta/Cliente/<int:id>',views.addCliente,name='addCliente'),
    path('modificarVenta/Mesa/<int:id>',views.addMesa,name='addMesa'),
    path('modificarVenta/updateRow/<int:lista>/<int:venta>',views.updateRow,name='updateRow'),
    path('modificarVenta/updateRow2/<int:list>/',views.updateRow2,name='updateRow2'),
    path('modificarVenta/ticket2/<int:venta>/',views.ticketRead,name='ticketRead'),

    path('modificarVenta/ticket/<int:venta>',views.ticket,name='ticket'),

    path('ventasTodas/',views.ventasTodas,name='ventasTodas'),

] 
