import datetime
from email.message import EmailMessage
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from Ventas.forms import VentaMenuForm, createVentaForm, modifyMesaForm, modifyVentaForm, modifyVentaMenuOrder,VentaMenuFormDireccion
from db.models import Cliente, Menu, Mesa, User, Venta, VentaMenu,Extras
from django.db.models import Q
from datetime import date, datetime, timezone
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import QueryDict
from decimal import Decimal
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
#import win32print
#import win32ui
import os
import ssl
#import win32api
import PyPDF2
import subprocess
from django.core.files import File
from io import BytesIO
#import cups
import subprocess
import tempfile

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
def ticketsIndex(request):


    return render(request, 'tickets/ticketsIndex.html')

