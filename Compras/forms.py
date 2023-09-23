
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
