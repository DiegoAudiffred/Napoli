from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
import authentication
from db.models import *
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.contrib.auth.decorators import user_passes_test,login_required

@login_required(login_url='authentication:login')
def index(request):
    users = request.user
    return render(request, 'registration/index.html',{"users":users})

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']  
        users = authenticate(request,email=email,password=password)
        if users is not None:
            login(request,users)
            
            return redirect('authentication:index')
        else:
            messages = "Error en la credenciales, inténtelo más tarde"
            return redirect('authentication:index')
    return render(request,"registration/login.html",{'form':form})

def signout(request):

    logout(request)
    return redirect('authentication:signin')


      