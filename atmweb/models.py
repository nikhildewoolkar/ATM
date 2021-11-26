from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import *
from django.db.models.signals import post_save
class ClientSignUp(models.Model):
    fullname=models.CharField(max_length=50)
    balance=models.CharField(max_length=50)
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=150)
