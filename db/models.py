from datetime import timezone
import decimal
import math
import urllib
import json
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from django.utils import timezone

# Create your models here.


ROLES = [
    ("Dueña/o", "Dueña/o"),
    ("Cocinera/o", "Cocinera/o"),
    ("Mesera/o", "Mesera/o"),
    ("Admin", "Admin"),
   
]

UNIDADES = [
    ("K", "Kilos"),
    ("L", "Litros"),
    ("ml", "mililitros"),
    ("kg", "miligramos"),
    ("U", "unidad"),

]

CATEGORIA = [
    ("Entradas", "Entradas"),
    ("Ensaladas", "Ensaladas"),
    ("Pastas", "Pastas"),
    ("Carnes", "Carnes"),
    ("Postres", "Postres"),
    ("Bebidas", "Bebidas"),
    ("Pizza", "Pizza"),
    ("Especialidad", "Especialidad"),

]

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Cliente(models.Model):
    first_name = models.CharField("Nombre", max_length=200)
    total_compras= models.IntegerField(null=True,blank=True,default=0)
    total_gastado= models.FloatField(null=True,blank=True,default=0)
    email = models.EmailField('Correo electrónico', unique=True, blank=True, null=True)
    phone_number = models.CharField("Teléfono", max_length=15, unique=True, null=True,blank=True)
    is_active= models.BooleanField(default=True)
    
def _str_(self):
        return self.first_name

class User(AbstractUser):

    username = None
    email = models.EmailField('Correo electrónico', unique=True, blank=True, null=True)
    first_name = models.CharField("Nombre", max_length=200, null=True, blank=True)
    phone_number = models.CharField("Teléfono", max_length=15, unique=True, null=True)
    url = models.ImageField(upload_to="uploads/gallery/",null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    rol = models.CharField( 
        choices=ROLES, max_length=20)
    objects = UserManager()
    is_active= models.BooleanField(default=True)


    def _str_(self):
        return self.email, self.first_name
    




class Bebidas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField( 
        choices=CATEGORIA, max_length=20)  
    url = models.ImageField(upload_to="uploads/gallery/",null=True,blank=True)

    def __str__(self):
        return self.nombre





class Ingredientes(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    unidad = models.CharField(choices=UNIDADES, max_length=20)
    cantidad = models.DecimalField(max_digits=8,decimal_places=2,default=0,null=False)
    fecha_compra = models.DateField(default=timezone.now())  # Establecer la fecha actual como valor predeterminado
    def __str__(self):
        return self.nombre
    

class Compras(models.Model):
    ingrediente = models.ForeignKey(Ingredientes, on_delete=models.CASCADE)
    cantidades = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    fecha = models.DateTimeField(default=timezone.now())  # Establecer la fecha actual como valor predeterminado
    precio = models.DecimalField(max_digits=8, decimal_places=2)



class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField( 
        choices=CATEGORIA, max_length=20)
    url = models.ImageField(upload_to="uploads/gallery/")
    ingredientes = models.ManyToManyField(Ingredientes)

    def __str__(self):
        return self.nombre
