from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from db.models import Cliente, Ingredientes, User
from authentication.forms import createUserForm

def stockIndex(request):
    totalStock = Ingredientes.objects.all()
    return render(request, 'Stock/stockIndex.html',{'totalStock':totalStock})