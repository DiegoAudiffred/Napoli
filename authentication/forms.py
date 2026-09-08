from django import forms
from db.models import ROLES 
from django.contrib.auth.forms import UserCreationForm
from db.models import User



class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','phone_number','url','rol']
        
