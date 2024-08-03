from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users_pfps')
    balance = models.IntegerField()
    # list of rates
    rates = ArrayField(models.DecimalField(max_digits=3, decimal_places=1))