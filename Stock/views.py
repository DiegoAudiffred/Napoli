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