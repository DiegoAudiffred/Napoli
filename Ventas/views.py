import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from Ventas.forms import VentaMenuForm, createVentaForm, modifyMesaForm, modifyVentaForm
from db.models import Cliente, Menu, Mesa, User, Venta, VentaMenu
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test,login_required


def isAdmin(user):
    if user.rol == 'Admin':
        return True
    else:
        return False
    


@login_required(login_url='authentication:login')
# Create your views here.
def ventasIndex(request):
    form = createVentaForm()
    form2 = modifyVentaForm()
    form3 = modifyMesaForm()
    ventas = Venta.objects.filter(is_open=True).order_by('-fecha_compra')
    user = request.user

    return render(request, 'Ventas/indexVentas.html',{'form':form,'ventas':ventas,'form2':form2,'form3':form3,'user':user})

@login_required(login_url='authentication:login')

def addCliente(request,id):
    venta = Venta.objects.get(id=id)
    if request.method == 'POST':
        form = modifyVentaForm(request.POST, instance=venta)  # Inicializar el formulario con los datos POST
        if form.is_valid():
            user = form.save()
            user.save()
        else:
            return redirect('Ventas:modificarVenta',id)

    return redirect('Ventas:modificarVenta',id)


def addMesa(request,id):
    venta = Venta.objects.get(id=id)
    print(venta)
    if request.method == 'POST':
        form = modifyMesaForm (request.POST, instance=venta)  # Inicializar el formulario con los datos POST
        if form.is_valid():
            user = form.save()
            user.save()
        else:
            print(form.errors)
            return redirect('Ventas:modificarVenta',id)

    return redirect('Ventas:modificarVenta',id)

def addRow(request, id):
    venta = Venta.objects.get(id=id)
  

    nueva_mesa = 'Para llevar' 

    response_data = {'mensaje': 'Actualización exitosa'}
   
    
    return JsonResponse(response_data)


def clienteRow(request):
    
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    clientes = Cliente.objects.filter(is_active=True)
    if search != "":
        clientes = clientes.filter(
            Q(nombre__icontains=search) 
        )
    return render(request, "Ventas/clienteRow.html",{'clientes':clientes})


def menuRow(request):
    
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
 
    menus = Menu.objects.all()
    if search != "":
        menus = menus.filter(
            Q(nombre__icontains=search) 
        )
    print(menus)
    return render(request, "Ventas/menuRow.html",{'menus':menus})


def menuRow2(request):
    
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
 
    menus = Menu.objects.filter(categoria='Pizza')
    if search != "":
        menus = menus.filter(
            Q(nombre__icontains=search) 
        )

    return render(request, "Ventas/menuRow2.html",{'menus':menus})

@login_required(login_url='authentication:login')

def modificarVenta(request,id):
    venta = Venta.objects.get(id=id)
    lista = VentaMenu.objects.filter(venta=id)
    mesas = Mesa.objects.all()
  

    user = request.user
    total = 0
    total2 = 0
    for ventas in lista:
        if ventas.menu.categoria == "Pizza":
            if ventas.familiar:
                if ventas.pizza_mitad:
                    if ventas.pizza_mitad.precioFamiliar < ventas.menu.precioFamiliar:
                        total += (ventas.menu.precioFamiliar) * ventas.cantidad
                    else:
                        total += (ventas.pizza_mitad.precioFamiliar) * ventas.cantidad
                else:
                    total += (ventas.menu.precioFamiliar) * ventas.cantidad
            else:
                if ventas.pizza_mitad:
                    if ventas.pizza_mitad.precio < ventas.menu.precio:
                        total += (ventas.menu.precio) * ventas.cantidad
                    else:
                        print(ventas.pizza_mitad.precio)
                        print(ventas.cantidad)

                        total += (ventas.pizza_mitad.precio) * ventas.cantidad
                else:
                        total += (ventas.menu.precio) * ventas.cantidad
        else:        
            if ventas.media_orden:
                total += ventas.menu.mediaOrden* ventas.cantidad
            else:
                total += (ventas.menu.precio) * ventas.cantidad

            
            
            
            
        if ventas.extras:
            if ventas.familiar:
                for venti in ventas.extras.all():
                    total += venti.precioFamiliar * ventas.cantidad
            else:
                for venti in ventas.extras.all():
                    total += venti.precio * ventas.cantidad
            
            
  
        
            
        ventas.totalfinal = total
        total2 = total2 + total
      
        total = 0
        ventas.save()
        
        
    venta.total = total2
    venta.save()
    
    form = modifyVentaForm(instance=venta)
    form2 = VentaMenuForm()
    form3 = modifyMesaForm()

    return render(request, 'Ventas/modificarVentas.html',{'venta':venta,'lista':lista,'form':form,'form2':form2,'form3':form3,'total':total2,'user':user,'mesas':mesas})



@login_required(login_url='authentication:login')

def cerrarVenta(request,id):
    venta = Venta.objects.get(id=id)
    cliente = venta.cliente
    lista = VentaMenu.objects.filter(venta=id)
    total = 0
    for ventas in lista:
        total += (ventas.menu.precio) * ventas.cantidad
    

    if venta.is_reopen == False:
        cliente.total_compras +=  1
        cliente.total_gastado += total
    venta.total= total
    venta.save()

    cliente.save()
    venta.is_reopen = True
    venta.is_open= False
    venta.save()
    
    
    return redirect('Ventas:ventasIndex')
@login_required(login_url='authentication:login')

def abrirVenta(request,id):
    venta = Venta.objects.get(id=id)
    venta.is_open= True
    if not venta.is_reopen:
        venta.is_reopen= True
  

    venta.save()
    return redirect('Ventas:ventasIndex')




@login_required(login_url='authentication:login')

def agregarVenta(request,id):
    
    ventas = Venta.objects.get(id=id)

    if request.method == "POST":
        form = VentaMenuForm(request.POST, request.FILES)
        if form.is_valid():            
            form.instance.venta = ventas

            user = form.save()
            user.save()
                      
            return redirect("Ventas:modificarVenta",id)
        else:
            print(form.errors)
            return redirect("Ventas:ventasIndex")
   
    return redirect("Ventas:ventasIndex")
@login_required(login_url='authentication:login')

def ventasCrear(request,id):
    if request.method == "POST":
        form = createVentaForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.empleado = User.objects.get(id=id)
            user.cliente = Cliente.objects.get(id=1)

            user.is_open = True
            user.save()
                      

            
            return redirect("Ventas:ventasIndex")
        else:
            return render(request, 'Ventas/ventasIndex.html',{'form':form})
          

    form = createVentaForm()

    return redirect("Ventas:ventasIndex")
@login_required(login_url='authentication:login')

def ventasTodas(request):



    return render(request, 'Ventas/ventasTodas.html',)

def ventasCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    fecha = jsonObject["date"]
   
    
    ventas = Venta.objects.filter(is_open=False).order_by('-fecha_compra')

    if fecha != "":
        if fecha != "" :
            date = fecha.split("/")
            start_dt = datetime(int(date[2]), int(date[1]), int(date[0]))
            ventas = ventas.filter(
                Q(fecha_compra__date=start_dt)  
            )


                
    return render(request, "Ventas/ventasCard.html",{'ventas':ventas})

@login_required(login_url='authentication:login')
def guardarCambios(request,compra_id,list_id,operacion):
   
    compras = Venta.objects.get(id=compra_id)
    producto = VentaMenu.objects.get(venta=compras,id=list_id)
    
    if operacion == "suma":
        
        producto.cantidad = producto.cantidad + 1
        producto.save()

    else:
        
    
   
        if producto.cantidad > 0:
            producto.cantidad = producto.cantidad - 1
            
            producto.save()
            if producto.cantidad == 0:
                producto.delete()
   
       

        
        
    
    return redirect("Ventas:modificarVenta",compra_id)
@login_required(login_url='authentication:login')

def cambiarFactura(request,id):
        compras = Venta.objects.get(id=id)
        if compras.bool_factura == True:
            compras.bool_factura = False
            compras.save()
        else:
            compras.bool_factura = True
            compras.save()

        return redirect("Ventas:modificarVenta",id)
