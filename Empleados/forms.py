from django import forms
from db.models import User
from django.forms import ImageField
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class createEmployeeForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email','first_name','phone_number','url', 'rol','password1','password2']
        

    def __init__(self, *args, **kwargs):
        super(createEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

        self.fields['email'].required = False
        self.fields['email'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary border border-0','placeholder':' Correo*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':'Nombre del empleado*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['phone_number'].required = True
        self.fields['phone_number'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Número telefónico*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


        self.fields['url'].required = False
        self.fields['url'].widget.attrs.update({'onchange':'loadFile(event);'})

        
        self.fields['rol'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Rol del empleado*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['rol'].required = True



