from django import forms
from db.models import CompraIngredientes, Compras, User, Ingredientes, VentaMenu
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
        self.fields['fecha_compra'].required = False




class VentaMenuForm(forms.ModelForm):

    class Meta:
        model = VentaMenu
        fields = ['venta','menu','cantidad','totalfinal','observaciones']
      

    def __init__(self, *args, **kwargs):
        super(VentaMenuForm, self).__init__(*args, **kwargs)
    
    
        self.fields['venta'].required = False

        self.fields['menu'].required = False
        self.fields['menu'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1','placeholder':' Breve descripción*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


        self.fields['cantidad'].required = False
        self.fields['cantidad'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 ','placeholder':' Cantidad*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        
        self.fields['observaciones'].required = False
        self.fields['observaciones'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 ','placeholder':' Observaciones en la preparación*','rows':'5', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


        self.fields['totalfinal'].required = False
        self.fields['totalfinal'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Breve descripción*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


        
class CompraIngredientesForm(forms.ModelForm):

    class Meta:
        model = CompraIngredientes
        fields = ['compra','ingrediente','cantidad','totalfinal']
      

    def __init__(self, *args, **kwargs):
        super(CompraIngredientesForm, self).__init__(*args, **kwargs)
    
    
        self.fields['compra'].required = False

        self.fields['ingrediente'].required = False
        self.fields['ingrediente'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1','placeholder':' Breve descripción*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


        self.fields['cantidad'].required = False
        self.fields['cantidad'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 ','placeholder':' Cantidad*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        
        self.fields['totalfinal'].required = False
        self.fields['totalfinal'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 ','placeholder':' Observaciones en la preparación*','rows':'5', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })




class ActualizarCampoForm(forms.ModelForm):
    codigos = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),  # Textarea multilínea
        label='Ingresar códigos (separados por líneas)',
        required=False  # Puede hacerse requerido si es necesario
    )

    class Meta:
        model = Ingredientes
        fields = ['codigo_de_barras']  # Campos que se mostrarán en el formulario
