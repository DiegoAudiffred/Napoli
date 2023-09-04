
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Clientes"

urlpatterns = [
    path('',views.clientesIndex,name='clientesIndex'),
    path('<int:id>',views.clientesEditar,name='clientesEditar'),
    path('crear/',views.clientesCrear,name='clientesCrear'),
    path('AjaxSearch', views.clientsCard, name='clientsCard'),
    path('Eliminar/<int:id>',views.clientesEliminar,name='clientesEliminar'),



] 
