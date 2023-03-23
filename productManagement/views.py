import json
from django.shortcuts import render, redirect, redirect
from db.models import *
from django.core.mail import send_mail
from django.db.models import Q
import math
import random

# Create your views here.
def productManagementList(request):
    return render(request, 'productManagement.html')