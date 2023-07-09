from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from db.models import Cliente, User
from authentication.forms import createUserForm
# Create your views here.
def empleadosIndex(request):
    clientes = User.objects.all()
    print(clientes)
    return render(request, 'Empleados/indexEmpleados.html',{'clientes':clientes})

