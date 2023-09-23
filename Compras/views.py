
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Compras.forms import createCompraForm
from Stock.forms import ActualizarCampoForm, CompraIngredientesForm
from db.models import *
from authentication.forms import createUserForm
# Create your views here.
def indexCompras(request):
    totalCompras = Compras.objects.all().order_by('-fecha')[:10]

    form2 = createCompraForm()
    return render(request, 'Compras/indexCompras.html',{'totalCompras':totalCompras,'form2':form2})

def compraCrear(request):
    if request.method == "POST":
        print("POST")

        form = createCompraForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
          
    

            print("Valido")

            return redirect("Compras:indexCompras")
        
        else:
            print(form.errors)
            print("No Valido")
          
    print("GET")

    return redirect("Compras:indexCompras")


def comprasCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    totalCompras = Compras.objects.all().order_by('-fecha')
    if search != "":
        totalCompras = totalCompras.filter(
            Q(fecha__icontains=search) 
        )
    totalCompras = totalCompras[:10]

    return render(request, "Compras/compraCard.html",{'totalCompras':totalCompras})


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
    return render(request, "Compras/editarCompra.html",{'compra':compra,'total':total,'lista':lista,'form':form,'productos':productos,'form2':form2})
def agregarCompra(request,id):
    compra = Compras.objects.get(id=id)

    if request.method == "POST":
        form = CompraIngredientesForm(request.POST, request.FILES)
        if form.is_valid():            
            form.instance.compra = compra
            user = form.save()
            user.save()
                      
            return redirect("Compras:compraEditar",id)
        else:
            return render(request, 'Compras/indexCompras.html',{'form':form})
   
    return redirect("Compras:indexCompras")


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

    return redirect("Compras:compraEditar",id)


def cerrarCompra(request,id):
    compra = Compras.objects.get(id=id)
    lista = CompraIngredientes.objects.filter(compra=id)
    inventario = Ingredientes.objects.all()
    total = 0
    for ventas in lista:
        total += (ventas.ingrediente.precio) * ventas.cantidad
        inventario = Ingredientes.objects.get(id=ventas.ingrediente.id)
        inventario.cantidad += ventas.cantidad
        inventario.save()
    compra.total_comprado = total
    
    compra.save()

    
    return redirect('Compras:indexCompras')



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
       

        
        
    
    return redirect("Compras:compraEditar",compra_id)