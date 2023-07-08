from django import forms
from db.models import ROLES 
from django.contrib.auth.forms import UserCreationForm
from db.models import User



class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','phone_number','url','rol']
        
    def __init__(self, *args, **kwargs):
        super(createUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'class':'rounded-pill'})
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['url'].required = True
        self.fields['rol'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
