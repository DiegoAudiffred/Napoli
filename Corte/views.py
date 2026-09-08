import datetime
from email.message import EmailMessage
import json
import smtplib
import ssl
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from Ventas.forms import VentaMenuForm, createVentaForm, modifyMesaForm, modifyVentaForm, modifyVentaMenuOrder
from db.models import CierreDeCaja, Cliente, Menu, Mesa, User, Venta, VentaMenu,Extras
from django.db.models import Q
from datetime import datetime, timezone
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import QueryDict
from decimal import Decimal
from datetime import datetime, date
from django.utils import timezone
from datetime import datetime, timedelta



def corteDeCajaIndex(request):
    fecha_hoy = date.today()

    Ventas = Venta.objects.filter(fecha_salida__date=fecha_hoy, is_open=False, is_reopen=False).order_by('numVentaDia')

    ventasAbiertas = Venta.objects.filter(is_open=True)
    total = 0
    for venta in Ventas:
        total+= venta.total
        
         # Obtener la fecha y hora actual
    fecha_actual = timezone.now()

    # Obtener solo la parte de la fecha
    fecha_actual_sin_hora = fecha_actual.date()

    # Verificar si ya existe un corte de caja para la fecha actual
    cierre_existente = CierreDeCaja.objects.filter(fecha_cierre__date=fecha_actual_sin_hora).first()
    
    if cierre_existente:
        corte_de_caja_habilitado = True
        # Realizar alguna acción si existe un corte de caja para hoy
    else:
        corte_de_caja_habilitado = False
        # Realizar alguna acción si no existe un corte de caja para hoy
        
    return render(request, 'Corte/indexCorte.html',{'Ventas':Ventas,'total':total,'corte_de_caja_habilitado':corte_de_caja_habilitado,'ventasAbiertas':ventasAbiertas,'fecha_hoy':fecha_hoy})

def cortesPasados(request):
    Cortes = CierreDeCaja.objects.all()
    
    return render(request,'Corte/cortesPasados.html',{'Cortes':Cortes})

def enviarCorreo(request):
    # Obtener la fecha y hora actual
    fecha_actual = timezone.now()

    # Obtener solo la parte de la fecha
    fecha_actual_sin_hora = fecha_actual.date()

    # Verificar si ya existe un cierre de caja para la fecha actual
    cierre_existente = CierreDeCaja.objects.filter(fecha_cierre__date=fecha_actual_sin_hora).first()

    if cierre_existente:
        print("Ya existe un cierre de caja para hoy")
    else:
        # Si no existe un cierre de caja para la fecha actual, recopilar los datos de ventas y crear uno nuevo
        Ventas = Venta.objects.filter(fecha_salida__date=fecha_actual_sin_hora)
        total = sum(venta.total for venta in Ventas)

        # Crear el nuevo objeto CierreDeCaja
        cierre_caja = CierreDeCaja.objects.create(
            fecha_cierre=fecha_actual,
            ventasDelDia=Ventas.count(),
            totalVentas=total
        )

        print("Se ha creado un nuevo cierre de caja para hoy")

    fecha_legible = fecha_actual_sin_hora.strftime("%d/%m/%Y")

    # Marcar las ventas como no editables
    for venta in Ventas:
        venta.editable = False
        venta.save()

    # Generar el texto del correo con los detalles de las ventas del día
    total = 0
    texto = "Ventas del día " + fecha_legible + "\n"

    for venta in Ventas:
        total += venta.total
        texto += "------------------------------\n"
        texto += "Mesa: " + str(venta.mesa) + "\n"
        texto += "Fecha: " + str(venta.fecha_salida.strftime("%H:%M")) + "\n"
        texto += "Total: " + str(venta.total) + "\n"

    texto += "------------------------------\n"
    texto += "Total de las ventas de hoy:  $" + str(total)

    # Configuración del correo electrónico
    email_reciver = "d1360.audi@gmail.com"
    email_reciver2 = "ale_0908@hotmail.com"

    email_sender = "cuentapruebanapoli@gmail.com"
    email_password = "spsy apcz sewh rmbc"  # Asegúrate de que esta contraseña sea la correcta
    subject = "Cierre de caja del día: " + fecha_legible
    body = texto

    # Crear el mensaje de correo
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = [email_reciver,email_reciver2]  # Lista de destinatarios , 
    em['Subject'] = subject
    em.set_content(body)

    # Iniciar sesión en el servidor SMTP y enviar el correo
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

    return redirect('Corte:corteDeCajaIndex')