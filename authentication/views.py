from django.http import HttpResponse
from django.shortcuts import redirect, render
from db.models import *
from authentication.forms import createUserForm
# Create your views here.
def index(request):
    users = request.user
    return render(request, 'authentication/index.html',{"users":users})

def createAccount(request):
    user = request.user
    if request.method == "POST":
        form = createUserForm(request.POST, request.FILES)
        if form.is_valid():
            print("Entro")
            newuser = form.save()
            newuser.save()
            return redirect('authentication:index')         

        else:
            return render(request, 'authentication/createAccount.html',{'form':form})
    form = createUserForm()
    return render(request, 'authentication/createAccount.html',{'form':form})

    owner = request.user
    totalproperties = Property.objects.filter(user=owner).count()
    if request.method == "POST":
        form = addPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            print("Entro")
            property = form.save()
            property.save()
            images = request.FILES.getlist('propertyImages')
            if len(images) > 0:
                for imageFile in images:
                    image = Image(url=imageFile, property=property)
                    image.save()
            return redirect('realStateProfile:propertiesList',owner.id)         
        else:
            print(form.cleaned_data)
            print("no entro")
            return render(request,"realStateProfile/propertyList.html", {
        "profile": owner,
        "form":form,
        "totalproperties":totalproperties,
     })