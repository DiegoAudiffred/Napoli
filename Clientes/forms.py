from django import forms
from db.models import User, Cliente
from django.forms import ImageField
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class createClientForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['email','nombre','total_compras','total_gastado','phone_number']
        

    def __init__(self, *args, **kwargs):
        super(createClientForm, self).__init__(*args, **kwargs)
 

        self.fields['email'].required = False
        self.fields['email'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Correo*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['nombre'].required = True
        self.fields['nombre'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':'Nombre del empleado*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['phone_number'].required = False
        self.fields['phone_number'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Número telefónico*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })







