import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from Ventas.forms import VentaMenuForm, createVentaForm, modifyMesaForm, modifyVentaForm, modifyVentaMenuOrder
from db.models import Cliente, Menu, Mesa, User, Venta, VentaMenu,Extras
from django.db.models import Q
from datetime import datetime, timezone
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import QueryDict
from decimal import Decimal
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import os
import win32print
import win32ui
import os
import win32api
import PyPDF2
import subprocess
from django.core.files import File
from io import BytesIO

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
   # Assuming ventas is a queryset or list of Venta objects
  
    
    mesasEnUso2 = []
    i = 0
    mesasEnUso = []
    mesas = Mesa.objects.all()
    for mesa in mesas:
        if mesa.ocupada:
            ventaActual = Venta.objects.get(mesa = mesa,is_open = True)
            mesasEnUso.append((mesa.id,ventaActual.id))
            mesasEnUso2.append(mesa.id)
            

    print(mesasEnUso)
  

    return render(request, 'Ventas/indexVentas.html',{'mesasEnUso2':mesasEnUso2,'mesasEnUso':mesasEnUso,'form':form,'ventas':ventas,'form2':form2,'form3':form3,'user':user})

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
    mesa = Mesa.objects.get(nombre = venta.mesa)
    if request.method == 'POST':
        form = modifyMesaForm (request.POST, instance=venta)  # Inicializar el formulario con los datos POST
        if form.is_valid():
            mesa_value = form.cleaned_data['mesa']
            
            mesa_value2 = Mesa.objects.get(nombre=mesa_value)

            if mesa_value2.ocupada:
                pass
            else:
                user = form.save()
                user.save()
               
                mesa_value2.ocupada = True
                mesa.ocupada = False
            mesa_value2.save()
            mesa.save()
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
        print(id)
        print(venta)
        mesaactual = venta.mesa
    
        mesas = Mesa.objects.all()
    
        menu = Menu.objects.all()
        lista = VentaMenu.objects.filter(venta=id)

        publications=[]
        for lst in lista:
                publications.append(modifyVentaMenuOrder(instance=lst))
    
        user = request.user
        total2 = 0
        for total in lista:
            total2 += total.totalfinal
            print(total)
            print(total2,"acumulado")
        venta.total = total2
        venta.save()
        form = modifyVentaForm(instance=venta) #Cliente
        form2 = VentaMenuForm() #Venta
        form3 = modifyMesaForm() #Mesa
        form4 = modifyVentaMenuOrder()

        return render(request, 'Ventas/modificarVentas.html',{'venta':venta,'lista':zip(lista,publications),'form':form,'form2':form2,'form3':form3,'form4':form4,'total':total2,'user':user,'mesas':mesas,'menu':menu}) 

#def  modificarVenta(request,mesa):
#    mesaVenta = Mesa.objects.get(nombre = mesa)
#    print(mesaVenta)
#
#    venta = Venta.objects.get(mesa = mesaVenta,is_open = True)
#    print(venta)
#
#    mesas = Mesa.objects.all()
#    
#    menu = Menu.objects.all()
#    lista = VentaMenu.objects.filter(venta=venta.id)
#    print(lista)
#    publications=[]
#    for lst in lista:
#            publications.append(modifyVentaMenuOrder(instance=lst))
#  
#    user = request.user
#    total2 = 0
#    for total in lista:
#        total2 += total.totalfinal
#        print(total)
#        print(total2,"acumulado")
#    venta.total = total2
#    venta.save()
#    form = modifyVentaForm(instance=venta) #Cliente
#    form2 = VentaMenuForm() #Venta
#    form3 = modifyMesaForm() #Mesa
#    form4 = modifyVentaMenuOrder()
#
#    return render(request, 'Ventas/modificarVentas.html',{'venta':venta,'lista':zip(lista,publications),'form':form,'form2':form2,'form3':form3,'form4':form4,'total':total2,'user':user,'mesas':mesas,'menu':menu}) 


@login_required(login_url='authentication:login')
def updateRow(request,lista,venta):
        row = VentaMenu.objects.get(id=lista)
        total = 0
        totalIndv = 0
        print(row)
        if request.method == "POST":
            form = modifyVentaMenuOrder(request.POST, instance=row)
            if form.is_valid():
                platillo = form.cleaned_data['menu']
                familiar = form.cleaned_data['familiar']
                pizza_mitad = form.cleaned_data['pizza_mitad']
                familiar = form.cleaned_data['familiar']
                cantidad = form.cleaned_data['cantidad']
                media_orden = form.cleaned_data['media_orden']
                extras=form.cleaned_data['extras']

                if platillo.categoria == "Pizza":
                    print("Pizza pizza")
                    if familiar:
                        print("Familiar")
                        if pizza_mitad:
                            print("Mitad")
                            if pizza_mitad.precioFamiliar < platillo.precioFamiliar:
                                print("La cara es la ")    
                                totalIndv += (platillo.precioFamiliar) 
                                total += (pizza_mitad.precioFamiliar) * cantidad

                            else:
                                totalIndv += (pizza_mitad.precioFamiliar)
                                total += (pizza_mitad.precioFamiliar) * cantidad

                        else:
                            print(f"Total:{platillo}")
                            print(f"cantidad:{pizza_mitad}")
                           
                            totalIndv += (platillo.precioFamiliar)
                            total += (platillo.precioFamiliar) * cantidad

                    else:
                        if pizza_mitad: 
                            if pizza_mitad.precio < platillo.precio:
                                totalIndv += (platillo.precio)
                                total += (platillo.precio) * cantidad

                            else:
                            
                                totalIndv += (pizza_mitad.precio)
                                total += (pizza_mitad.precio) * cantidad                            


                        else:
                                totalIndv += (platillo.precio)
                                total += (platillo.precio) * cantidad  

                elif media_orden == True: #Mediaorden
                        totalIndv += (platillo.mediaOrden)
                        total += (platillo.mediaOrden) * cantidad  

                else: #Compra normal
                    totalIndv += (platillo.precio)
                    total += (platillo.precio) * cantidad  

                listaextras = Extras.objects.all()
                for i,list in enumerate(listaextras):
                    if listaextras[i] in extras:
                        total += listaextras[i].precio * cantidad
                        totalIndv += listaextras[i].precio
                        print("Entro", listaextras[i] )


                form.instance.totalfinal = total
                form.instance.final = totalIndv

                print(total)
                print(totalIndv)   
                form.save()


    
        return redirect('Ventas:modificarVenta',venta)


    
@login_required(login_url='authentication:login')
def updateRow2(request, list):
    pizzas = Menu.objects.filter(categoria="Pizza")
    print(pizzas)
    row = VentaMenu.objects.get(id=list)
    venta = row.venta
    if request.method == "POST":
        form = modifyVentaMenuOrder(request.POST, instance=row)
        if form.is_valid():
            form.save()
    else:
        form = modifyVentaMenuOrder(instance=row)
    return render(request, 'Ventas/modificarRow.html', {'row': row, 'venta': venta, 'form': form,'pizzas':pizzas})





def generar_pdf(id):
    venta = Venta.objects.get(id=id)
    pdf_file = "ticket" + str(id) +".pdf" 
    row = VentaMenu.objects.filter(venta=venta)
    alturaFinal = int(row.count() * 20 + 450)
    pdf = canvas.Canvas(pdf_file, pagesize=(215, alturaFinal))
    
    pdf.setFont("Helvetica", 12)
    line_start = 30
    line_end = 180
    pdf.drawString(line_start, alturaFinal - 60, "Napoli Ristorante y Pizzeria")
    pdf.drawString(line_start, alturaFinal - 80, "C. 29 Sur 119, La Paz, 72160") 
    pdf.drawString(line_start, alturaFinal - 100, "Heroica Puebla de Zaragoza")
    pdf.drawString(line_start, alturaFinal - 120, "Teléfono: 222 621 9650")
    pdf.drawString(line_start, alturaFinal - 140, "--------------------------------")
  

    pdf.drawString(line_start, alturaFinal - 160, "Producto        Cantidad  Total")
    pdf.drawString(line_start, alturaFinal - 170, "                                 ")

   # Posiciones iniciales y configuraciones
    line_start = 30
    alturaFor = alturaFinal - 190
    var = 20
    espacio_linea = 20  # Espacio vertical entre cada línea de producto

    for products in row:
        nombre = products.menu.nombre[:15]
        diff = 15 - len(nombre)
        if len(nombre) < 15:
            nombre += " " * (diff)
        
        cantidad = str(products.cantidad)
        if products.cantidad >= 10:
            nombre += "    "
            
        else:
            nombre += "     "
        
        if products.totalfinal >=100 and products.totalfinal < 1000:
            cantidad +="    "   
            print("Entro", products.menu.nombre)
        elif products.totalfinal >= 1000:
            cantidad +="  "  
        else:
            cantidad +="     " 
              
        ing = []
        totalfinal = str(products.totalfinal)
        string = nombre + cantidad + totalfinal
        pdf.drawString(line_start, alturaFor - var, string)
        
        if products.extras.exists():
            for extra in products.extras.all():
                ing.append(extra.nombre)
                
        try:
            pdf.drawString(line_start, alturaFor - var + 10, ing[0])
            pdf.drawString(line_start, alturaFor - var + 20, ing[1])
            pdf.drawString(line_start, alturaFor - var + 30, ing[2])
            pdf.drawString(line_start, alturaFor - var + 40, ing[3])

        except:
            print("")
        pdf.drawString(line_start, alturaFor - var + 50, "                                 ")

        var += espacio_linea  
    
    alturaPostFor = alturaFor - var
    totalString= str(venta.total)
    strintTotal = f"Total:                  {totalString}"
    pdf.drawString(line_start,alturaPostFor, strintTotal)

    pdf.drawString(line_start,alturaPostFor - 20 , "--------------------------------")
    pdf.drawString(line_start,alturaPostFor- 40, "Gracias por su compra")
    empleado = f"Atendido por: {venta.empleado}"
    nventa = f"Venta num: {venta.id}"
    nmesa = f"Mesa: {venta.mesa}"

    pdf.drawString(line_start, alturaFinal - 160, nmesa)
    
    fecha = f"Fecha: {venta.fecha_compra.strftime('%Y-%m-%d %H:%M:%S')}"
    
    #pdf.drawString(line_start,alturaPostFor- 60, empleado)
    #pdf.drawString(line_start,alturaPostFor- 80, nventa)
    pdf.drawString(line_start,alturaPostFor- 100, fecha)

    pdf.drawString(line_start,alturaPostFor- 120, "Este ticket no es un comprobante")
    pdf.drawString(line_start,alturaPostFor- 140, "fiscal")
    pdf.drawString(line_start,alturaPostFor- 160, "Para facturar mandar sus datos")
    pdf.drawString(line_start,alturaPostFor- 160, "fiscales completos al correo: ")

    
    pdf.drawString(line_start,alturaPostFor- 160, "napoli10.facturacion@gmail.com")
    pdf.drawString(line_start,0  , "--------------------------------")


    pdf.showPage()
    pdf.save()
    #os.startfile(pdf_file)
 
   
    
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        texto = ''
        for page in pdf_reader.pages:
            texto += page.extract_text()
    print(texto)
    printer_name = win32print.GetDefaultPrinter()
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Texto a imprimir", None, "RAW"))
        print("parte1")
        try:
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, texto.encode('utf-8'))
            win32print.EndPagePrinter(hPrinter)
            print("parte2")
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)
       
    if os.path.exists(pdf_file):
        os.remove(pdf_file)

    
  
@login_required(login_url='authentication:login')


def ticket(request,venta):
    venta = Venta.objects.get(id=venta)
    generar_pdf(venta.id)
    return redirect('Ventas:ventasIndex')

def cerrarVenta(request,id):
    venta = Venta.objects.get(id=id)
    if venta.is_open:
        #cliente = venta.cliente
        lista = VentaMenu.objects.filter(venta=id)
        mesa = venta.mesa
        mesa.ocupada=False
        mesa.save()
        total2 = 0
        for total in lista:
            total2 += total.totalfinal
        venta.total = total2
        venta.save()
        #if venta.is_reopen == False:
        #    cliente.total_compras +=  1
        #    cliente.total_gastado += total
        #cliente.save()
        venta.is_reopen = True
        venta.is_open= False
        venta.fecha_salida = datetime.now()  
        venta.save()
        if venta.total == 0:
            venta.delete()
        else:
            generar_pdf(venta.id)
  

    
    
    #venta.ticket = generar_pdf(venta.id)
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

def agregarVenta(request, id):
    ventas = Venta.objects.get(id=id)
    lista = VentaMenu.objects.filter(venta=id)
    data_from_jquery = request.POST
    mutable_data = QueryDict(mutable=True)
    mutable_data.update(data_from_jquery)
    new_dict = {re.sub(r'_\d+$', '', key): value for key, value in mutable_data.items()}
    if request.method == "POST":
        menu_id = new_dict.get('id_menu')
        cantidad = Decimal(new_dict.get('id_cantidad'))
        observaciones = new_dict.get('id_observaciones')
        pizza_id = new_dict.get('id_pizza_mitad')
        familiar = new_dict.get('id_familiar')
        media_orden = new_dict.get('id_media_orden')
        extra1=new_dict.get('id_extras_0')
        extra2=new_dict.get('id_extras_1')
        extra3=new_dict.get('id_extras_2')
        extra4=new_dict.get('id_extras_3')
        extrasList = [extra1, extra2, extra3, extra4]

        menu = None
        pizza_mitad = None
        for i in range(len(extrasList)):
            extrasList[i] = extrasList[i] != "false"
           
        if media_orden == "false":
            media_orden = False
        else:
            media_orden = True
        if familiar == "false":
            familiar = False
        else:
            familiar = True
        if menu_id:
            menu = Menu.objects.get(id=menu_id)
        
        if pizza_id:
            pizza_mitad = Menu.objects.get(id=pizza_id)
        #####
  

        total = 0
        totalIndiv=0

        if menu.categoria == "Pizza":
            if familiar:
                if pizza_mitad:
                    if pizza_mitad.precioFamiliar < menu.precioFamiliar:
                        total += (menu.precioFamiliar) * cantidad
                        totalIndiv += (menu.precioFamiliar)

                    else:
                        total += (pizza_mitad.precioFamiliar) * cantidad
                        totalIndiv += (pizza_mitad.precioFamiliar)

                else:
                    total += (menu.precioFamiliar) * cantidad
                    totalIndiv += (menu.precioFamiliar)
   
            else:
                if pizza_mitad: 
                    if pizza_mitad.precio < menu.precio:
                        total += (menu.precio) * cantidad
                        totalIndiv += (menu.precio)
      
                    else:
                  
                        total += (pizza_mitad.precio) * cantidad
                        totalIndiv += (pizza_mitad.precio) 
                else:
                        total += (menu.precio) * cantidad
                
                        totalIndiv += (menu.precio)

        elif media_orden == True: #Mediaorden
                total += (menu.mediaOrden) * (cantidad)
                totalIndiv += (menu.mediaOrden)

        else: #Compra normal
                total += (menu.precio) * cantidad
                totalIndiv += (menu.precio)
   
        listaextras = Extras.objects.all()
        
        for i,ext in enumerate(listaextras):
            if extrasList[i] == True:
                if familiar:
                    total += ext.precioFamiliar * cantidad
                    totalIndiv += ext.precioFamiliar

                else:
                    total += ext.precio * cantidad               
                    totalIndiv += ext.precio

        indicies = []
        for i,ex in enumerate(extrasList):
            elemento = Extras.objects.get(id=i+1)
            if extrasList[i] == True:
                    indicies.append(i+1)
      

        queryset_result = Extras.objects.filter(id__in=indicies)        
        print(total,"TotalFinal")
        print(totalIndiv,"Indiv")
        ####   
        form = VentaMenuForm({
            'venta': ventas,
            'menu': menu,
            'cantidad': cantidad,
            'observaciones': observaciones,
            'familiar': familiar,
            'media_orden': media_orden,
            'pizza_mitad': pizza_mitad,
            'totalfinal':total,
            'extras':queryset_result,
            'final':totalIndiv
        })

        if form.is_valid():    
            data = form.cleaned_data
            data2 = form.save()
            return redirect("Ventas:modificarVenta", id)
        else:
            print(form.errors)
    return redirect("Ventas:ventasIndex")


@login_required(login_url='authentication:login')

#def ventasCrear(request,id):
#    if request.method == "POST":
#        form = createVentaForm(request.POST, request.FILES)
#   
#        if form.is_valid():
#            user = form.save()
#            user.empleado = request.user
#            user.cliente = Cliente.objects.get(id=1)
#
#            user.is_open = True
#            user.save()
#                      
#
#            
#            return redirect("Ventas:ventasIndex")
#        else:
#            return render(request, 'Ventas/ventasIndex.html',{'form':form})
#          
#
#    form = createVentaForm()
#
#    return redirect("Ventas:ventasIndex")
#
#
@login_required(login_url='authentication:login')

def ventasCrearMesa(request, mesa):
    if request.method == "POST":
        mesa_ocupada = Mesa.objects.filter(nombre=mesa, ocupada=True).exists()

        form = createVentaForm(request.POST, request.FILES)

        if form.is_valid():
            if not mesa_ocupada:
                user = form.save(commit=False)
                user.empleado = request.user
                user.mesa = Mesa.objects.get(nombre=mesa)
                mesa2 = Mesa.objects.get(nombre=mesa)
                mesa2.ocupada = True
                mesa2.save()
                user.is_open = True
                user.save()
                id = user.id
                return redirect("Ventas:modificarVenta", id=id)
            else:
                pass
        else:
            return render(request, 'Ventas/ventasIndex.html', {'form': form})

    form = createVentaForm()
    return redirect("Ventas:ventasIndex")

@login_required(login_url='authentication:login')

def ventasTodas(request):
     
  
    ventasPasadas = []
    ventas = Venta.objects.filter(is_open = False)
    for venta in ventas:
        
            ventasPasadas.append(venta.id)
       
            

    print(ventas)


    return render(request, 'Ventas/ventasTodas.html',{'ventas':ventas,'ventasPasadas':ventasPasadas})

def ventasCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    fecha = jsonObject["date"]
   
    


    ventas = Venta.objects.filter(Q(is_open=False) | Q(is_reopen=True)).order_by('-fecha_compra')

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

    venta = Venta.objects.get(id=compra_id)
    producto = VentaMenu.objects.get(venta=venta,id=list_id)

    if operacion == "suma":
        
        producto.cantidad = producto.cantidad + 1
        producto.totalfinal = producto.final * producto.cantidad
        producto.save()

    else:
        print("resta")
        if producto.cantidad > 0:

                producto.cantidad = producto.cantidad - 1
                producto.totalfinal = producto.final * producto.cantidad
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
    
    
@login_required(login_url='authentication:login')
def agregarPlatillosVenta(request,id):
    print(id)
    venta = Venta.objects.get(id=id)
    print(venta)

    if request.method == 'POST':
        platillos_ids = request.POST.get('platillosIds').split(',')

        for platillo_id in platillos_ids:
            menu = Menu.objects.get(id=platillo_id)
            final = menu.precio
            totalfinal = final
            form = VentaMenuForm({
            'venta': venta,
            'menu': menu,
            'cantidad': 1,
            'observaciones': "",
            'familiar': False,
            'media_orden': False,
            'pizza_mitad': "",
            'totalfinal':totalfinal,
            'extras':"",
            'final':final})
            if form.is_valid():    
                data = form.cleaned_data
                data = form.save()
            else:
                print(form.errors)
        

            
        return redirect('Ventas:modificarVenta',id)

