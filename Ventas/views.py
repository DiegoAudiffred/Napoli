import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Ventas.forms import VentaMenuForm, addClienteForm, createVentaForm, modifyVentaForm
from db.models import Cliente, User, Venta, VentaMenu
from django.db.models import Q
# Create your views here.
def ventasIndex(request):
    form = createVentaForm()
    form2 = modifyVentaForm()
    ventas = Venta.objects.filter(is_open=True).order_by('-fecha_compra')
    user = request.user

    return render(request, 'Ventas/indexVentas.html',{'form':form,'ventas':ventas,'form2':form2,'user':user})


def addCliente(request,id):
    venta = Venta.objects.get(id=id)
    print(venta)
    if request.method == 'POST':
        form = modifyVentaForm(request.POST, instance=venta)  # Inicializar el formulario con los datos POST
        if form.is_valid():
            print("Aqui Si")
            user = form.save()
            user.save()
        else:
            print("Aqui No")
            return redirect('Ventas:modificarVenta',id)

    return redirect('Ventas:modificarVenta',id)




def clienteRow(request):
    
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    clientes = Cliente.objects.filter(is_active=True)
    if search != "":
        clientes = clientes.filter(
            Q(nombre__icontains=search) 
        )
    return render(request, "Ventas/clienteRow.html",{'clientes':clientes})


def modificarVenta(request,id):
    venta = Venta.objects.get(id=id)
    lista = VentaMenu.objects.filter(venta=id)

    user = request.user
    total = 0
    for ventas in lista:
        total += (ventas.menu.precio) * ventas.cantidad
    
    for ven in lista:
        ven.totalfinal = (ven.menu.precio) * ven.cantidad
   
      

    venta.total = total
    venta.save()
    
    form = modifyVentaForm(instance=venta)
    form2 = VentaMenuForm()
    return render(request, 'Ventas/modificarVentas.html',{'venta':venta,'lista':lista,'form':form,'form2':form2,'total':total,'user':user})




def cerrarVenta(request,id):
    venta = Venta.objects.get(id=id)
    cliente = venta.cliente
    lista = VentaMenu.objects.filter(venta=id)
    print(cliente)
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

def abrirVenta(request,id):
    venta = Venta.objects.get(id=id)
    venta.is_open= True
    if not venta.is_reopen:
        venta.is_reopen= True
  

    venta.save()
    return redirect('Ventas:ventasIndex')





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
            return render(request, 'Ventas/indexVentas.html',{'form':form})
   
    return redirect("Ventas:ventasIndex")

def ventasCrear(request,id):
    if request.method == "POST":
        form = createVentaForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.empleado = User.objects.get(id=id)
            user.is_open = True
            user.save()
                      

            
            return redirect("Ventas:ventasIndex")
        else:
            return render(request, 'Ventas/ventasIndex.html',{'form':form})
          

    form = createVentaForm()

    return redirect("Ventas:ventasIndex")

def ventasTodas(request):



    return render(request, 'Ventas/ventasTodas.html',)

def ventasCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    ventas = Venta.objects.filter(is_open=False).order_by('-fecha_compra')
 
    if search != "":
        ventas = ventas.filter(
            Q(fecha_compra__icontains=search) 
        )
    return render(request, "Ventas/ventasCard.html",{'ventas':ventas})

def guardarCambios(request,compra_id,list_id,operacion):
    print(compra_id)
    print(list_id)
    compras = Venta.objects.get(id=compra_id)
    producto = VentaMenu.objects.get(venta=compras,id=list_id)
    
    print(operacion)
    if operacion == "suma":
        
        producto.cantidad = producto.cantidad + 1
        producto.save()

    else:
        
        if producto.cantidad == 0:
            producto.delete()
   
        if producto.cantidad > 0:
            producto.cantidad = producto.cantidad - 1
            producto.save()
       

        
        
    
    return redirect("Ventas:modificarVenta",compra_id)
