import json
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Empleados.forms import createEmployeeForm
from db.models import Cliente, User
from authentication.forms import createUserForm
# Create your views here.
def empleadosIndex(request):
    empleados = User.objects.all()
    return render(request, 'Empleados/indexEmpleados.html',{'empleados':empleados})

def employeeCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    employees = User.objects.all()
    if search != "":
        employees = employees.filter(
            Q(first_name__icontains=search) 
        )
    print(employees)

  
    return render(request, "Empleados/empleadoCard.html",{'employees':employees})


def empleadosEditar(request,id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = createEmployeeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
                user = form.save()
                user.save()

                return redirect("Empleados:empleadosIndex")
        else:
                return render(request, 'Empleados/editarEmpleado.html',{'form':form, 'user':user})


    form = createEmployeeForm(instance=user)
    print(user)
    return render(request, 'Empleados/editarEmpleado.html',{'form':form,'user':user})






def empleadosCrear(request):
    if request.method == "POST":
        form = createEmployeeForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
            
            user.set_password('Super1')
          
            user.save()

            
            return redirect("Empleados:empleadosIndex")
        else:
            return render(request, 'Empleados/crearEmpleado.html',{'form':form})
          

    form = createEmployeeForm()

    return render(request, 'Empleados/crearEmpleado.html',{'form':form})


