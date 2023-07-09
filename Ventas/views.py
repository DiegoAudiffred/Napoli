from django.http import HttpResponse
from django.shortcuts import redirect, render
from db.models import *
from authentication.forms import createUserForm
# Create your views here.
def ventasIndex(request):
   
    return render(request, 'Ventas/indexVentas.html')

def crearVenta(request):
    
    return HttpResponse("Vendido")