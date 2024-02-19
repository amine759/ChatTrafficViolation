from django.db import models


class Amendes(models.Model):
    classe = models.CharField(max_length=20)
    category = models.CharField(max_length=400)


# Create your models here.
