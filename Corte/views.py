import datetime
from email.message import EmailMessage
import json
import smtplib
import ssl
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from Ventas.forms import VentaMenuForm, createVentaForm, modifyMesaForm, modifyVentaForm, modifyVentaMenuOrder
from db.models import Cliente, Menu, Mesa, User, Venta, VentaMenu,Extras
from django.db.models import Q
from datetime import datetime, timezone
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import QueryDict
from decimal import Decimal
from datetime import datetime, date




def corteDeCajaIndex(request):
    fecha_hoy = date.today()

    Ventas = Venta.objects.filter(fecha_salida__date=fecha_hoy)

    ventasAbiertas = Venta.objects.filter(is_open=True)
    print(Ventas)
    total = 0
    for venta in Ventas:
        total+= venta.total
    return render(request, 'Corte/indexCorte.html',{'Ventas':Ventas,'total':total,'ventasAbiertas':ventasAbiertas,'fecha_hoy':fecha_hoy})


def enviarCorreo(request):
    fecha_hoy = date.today()
    

        
    fecha_legible = fecha_hoy.strftime("%d/%m/%Y")
    Ventas = Venta.objects.filter(fecha_salida__date=fecha_hoy)
    
    for venta in Ventas:
        venta.editable = False
        venta.save()
        
    
    total = 0
    texto = "Ventas del dia " + fecha_legible + "\n"

    for venta in Ventas:
        total+= venta.total
        texto+= "------------------------------\n"
        texto+= "Mesa: " + str(venta.mesa) + "\n"
        texto+= "Fecha: " + str(venta.fecha_salida.strftime("%H:%M")) + "\n"
        texto+= "Total: " + str(venta.total) + "\n"
    
    texto+= "------------------------------\n"
    texto += "Total de las ventas de hoy:  $" + str(total)
    
    
    email_reciver = "d1360.audi@gmail.com"
    #email_reciver2 = "ale_0908@hotmail.com"

    email_sender = "cuentapruebanapoli@gmail.com"
    email_password = "spsy apcz sewh rmbc"  # Asegúrate de que esta contraseña sea la correcta
    
    subject = "Cierre de caja del día: " + fecha_legible
    body = texto

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = [email_reciver]  # Lista de destinatarios , email_reciver2
    em['Subject'] = subject
    em.set_content(body)

    #stringPDF = "ticket" +".pdf"
    #with open(stringPDF, "rb") as f:  
    #    archivo_adjunto = f.read()
    #em.add_attachment(archivo_adjunto, maintype="application", subtype="octet-stream", filename="ticket.pdf")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
    print("Enviaddo")
    return redirect('Index:index')
