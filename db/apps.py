from django.apps import AppConfig
from django.db.models.signals import post_migrate

MESAS = [
    "1A", "1B", "2", "3", "4", "5", "6", "7", "8",
    "T2", "T3", "T4", "T5", "T6", "T6A", "T6B",
    "8A", "8B", "9A", "Para llevar 1", "Para llevar 2" , "Para llevar 3", "Para llevar 4","Para llevar 5","Donaciones"
]

def crear_mesas_predeterminadas(sender, **kwargs):
    from .models import Mesa
    for nombre_mesa in MESAS:
        Mesa.objects.get_or_create(nombre=nombre_mesa)

class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'

    def ready(self):
        post_migrate.connect(crear_mesas_predeterminadas, sender=self)