import datetime
from email.message import EmailMessage
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from Ventas.forms import RegistroCambiosVentaMenuForm, TicketImpresosForm, VentaMenuForm, createVentaForm, modifyMesaForm, modifyVentaForm, modifyVentaMenuOrder,VentaMenuFormDireccion
from db.models import Cliente, Menu, Mesa, TicketImpresos, User, Venta, VentaMenu,Extras
from django.db.models import Q
from datetime import date, datetime, timezone
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import QueryDict
from decimal import Decimal
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

import os
import ssl
import PyPDF2
import subprocess
from django.core.files import File
from io import BytesIO
import subprocess
import tempfile
from django.db import transaction

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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
  
    
    mesasEnUso2 = []
    i = 0
    mesasEnUso = []
    mesas = Mesa.objects.all()
    

    for mesa in mesas:
        if mesa.ocupada:

            ventaActual = Venta.objects.get(mesa = mesa,is_open = True)
            mesasEnUso.append((mesa.id,ventaActual.id))
            mesasEnUso2.append(mesa.id)
            

  

    return render(request, 'Ventas/indexVentas.html',{'mesasEnUso2':mesasEnUso2,'mesasEnUso':mesasEnUso,'form':form,'ventas':ventas,'form2':form2,'form3':form3,'user':user})

@login_required(login_url='authentication:login')



def addMesa(request,id):
    venta = Venta.objects.get(id=id)
    mesa = Mesa.objects.get(nombre = venta.mesa)
   
    mesa_nueva = mesa
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
                mesa_nueva=mesa_value2
        else:
            
            return redirect('Ventas:modificarVenta',mesa.id)

    return redirect('Ventas:modificarVenta',mesa_nueva.id)

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


def addDireccion(request,id):
    venta = Venta.objects.get(id=id)
    if request.method == 'POST':
        form = VentaMenuFormDireccion(request.POST, instance=venta)  # Inicializar el formulario con los datos POST
        if form.is_valid():
            user = form.save()
            user.save()
        else:
            return redirect('Ventas:modificarVenta',venta.mesa.id)
    return redirect('Ventas:modificarVenta',venta.mesa.id)


def modificarVentaPasada(request,id):
        
        venta = Venta.objects.get(id=id)
        #venta = Venta.objects.get(id=26)
    
        mesas = Mesa.objects.all()
    
        menu = Menu.objects.all()
        lista = VentaMenu.objects.filter(venta=id, cantidad__gt=0)

        publications=[]
        for lst in lista:
                publications.append(modifyVentaMenuOrder(instance=lst))
    
        user = request.user
        total2 = 0
        for total in lista:
            total2 += total.totalfinal
           
        venta.total = total2
        venta.save()
        form = modifyVentaForm(instance=venta) #Cliente
        form2 = VentaMenuForm() #Venta
        form3 = modifyMesaForm() #Mesa
        form4 = modifyVentaMenuOrder()
        form5 = VentaMenuFormDireccion(instance=venta)
        fecha_hoy = date.today()
        nfinal = 0
        numVentaHoy = Venta.objects.filter(fecha_compra__date = fecha_hoy)
        for index, hoy in enumerate(numVentaHoy, start=1):
            if hoy == venta:
                nfinal = index
        return render(request, 'Ventas/modificarVentaPasada.html',{'venta':venta,'items':lista,'lista':zip(lista,publications),'form':form,'form2':form2,'form3':form3,'form4':form4,'form5':form5,'total':total2,'user':user,'mesas':mesas,'menu':menu,'nfinal':nfinal}) 





def modificarVenta(request,id):
        mesa = Mesa.objects.get(id=id)
        venta = Venta.objects.get(mesa=mesa,is_open= True)
        #venta = Venta.objects.get(id=26)
    
        mesas = Mesa.objects.all()
    
        menu = Menu.objects.all()
        lista = VentaMenu.objects.filter(venta=venta.id, cantidad__gt=0)

        publications=[]
        for lst in lista:
                publications.append(modifyVentaMenuOrder(instance=lst))
    
        user = request.user
        total2 = 0
        for total in lista:
            total2 += total.totalfinal
           
        venta.total = total2
        venta.save()
        form = modifyVentaForm(instance=venta) #Cliente
        form2 = VentaMenuForm() #Venta
        form3 = modifyMesaForm() #Mesa
        form4 = modifyVentaMenuOrder()
        form5 = VentaMenuFormDireccion(instance=venta)
        fecha_hoy = date.today()
        nfinal = 0
        numVentaHoy = Venta.objects.filter(fecha_compra__date = fecha_hoy)
        for index, hoy in enumerate(numVentaHoy, start=1):
            if hoy == venta:
                nfinal = index
        if venta:
            return render(request, 'Ventas/modificarVentas.html',{'venta':venta,'items':lista,'lista':zip(lista,publications),'form':form,'form2':form2,'form3':form3,'form4':form4,'form5':form5,'total':total2,'user':user,'mesas':mesas,'menu':menu,'nfinal':nfinal}) 
        else:
            return redirect("Ventas:ventasIndex")


@login_required(login_url='authentication:login')
def updateRow(request,lista):
        row = VentaMenu.objects.get(id=lista)
        totalUpdate = 0
        totalAntes = row.totalfinal
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
                extraCosto =form.cleaned_data['extraCosto']
                if platillo.categoria == "Pizza":
                    if familiar:
                        if pizza_mitad:
                            if pizza_mitad.precioFamiliar < platillo.precioFamiliar:
                        
                                totalUpdate += platillo.precioFamiliar 

                            else:
                                totalUpdate += (pizza_mitad.precioFamiliar)

                        else:
                       
                           
                            totalUpdate += (platillo.precioFamiliar)

                    else:
                        if pizza_mitad: 
                            if pizza_mitad.precio < platillo.precio:
                                totalUpdate += (platillo.precio)

                            else:
                            
                                totalUpdate += (pizza_mitad.precio)


                        else:
                                totalUpdate += (platillo.precio)

                elif media_orden == True: #Mediaorden
                        totalUpdate += (platillo.mediaOrden)

                else: #Compra normal
                    totalUpdate += (platillo.precio)

                listaextras = Extras.objects.all()
                for i,list in enumerate(listaextras):
                    if listaextras[i] in extras:
                        if familiar:
                            totalUpdate += (listaextras[i].precio* 2)
                          
                        else:
                            totalUpdate += listaextras[i].precio
                          
                form.instance.totalfinal = totalUpdate * cantidad + extraCosto
                form.instance.final = totalUpdate

                
                form.save()
                if row.venta.is_reopen:
                    registro_form = RegistroCambiosVentaMenuForm({'venta_menu': row.menu.nombre,
                                                                  'accion': "MODIFICADO",
                                                                  'fecha_hora_cambio': datetime.now(),
                                                                  'precioAnterior': totalAntes,
                                                                  'precioNuevo': row.totalfinal,
                                                                  'mesa':row.venta.mesa,
                                                                  'venta': row.venta.id,})
        
                    if registro_form.is_valid():
                        registro_form.save()
               

                    else:
                        pass
        if row.venta.is_reopen:
            return redirect('Ventas:modificarVentaPasada',row.venta.id)

        else:
            return redirect('Ventas:modificarVenta',row.venta.mesa.id)



    
@login_required(login_url='authentication:login')


def updateRow2(request, list):
    pizzas = Menu.objects.filter(categoria="Pizza")
    row = VentaMenu.objects.get(id=list)
    venta = row.venta
    #if request.method == "POST":
    #    form = modifyVentaMenuOrder(request.POST, instance=row)
    #    if form.is_valid():
    #        form.save()
    
    form = modifyVentaMenuOrder(instance=row)

    return render(request, 'Ventas/modificarRow.html', {'row': row, 'venta': venta, 'form': form,'pizzas': pizzas})




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
            pass
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
  


def enviarCorreo():
    #venta = Venta.objects.get(id=id)

    email_reciver = "d1360.audi@gmail.com"
    email_sender = "cuentapruebanapoli@gmail.com"
    email_password = "spsy apcz sewh rmbc"  # Asegúrate de que esta contraseña sea la correcta
    
    subject = "Correo con archivo adjunto"
    body = "Hola, adjunto te envío un archivo desde Python."

    # Creación del mensaje de correo electrónico
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciver
    em['Subject'] = subject
    em.set_content(body)
    idstring= str(id)

    stringPDF = "ticket"+ idstring +".pdf"
    # Adjuntar el archivo PDF
    with open(stringPDF, "rb") as f:  # Asegúrate de proporcionar la ruta correcta al archivo PDF
        archivo_adjunto = f.read()
    em.add_attachment(archivo_adjunto, maintype="application", subtype="octet-stream", filename="ticket.pdf")

    # Configuración del servidor SMTP y envío del correo electrónico
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
    

# Llamada a la función para enviar el correo electrónico
  
@login_required(login_url='authentication:login')

def ticketRead(request,venta):
    
        venta = Venta.objects.get(id=venta)
     
        items = VentaMenu.objects.filter(venta=venta)
       

        return render(request, 'Ventas/ticket.html',{'venta':venta,'items':items}) 

# views.py



def actualizar_ticket(request, venta):
    if request.method == 'POST':
        # Obtener los datos JSON del cuerpo de la solicitud
        venta = Venta.objects.get(id=venta)
        venta.impresiones += 1
        venta.save()


        ticket = TicketImpresos.objects.filter(venta=venta).count()
        
        cantidad = 0
        if ticket == 0:
            cantidad = 1
        else:
            cantidad = ticket + 1
           

        registro_form = TicketImpresosForm({'venta': venta,
                                                    'cantidad': venta.total ,
                                                    'numImpresion': cantidad ,
                                                    'horaImpresion': datetime.now(),
                                                                  })
               

        if registro_form.is_valid():
                        registro_form.save()
        else:
            pass
            
     

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})



def ticket(request,venta):
    venta = Venta.objects.get(id=venta)
    generar_pdf(venta.id)
    return redirect('Ventas:ventasIndex')

def cerrarVenta(request,id):
    venta = Venta.objects.get(id=id)
    if venta.is_open or venta.is_reopen:
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
        #if venta.is_open:
        #    enviarCorreo(venta.id)
        
 
        venta.is_open= False
      
        venta.is_reopen= False
        venta.save()
        venta.fecha_salida = datetime.now()  
        venta.save()
        if venta.total == 0:
            venta.delete()
        
        #else:
        #    generar_pdf(venta.id)
            
  

    
    
    #venta.ticket = generar_pdf(venta.id)
    return redirect('Ventas:ventasIndex')

@login_required(login_url='authentication:login')

def abrirVenta(request,id):
    venta = Venta.objects.get(id=id)
    #venta.is_open= True
    venta.is_reopen= True
    

    venta.save()
    return redirect('Ventas:modificarVentaPasada',id)




@login_required(login_url='authentication:login')
#Forms viejos
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
            pass
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


@transaction.atomic
def ventasCrearMesa(request, mesa):
    if request.method == "POST":
        mesa_ocupada = Mesa.objects.filter(nombre=mesa, ocupada=True).exists()
        
        form = createVentaForm(request.POST, request.FILES)
        hot = date.today() 
    
        vDia = Venta.objects.filter(fecha_compra__date=hot).count()

        if form.is_valid():
            if not mesa_ocupada:    
                mesa = Mesa.objects.get(nombre=mesa)
                # Guardar la venta dentro de una transacción
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.empleado = request.user
                    user.mesa = Mesa.objects.get(nombre=mesa)
                    user.numVentaDia = vDia + 1
                    mesa2 = Mesa.objects.get(nombre=mesa)
                    mesa2.ocupada = True
                    mesa2.save()
                    user.is_open = True
                    user.save()
                    id = user.id

                    return redirect("Ventas:modificarVenta", id=mesa.id)
            else:
                # La mesa está ocupada, mostrar algún mensaje de error
                pass
        else:
            # El formulario no es válido, volver a renderizar el formulario con los errores
            return render(request, 'Ventas/ventasIndex.html', {'form': form})
   
    # Si la solicitud no es de tipo POST, redirigir a la página de índice de ventas
    return redirect("Ventas:ventasIndex")


@login_required(login_url='authentication:login')

def ventasTodas(request):
     

  
    ventasPasadas = []
    ventas = Venta.objects.filter(is_open = False)
    for venta in ventas:
        
            ventasPasadas.append(venta.id)
       
            




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
    precioAnterior = producto.totalfinal
    if operacion == "suma":
        producto.cantidad = producto.cantidad + 1
        producto.totalfinal = producto.final * producto.cantidad + producto.extraCosto

        producto.save()
        
        if venta.is_reopen:
            registro_form = RegistroCambiosVentaMenuForm({
            'venta_menu': producto.menu.nombre,
            'accion': "AUMENTO",
            'fecha_hora_cambio': datetime.now(),
            'precioAnterior': precioAnterior,
            'precioNuevo': producto.totalfinal,
            'mesa':venta.mesa,
            'venta': venta.id,})
          
    
            if registro_form.is_valid():
                    registro_form.save()
               
               

    else:
        
        
        if producto.cantidad > 0:

                producto.cantidad = producto.cantidad - 1
                producto.totalfinal = producto.final * producto.cantidad + producto.extraCosto
                producto.save()
                if venta.is_reopen:

                    registro_form = RegistroCambiosVentaMenuForm({
                                  'venta_menu': producto.menu.nombre,
                                  'accion': "DISMINUYO",
                                  'fecha_hora_cambio': datetime.now(),
                                 'precioAnterior': precioAnterior,
                                  'precioNuevo': producto.totalfinal,
                                  'mesa':venta.mesa,
                                  'venta': venta.id,
                                  })
          
              
                    if registro_form.is_valid():
                        registro_form.save()
               
        if producto.cantidad == 0:
            if venta.is_reopen:

                registro_form = RegistroCambiosVentaMenuForm({
                             'venta_menu': producto.menu.nombre,
                             'accion': "ELIMINADO",
                             'fecha_hora_cambio': datetime.now(),
                             'precioAnterior': precioAnterior,
                             'precioNuevo': 0,
                             'mesa':venta.mesa,
                             'venta': venta.id,})
        
                if registro_form.is_valid():
                    registro_form.save()
            producto.delete()
   
       
    if venta.is_reopen:
         return redirect("Ventas:modificarVentaPasada",venta.id)
    else: 
        return redirect("Ventas:modificarVenta",venta.mesa.id)

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
def agregarPlatillosVenta(request, id):
    venta = Venta.objects.get(id=id)
    hoy = datetime.now() 
   
    if request.method == 'POST':
        platillos_ids = request.POST.get('platillosIds').split(',')

        for platillo_id in platillos_ids:
            menu = Menu.objects.get(id=platillo_id)
            final = menu.precio
            residuo = final % 10
            if residuo > 5:
                final += (10-residuo)  
            elif residuo > 0: 
                final += (5-residuo)  
            
            form = VentaMenuForm({
                'venta': venta,
                'menu': menu,
                'cantidad': 1,
                'observaciones': "",
                'familiar': False,
                'media_orden': False,
                'pizza_mitad': "",
                'totalfinal': final,
                'extras':"",
                'final': final,
                
            })

            if form.is_valid():    
                venta_menu_instance = form.save()  # Guardamos el formulario y obtenemos la instancia creada
                
                if venta.is_reopen:
                    registro_form = RegistroCambiosVentaMenuForm({
                        'venta_menu': menu.nombre,  # Usamos la instancia creada
                        'accion': "CREADO",
                        'fecha_hora_cambio': datetime.now(),
                        'precioAnterior': 0,
                        'precioNuevo': menu.precio,
                        'mesa':venta.mesa,
                        'venta': venta.id,
                    })
                    if registro_form.is_valid():
                        registro_form.save()
                    else:
                        pass
            else:
                pass

        return redirect('Ventas:modificarVenta', venta.mesa.id)
    
    
def agregarPlatillosVentaPasada(request, id):
    venta = Venta.objects.get(id=id)
    hoy = datetime.now() 
   
    if request.method == 'POST':
        platillos_ids = request.POST.get('platillosIds').split(',')

        for platillo_id in platillos_ids:
            menu = Menu.objects.get(id=platillo_id)
            final = menu.precio
            residuo = final % 10
            if residuo > 5:
                final += (10-residuo)  
            elif residuo > 0: 
                final += (5-residuo)  
            
            form = VentaMenuForm({
                'venta': venta,
                'menu': menu,
                'cantidad': 1,
                'observaciones': "",
                'familiar': False,
                'media_orden': False,
                'pizza_mitad': "",
                'totalfinal': final,
                'extras':"",
                'final': final,
                
            })

            if form.is_valid():    
                venta_menu_instance = form.save()  # Guardamos el formulario y obtenemos la instancia creada
                
                if venta.is_reopen:
                    registro_form = RegistroCambiosVentaMenuForm({
                        'venta_menu': menu.nombre,  # Usamos la instancia creada
                        'accion': "CREADO",
                        'fecha_hora_cambio': datetime.now(),
                        'precioAnterior': 0,
                        'precioNuevo': menu.precio,
                        'mesa':venta.mesa,
                        'venta': venta.id,
                    })
                    if registro_form.is_valid():
                        registro_form.save()
                    else:
                        pass
            else:
                pass

        return redirect('Ventas:modificarVentaPasada', venta.id)