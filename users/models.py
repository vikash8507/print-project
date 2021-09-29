from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   points = models.IntegerField(default=0)
   name = models.CharField(max_length=255, default='')
   phone = models.CharField(max_length=10, default='')
   shop_name = models.CharField(max_length=255, default='')
   shop_address = models.CharField(max_length=255, default='')