from django.http import HttpResponse
from django.shortcuts import redirect, render
from db.models import Cliente
from authentication.forms import createUserForm
# Create your views here.
def ventasIndex(request):
   
    return render(request, 'Ventas/indexVentas.html')

def crearVenta(request):
    
    return HttpResponse("Vendido")

def clientList(request):
    clientes = Cliente.objects.all()
    print(clientes)
    return render(request,'Ventas/clientList.html',{'clientes':clientes})

