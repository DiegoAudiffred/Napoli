import datetime
import json
from django.shortcuts import render
from django.db.models import Q
import time
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Stock.forms import ActualizarCampoForm, CompraIngredientesForm, createStockForm
from db.models import Cliente, CompraIngredientes, Ingredientes, User, Compras
from authentication.forms import createUserForm
from django.contrib.auth.decorators import user_passes_test,login_required

@login_required(login_url='authentication:login')
def stockIndex(request):
    totalStock = Ingredientes.objects.all().order_by('-fecha_compra')
    totalCompras = Compras.objects.all().order_by('-fecha')[:10]
    form = createStockForm()

    return render(request, 'Stock/stockIndex.html',{'totalStock':totalStock,'totalCompras':totalCompras,'form':form})

@login_required(login_url='authentication:login')
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



def stockCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    totalStock = Ingredientes.objects.all().order_by('-fecha_compra')
    if search != "":
        totalStock = totalStock.filter(
            Q(nombre__icontains=search) 
        )

  
    return render(request, "Stock/stockCard.html",{'totalStock':totalStock})




