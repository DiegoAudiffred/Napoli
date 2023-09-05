from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Stock.forms import createStockForm
from db.models import Cliente, Ingredientes, User, Compras
from authentication.forms import createUserForm

def stockIndex(request):
    totalStock = Ingredientes.objects.all()
    totalCompras = Compras.objects.all()
    return render(request, 'Stock/stockIndex.html',{'totalStock':totalStock,'totalCompras':totalCompras})


def stockCrear(request):
    if request.method == "POST":
        form = createStockForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
    
            return redirect("Stock:stockIndex")
        else:
            return render(request, 'Stock/crearStock.html',{'form':form})
          

    form = createStockForm()

    return render(request, 'Stock/crearStock.html',{'form':form})