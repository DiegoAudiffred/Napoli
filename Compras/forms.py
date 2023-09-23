
from django import forms
from db.models import CompraIngredientes, Compras, User, Ingredientes, VentaMenu
from django.forms import ImageField
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class createCompraForm(forms.ModelForm):

    class Meta:
        model = Compras
        fields = ['fecha','comprador','metodo','ticket','total_comprado','numero_factura','proovedor']
        

  
    def __init__(self, *args, **kwargs):
        super(createCompraForm, self).__init__(*args, **kwargs)

        self.fields['fecha'].required = False
        self.fields['total_comprado'].required = False
        self.fields['comprador'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary border border-0','placeholder':' Correo*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        self.fields['metodo'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary border border-0','placeholder':' Correo*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        self.fields['numero_factura'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary border border-0','placeholder':' Número de factura*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        self.fields['proovedor'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary border border-0','placeholder':' Correo*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
      