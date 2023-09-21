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
from Stock.forms import ActualizarCampoForm, CompraIngredientesForm, createCompraForm, createStockForm
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
    productos = Ingredientes.objects.all()
   

    total = 0
    for ventas in lista:
        total += (ventas.ingrediente.precio) * ventas.cantidad
    
    for ven in lista:
        ven.totalfinal = (ven.ingrediente.precio) * ven.cantidad
   
    form = CompraIngredientesForm(instance=compra)
    form2 = ActualizarCampoForm()

    compra.total_comprado = total
    compra.save()
    return render(request, "Stock/editarCompra.html",{'compra':compra,'total':total,'lista':lista,'form':form,'productos':productos,'form2':form2})

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


def agregarCompraCodigo(request,id):
    venta = Compras.objects.get(id=id)
    Ingre = Ingredientes.objects.all()
    if request.method == 'POST':
        print("Aqui")

        form = ActualizarCampoForm(request.POST)
        if form.is_valid():
            codigos = form.cleaned_data['codigo_de_barras'].split(',')  # Dividir por comas

            ingredientes_registrados = []  # Lista para almacenar ingredientes registrados

            print("Los codigos son:")
            print(codigos)
            for codigo in codigos:
                codigo_limpio = codigo.strip()  # Eliminar espacios en blanco alrededor del código
                print("Codigo Limpio")
                print(codigo_limpio)

                existe_codigo = Ingredientes.objects.filter(codigo_de_barras=codigo_limpio).exists()
                print(existe_codigo)

                if existe_codigo:
                    ingrediente = Ingredientes.objects.get(codigo_de_barras=codigo)
                    ingredientes_registrados.append(ingrediente)

                    print(f'El código de barras {codigo} está presente en la base de datos de ingredientes.')
                else:
                    print(f'El código de barras {codigo} no está presente en la base de datos de ingredientes.')
            
            print("Lista de ingredientes:")      
            print(ingredientes_registrados)

            for ingrediente in ingredientes_registrados:
                form2 = CompraIngredientesForm(request.POST)
                if form2.is_valid():
                    form2.instance.ingrediente = ingrediente
                    form2.instance.compra = venta
                    form2.instance.cantidad  = 1
                    form2.instance.totalfinal  = 0
                    form2.save()
                  
              
    else:
        form = ActualizarCampoForm()

    return redirect("Stock:compraEditar",id)


def cerrarCompra(request,id):
    compra = Compras.objects.get(id=id)
    lista = CompraIngredientes.objects.filter(compra=id)

    total = 0
    for ventas in lista:
        total += (ventas.ingrediente.precio) * ventas.cantidad
    
    compra.total_comprado = total
    
    compra.save()

    
    return redirect('Stock:stockIndex')

def guardarCambios(request,compra_id,list_id,operacion):
    print(compra_id)
    print(list_id)
    compras = Compras.objects.get(id=compra_id)
    producto = CompraIngredientes.objects.get(compra=compras,id=list_id)
    
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
       

        
        
    
    return redirect("Stock:compraEditar",compra_id)
  
    #return redirect("Stock:compraEditar",id)

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