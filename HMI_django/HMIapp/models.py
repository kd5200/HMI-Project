from django.db import models

class weather(models.Model):
    condition = models.CharField(max_length=50)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.condition


# TBD
# Create your models here.
