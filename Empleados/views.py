import json
from django.shortcuts import render
from django.db.models import Q
from django.templatetags.static import static
from django.contrib.auth import update_session_auth_hash

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Empleados.forms import createEmployeeForm, modifyEmployeeForm
from db.models import Cliente, User
from authentication.forms import createUserForm
# Create your views here.
from django.contrib.auth.decorators import user_passes_test,login_required


@login_required(login_url='authentication:login')

def empleadosIndex(request):
    form = createEmployeeForm()

    return render(request, 'Empleados/indexEmpleados.html',{'form':form})

def employeeCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    employees = User.objects.filter(is_active=True)
    if search != "":
        employees = employees.filter(
            Q(first_name__icontains=search) 
        )
    print(employees)

  
    return render(request, "Empleados/empleadoCard.html",{'employees':employees})

@login_required(login_url='authentication:login')

def empleadosEditar(request,id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = modifyEmployeeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
                print(form)
                nueva_contraseña = request.POST['nueva_contraseña']
                user.set_password(nueva_contraseña)
                user = form.save()
                user.save()
                update_session_auth_hash(request, user)

                return redirect("Empleados:empleadosIndex")
        else:
                return render(request, 'Empleados/editarEmpleado.html',{'form':form, 'user':user})


    form = modifyEmployeeForm(instance=user)
    print(user)
    return render(request, 'Empleados/editarEmpleado.html',{'form':form,'user':user})


def recuperarContra(request,id):
    user = User.objects.get(id=id)
    user.set_password('Super12345')
    user.save()
    return redirect("Empleados:empleadosIndex")



@login_required(login_url='authentication:login')

def empleadosCrear(request):
    if request.method == "POST":
        form = createEmployeeForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
            img = static('img/fondogris.PNG')
            user.url = img
            user.set_password('super')
          
            user.save()
            
            return redirect("Empleados:empleadosIndex")
        else:
            print("Valio")
            print(form.errors)
            return render(request, 'Empleados/indexEmpleados.html',{'form':form})
          


@login_required(login_url='authentication:login')

def empleadosEliminar(request,id):
    clientes = User.objects.get(id=id)
    clientes.is_active=False
    clientes.save()
    return redirect("Empleados:empleadosIndex")
