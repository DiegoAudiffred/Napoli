from django import forms
from db.models import ROLES 
from django.contrib.auth.forms import UserCreationForm
from db.models import Cliente



class createCliente(forms.Form):
    class Meta:
        model = Cliente
        fields = ['first_name','last_name','total_compras','total_gastado']
        
    def __init__(self, *args, **kwargs):
        super(createCliente, self).__init__(*args, **kwargs)
   
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
