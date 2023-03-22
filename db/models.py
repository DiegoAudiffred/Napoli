import decimal
import math
import urllib
import json
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
# Create your models here.
class User(AbstractUser):

    
    email = models.EmailField('Correo electrónico', unique=True)
    first_name = models.CharField("Nombre", max_length=200, null=True, blank=True)
    last_name = models.CharField("Apellido", max_length=200, null=True, blank=True)
    address = models.CharField("Dirección", max_length=400, null=True, blank=True)
    phone_number = models.CharField("Teléfono", max_length=15, unique=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def _str_(self):
        return self.email, self.first_name
