from django import forms
from db.models import Ingredientes, Menu
from django.forms import ImageField, ModelChoiceField, ModelMultipleChoiceField, MultipleChoiceField
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_select2.forms import Select2MultipleWidget

class createMenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['nombre','precio','descripcion','categoria', 'ingredientes','url']
      

    def __init__(self, *args, **kwargs):
        super(createMenuForm, self).__init__(*args, **kwargs)
  
        self.fields['nombre'].required = False
        self.fields['nombre'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Nombre que aparece en el menú*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['precio'].required = True
        self.fields['precio'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':'Precio en el menú*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['descripcion'].required = True
        self.fields['descripcion'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Breve descripción*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        
        self.fields['categoria'].required = True
        self.fields['categoria'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Categoría*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })

        self.fields['ingredientes'].required = True 
        self.fields['ingredientes'].widget.attrs.update({'class':'form-control shadow-none bg-corporateTan200  px-2 py-1 text-primary','placeholder':' Ingredientes*','rows':'1', 'aria-label':'Username','aria-describedby':'basic-addon1','style':'border-left:none', })
        self.fields['ingredientes']= ModelMultipleChoiceField (widget=forms.CheckboxSelectMultiple,queryset=Ingredientes.objects.all())


     

        self.fields['url'].required = False
        self.fields['url'].widget.attrs.update({'onchange':'loadFile(event);'})

        
 


