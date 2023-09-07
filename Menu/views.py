import json
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Menu.forms import createEmployeeForm
from db.models import Cliente, User, Menu
from authentication.forms import createUserForm
# Create your views here.
def menuIndex(request):
    return render(request, 'Menu/menuIndex.html')

def menuCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    employees = Menu.objects.all()
    if search != "":
        employees = employees.filter(
            Q(nombre__icontains=search) 
        )
    print(employees)

  
    return render(request, "Menu/menuCard.html",{'employees':employees})


def menuEditar(request,id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = createEmployeeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
                print(form)
                user = form.save()
                user.save()

                return redirect("Menu:empleadosIndex")
        else:
                return render(request, 'Menu/editarEmpleado.html',{'form':form, 'user':user})


    form = createEmployeeForm(instance=user)
    print(user)
    return render(request, 'Menu/editarEmpleado.html',{'form':form,'user':user})






def menuCrear(request):
    if request.method == "POST":
        form = createEmployeeForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
            
            user.set_password('Super1')
          
            user.save()

            
            return redirect("Menu:empleadosIndex")
        else:
            return render(request, 'Menu/crearEmpleado.html',{'form':form})
          

    form = createEmployeeForm()

    return render(request, 'Menu/crearEmpleado.html',{'form':form})


def menuEliminar(request,id):
    clientes = User.objects.get(id=id)
    clientes.is_active=False
    clientes.save()
    return redirect("Menu:empleadosIndex")
