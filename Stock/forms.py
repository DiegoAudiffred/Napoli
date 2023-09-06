from django import forms
from db.models import Compras, User, Ingredientes
from django.forms import ImageField
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class createStockForm(forms.ModelForm):

    class Meta:
        model = Ingredientes
        fields = ['nombre','precio','unidad','cantidad','fecha_compra']
        

    def __init__(self, *args, **kwargs):
        super(createStockForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].required = False
        self.fields['nombre'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Nombre*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['precio'].required = True
        self.fields['precio'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':'Precio*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['unidad'].required = True
        self.fields['unidad'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Unidad*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


        self.fields['cantidad'].required = True
        self.fields['cantidad'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Cantidad*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        
        self.fields['fecha_compra'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Última fecha*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        self.fields['fecha_compra'].required = True


class createCompraForm(forms.ModelForm):

    class Meta:
        model = Compras
        fields = ['ingrediente','cantidades','fecha','precio']
        

    def __init__(self, *args, **kwargs):
        super(createCompraForm, self).__init__(*args, **kwargs)

        self.fields['ingrediente'].required = True
        self.fields['ingrediente'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Nombre*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['cantidades'].required = True
        self.fields['cantidades'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':'Cantidad comprada*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['precio'].required = True
        self.fields['precio'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Precio de compra*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })



        
        self.fields['fecha'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':'Fecha de compra*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        self.fields['fecha'].required = True


