import datetime
import json
from django.shortcuts import render
from django.db.models import Q
import cv2 
from pyzbar.pyzbar import decode
import time
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Stock.forms import CompraIngredientesForm, createCompraForm, createStockForm
from db.models import Cliente, CompraIngredientes, Ingredientes, User, Compras
from authentication.forms import createUserForm

def stockIndex(request):
    totalStock = Ingredientes.objects.all().order_by('-fecha_compra')
    totalCompras = Compras.objects.all().order_by('-fecha')[:10]
    form = createStockForm()
    form2 = createCompraForm()

    return render(request, 'Stock/stockIndex.html',{'totalStock':totalStock,'totalCompras':totalCompras,'form':form,'form2':form2})


def stockCrear(request):
    if request.method == "POST":
        print("POST")
        form = createStockForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()

            print("Valido")

            return redirect("Stock:stockIndex")
        else:
            print(form.errors)
            print("No Valido")

    print("NADA")
    return redirect("Stock:stockIndex")


def compraCrear(request):
    if request.method == "POST":
        print("POST")

        form = createCompraForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
          
    

            print("Valido")

            return redirect("Stock:stockIndex")
        
        else:
            print(form.errors)
            print("No Valido")
          
    print("GET")

    return redirect("Stock:stockIndex")

def stockCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    totalStock = Ingredientes.objects.all().order_by('-fecha_compra')
    if search != "":
        totalStock = totalStock.filter(
            Q(nombre__icontains=search) 
        )
    print(totalStock)

  
    return render(request, "Stock/stockCard.html",{'totalStock':totalStock})

def comprasCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    totalCompras = Compras.objects.all().order_by('-fecha')
    if search != "":
        totalCompras = totalCompras.filter(
            Q(fecha__icontains=search) 
        )
    totalCompras = totalCompras[:10]

    return render(request, "Stock/compraCard.html",{'totalCompras':totalCompras})


def compraEditar(request,id):
    compra = Compras.objects.get(id=id)
    lista = CompraIngredientes.objects.filter(compra=id)
    total = 0
    for ventas in lista:
        total += (ventas.ingrediente.precio) * ventas.cantidad
    
    for ven in lista:
        ven.totalfinal = (ven.ingrediente.precio) * ven.cantidad
   
    form = CompraIngredientesForm(instance=compra)
  

    compra.total = total
    compra.save()
    return render(request, "Stock/editarCompra.html",{'compra':compra,'total':total,'lista':lista,'form':form})

def agregarCompra(request,id):
    compra = Compras.objects.get(id=id)

    if request.method == "POST":
        form = CompraIngredientesForm(request.POST, request.FILES)
        if form.is_valid():            
            form.instance.compra = compra

            user = form.save()
            user.save()
                      
            return redirect("Stock:compraEditar",id)
        else:
            return render(request, 'Stock/stockIndex.html',{'form':form})
   
    return redirect("Stock:stockIndex")

#def agregarCompraCamara(request,id):
#    
#        compra = Compras.objects.get(id=id)
#        cap = cv2.VideoCapture(0)
#        cap.set (3, 640) 
#        cap.set (4, 480) 
#        used_codes = []
#        camera = True
#        while camera == True:
#            success, frame = cap.read()
#            for code in decode(frame):
#                if code.data.decode('utf-8') not in used_codes: 
#                    print ('Producto nuevo agregado con éxito')
#                    print(code.data.decode('utf-8'))
#                    used_codes.append(code.data.decode('utf-8'))
#                    camera = False
#                elif code.data.decode('utf-8') in used_codes: 
#                    print ('Sorry, this code has been already used!')
#
#                else:
#                    pass
#            cv2.imshow('Testing-code-scan', frame) 
#            cv2.waitKey (1)
#        cv2.destroyAllWindows()
#        print(used_codes)    
#        
#        
#        ingredientes_encontrados = Ingredientes.objects.filter(codigo_de_barras__in=used_codes)
#        print(ingredientes_encontrados)
#                      
#        return redirect("Stock:compraEditar",id)
#   
#