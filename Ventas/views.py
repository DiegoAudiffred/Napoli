import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Ventas.forms import VentaMenuForm, createVentaForm, modifyVentaForm
from db.models import Cliente, Venta, VentaMenu
from django.db.models import Q
# Create your views here.
def ventasIndex(request):
    form = createVentaForm()
    form2 = modifyVentaForm()

    ventas = Venta.objects.filter(is_open=True).order_by('-fecha_compra')

    return render(request, 'Ventas/indexVentas.html',{'form':form,'ventas':ventas,'form2':form2})



def modificarVenta(request,id):
    venta = Venta.objects.get(id=id)
    lista = VentaMenu.objects.filter(venta=id)
    total = 0
    for ventas in lista:
        total += (ventas.menu.precio) * ventas.cantidad
    
    for ven in lista:
        ven.totalfinal = (ven.menu.precio) * ven.cantidad
        print(ven.totalfinal)
        
        
    venta.total = total
    
    venta.save()
    #print(venta.total)
    
    form = modifyVentaForm(instance=venta)
    form2 = VentaMenuForm()
    return render(request, 'Ventas/modificarVentas.html',{'venta':venta,'lista':lista,'form':form,'form2':form2,'total':total})




def cerrarVenta(request,id):
    venta = Venta.objects.get(id=id)
    venta.is_open= False
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

def ventasCrear(request):
    if request.method == "POST":
        form = createVentaForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.is_open = True
            user.save()
                      

            
            return redirect("Ventas:ventasIndex")
        else:
            return render(request, 'Ventas/ventasIndex.html',{'form':form})
          

    form = createVentaForm()

    return redirect("Ventas:ventasIndex")

