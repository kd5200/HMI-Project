from django.db import models

class weather(models.Model):
    condition = models.CharField(max_length=50)
    city = models.CharField(max_length=100)

class city(models.Model):
    states = models.CharField(max_length=150)
    cities = models.CharField(max_length=150)
    

# TBD
# Create your models here.
