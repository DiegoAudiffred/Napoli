
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Compras"

urlpatterns = [
    path('',views.indexCompras,name='indexCompras'),
    path('compraCrear/',views.compraCrear,name='compraCrear'),
    path('compraEditar/<int:id>',views.compraEditar,name='compraEditar'),
    path('compraEditar/agregarCompra/<int:id>',views.agregarCompra,name='agregarCompra'),
    path('compraEditar/cerrarCompra/<int:id>',views.cerrarCompra,name='cerrarCompra'),
    path('compraEditar/agregarCompraCodigo/<int:id>',views.agregarCompraCodigo,name='agregarCompraCodigo'),
    path('compraEditar/guardarCambios/<int:compra_id>/<int:list_id>/<str:operacion>/', views.guardarCambios, name='guardarCambios'),
    path('AjaxSearch2', views.comprasCard, name='comprasCard'),
]