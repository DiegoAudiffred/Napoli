from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Menu)
admin.site.register(Ingredientes)
admin.site.register(Compras)
admin.site.register(Venta)
admin.site.register(VentaMenu)
admin.site.register(Proovedores)
admin.site.register(CompraIngredientes)
admin.site.register(Extras)
admin.site.register(Mesa)
admin.site.register(RegistroCambiosVentaMenu)
