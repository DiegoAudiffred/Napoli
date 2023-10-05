from django import forms
from db.models import Extras, Ingredientes, Menu, Venta, VentaMenu
from django.forms import ImageField, ModelChoiceField, ModelMultipleChoiceField, MultipleChoiceField
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class createVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ['cliente','empleado','total','fecha_compra', 'is_open']
      

    def __init__(self, *args, **kwargs):
        super(createVentaForm, self).__init__(*args, **kwargs)
    
    
        self.fields['cliente'].required = False
        self.fields['cliente'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Nombre que aparece en el menú*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['empleado'].required = False
        self.fields['empleado'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':'Precio en el menú*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['total'].required = False
        self.fields['total'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Breve descripción*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        
        self.fields['fecha_compra'].required = False
        self.fields['fecha_compra'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Categoría*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['is_open'].required = False 
        self.fields['is_open'].default = True 

        self.fields['is_open'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Ingredientes*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


class modifyVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ['cliente']
    def __init__(self, *args, **kwargs):
        super(modifyVentaForm, self).__init__(*args, **kwargs)
        
        self.fields['cliente'].required = False

class modifyMesaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ['mesa']
    def __init__(self, *args, **kwargs):
        super(modifyMesaForm, self).__init__(*args, **kwargs)
        
        self.fields['mesa'].required = False
        self.fields['mesa'].widget.attrs.update({'class':'border border-0' })


        
class VentaMenuForm(forms.ModelForm):
      

    def __init__(self, *args, **kwargs):
        super(VentaMenuForm, self).__init__(*args, **kwargs)
    
    
        self.fields['venta'].required = False

        self.fields['menu'].required = False
        self.fields['menu'].widget.attrs.update({'class':'form-control shadow-none   px-2 py-1','placeholder':' Breve descripción*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


        self.fields['cantidad'].required = False
        self.fields['cantidad'].widget.attrs.update({'class':'form-control shadow-none border border-0   px-2 py-1 ','placeholder':' Cantidad*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        
        self.fields['observaciones'].required = False
        self.fields['observaciones'].widget.attrs.update({'class':'form-control shadow-none border border-0  px-2 py-1 ','placeholder':' Observaciones en la preparación*','rows':'5', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


        self.fields['totalfinal'].required = False
        self.fields['totalfinal'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Breve descripción*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['extras'].required = False 
        self.fields['extras'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Ingredientes*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        self.fields['extras'].widget = forms.CheckboxSelectMultiple()
        self.fields['extras'].queryset = Extras.objects.all()

        
        self.fields['familiar'].widget.attrs.update({'style':'height:30px;width:30px','class':'' })
        self.fields['media_orden'].widget.attrs.update({'style':'height:30px;width:30px','class':'' })
        
        self.fields['pizza_mitad'].required = False
        self.fields['pizza_mitad'].widget.attrs.update({'class':'form-control shadow-none   px-2 py-1','placeholder':' Breve descripción*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })


    class Meta:
        model = VentaMenu
        fields = ['venta','menu','cantidad','totalfinal','observaciones','extras','media_orden','familiar','pizza_mitad']


        
 


