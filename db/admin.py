from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Menu)
admin.site.register(Ingredientes)
admin.site.register(Compras)
