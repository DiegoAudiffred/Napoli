import json
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Menu.forms import createMenuForm
from db.models import Cliente, User, Menu
# Create your views here.
from django.templatetags.static import static

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


def menuEditar(request, id):
    try:
        platillo = Menu.objects.get(id=id)
    except Menu.DoesNotExist:
        # Si el objeto Menu con el id dado no existe, redirigir o manejar el error según sea necesario
        return redirect("ruta_a_tu_vista_de_error")

    if request.method == "POST":
        form = createMenuForm(request.POST, request.FILES, instance=platillo)
        if form.is_valid():
            try:
                platillo = form.save()
            except ValidationError as e:
                # Imprimir el error en la consola
                print("Error al guardar el platillo:", e)
                # Puedes agregar código para manejar el error aquí, como mostrar un mensaje de error al usuario
                return render(request, 'ruta_a_tu_plantilla_de_error', {'error_message': e})
            return redirect("Menu:menuIndex")
        else:
            # Si hay errores en el formulario, imprimirlos en la consola
            print("Errores en el formulario:", form.errors)
            # Puedes agregar código para manejar los errores del formulario aquí, como mostrar los errores al usuario
            return render(request, 'Menu/menuEditar.html', {'form': form, 'platillo': platillo})
    else:
        form = createMenuForm(instance=platillo)
        return render(request, 'Menu/menuEditar.html', {'form': form, 'platillo': platillo})






@login_required(login_url='authentication:login')

def menuCrear(request):
    if request.method == "POST":
        form = createMenuForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            if not user.url:
                       
                img = static('img/noimage.jpg')
                user.url = img

            user.save()
                      

            
            return redirect("Menu:menuIndex")
        else:
            print(form.errors)
            return render(request, 'Menu/crearIndex.html',{'form':form})
          

    form = createMenuForm()

    return redirect("Menu:menuIndex")

@login_required(login_url='authentication:login')

def menuEliminar(request,id):
    clientes = User.objects.get(id=id)
    clientes.is_active=False
    clientes.save()
    return redirect("Menu:empleadosIndex")
