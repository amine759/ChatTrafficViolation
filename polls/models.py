from django.db import models


class Traffic(models.Model):
    classe= models.CharField(max_length=200)
    amende= models.CharField(max_length=200)
    key=models.CharField(max_length=200)

# Create your models here.
