
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="Menu"

urlpatterns = [
    path('',views.menuIndex,name='menuIndex'),
    path('<int:id>',views.menuEditar,name='menuEditar'),
    path('crear/',views.menuCrear,name='menuCrear'),
    path('AjaxSearch', views.menuCard, name='menuCard'),
    path('Eliminar/<int:id>',views.menuEliminar,name='menuEliminar'),



] 
