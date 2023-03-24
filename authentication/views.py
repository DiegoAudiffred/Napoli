from django.http import HttpResponse
from django.shortcuts import render
from db.models import *

# Create your views here.
def index(request):
    users = User.objects.all()
    return render(request, 'authentication/index.html',{"users":users})

