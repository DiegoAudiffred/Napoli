import json
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Menu.forms import createMenuForm
from db.models import Cliente, User, Menu
# Create your views here.

from django.contrib.auth.decorators import user_passes_test,login_required


@login_required(login_url='authentication:login')

def menuIndex(request):
    form = createMenuForm()

    return render(request, 'Menu/menuIndex.html',{'form':form})

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

@login_required(login_url='authentication:login')

def menuEditar(request,id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = createMenuForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
                print(form)
                user = form.save()
                user.save()

                return redirect("Menu:empleadosIndex")
        else:
                return render(request, 'Menu/editarEmpleado.html',{'form':form, 'user':user})


    form = createMenuForm(instance=user)
    print(user)
    return render(request, 'Menu/editarEmpleado.html',{'form':form,'user':user})





@login_required(login_url='authentication:login')

def menuCrear(request):
    if request.method == "POST":
        form = createMenuForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
                      
            user.save()

            
            return redirect("Menu:menuIndex")
        else:
            return render(request, 'Menu/crearIndex.html',{'form':form})
          

    form = createMenuForm()

    return redirect("Menu:menuIndex")

@login_required(login_url='authentication:login')

def menuEliminar(request,id):
    clientes = User.objects.get(id=id)
    clientes.is_active=False
    clientes.save()
    return redirect("Menu:empleadosIndex")
