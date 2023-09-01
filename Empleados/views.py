from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Empleados.forms import createEmployeeForm
from db.models import Cliente, User
from authentication.forms import createUserForm
# Create your views here.
def empleadosIndex(request):
    clientes = User.objects.all()
    print(clientes)
    return render(request, 'Empleados/indexEmpleados.html',{'clientes':clientes})

def empleadosEditar(request,id):
    user = User.objects.get(id=id)
    return render(request, 'Empleados/editarEmpleado.html',{'user':user})

def empleadosCrear(request):
        form = createEmployeeForm()
        return render(request, 'Empleados/crearEmpleado.html',{'form':form})
