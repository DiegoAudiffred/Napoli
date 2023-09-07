import datetime
import json
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Stock.forms import createCompraForm, createStockForm
from db.models import Cliente, Ingredientes, User, Compras
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

            return render(request, 'Stock/crearStock.html',{'form':form})
    print("NADA")
    return redirect("Stock:stockIndex")

def compraCrear(request):
    if request.method == "POST":
        print("POST")

        form = createCompraForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
            ingrediente = form.cleaned_data['ingrediente']
            cantidades = form.cleaned_data['cantidades']

            suma = Ingredientes.objects.get(nombre=ingrediente)
            suma.cantidad = suma.cantidad + cantidades
            suma.save()
            print("Valido")

            return redirect("Stock:stockIndex")
        
        else:
            print(form.errors)
            print("No Valido")
            return render(request, 'Stock/compraCrear.html',{'form':form})
          
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
            Q(ingrediente__nombre__icontains=search) 
        )
    totalCompras = totalCompras[:10]

    return render(request, "Stock/compraCard.html",{'totalCompras':totalCompras})


