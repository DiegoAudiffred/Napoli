
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Compras.forms import createCompraForm
from Stock.forms import ActualizarCampoForm, CompraIngredientesForm
from db.models import *
from authentication.forms import createUserForm
# Create your views here.
# Create your views here.

def proveedoresIndex(request):

    return render(request, 'Proveedores/indexProveedores.html')