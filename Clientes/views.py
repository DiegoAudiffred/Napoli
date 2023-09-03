import json
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Clientes.forms import createClientForm
from db.models import Cliente, User
from authentication.forms import createUserForm
# Create your views here.

# Create your views here.
def clientesIndex(request):
    clientes = Cliente.objects.all()
    return render(request, 'Clientes/indexClientes.html',{'clientes':clientes})


def clientsCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    employees = Cliente.objects.all()
    if search != "":
        employees = employees.filter(
            Q(first_name__icontains=search) 
        )

  
    return render(request, "Clientes/clienteCard.html",{'employees':employees})


def clientesEditar(request,id):
    user = Cliente.objects.get(id=id)
    if request.method == "POST":
        form = createClientForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
                user = form.save()
                user.save()

                return redirect("Clientes:clientesIndex")
        else:
                return render(request, 'Clientes/editarCliente.html',{'form':form, 'user':user})


    form = createClientForm(instance=user)
    print(user)
    return render(request, 'Clientes/editarCliente.html',{'form':form,'user':user})






def clientesCrear(request):
    if request.method == "POST":
        form = createClientForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
            


            
            return redirect("Clientes:clientesIndex")
        else:
            return render(request, 'Clientes/crearCliente.html',{'form':form})
          

    form = createClientForm()

    return render(request, 'Clientes/crearCliente.html',{'form':form})


