from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users_pfps')
    balance = models.IntegerField(default=0)
    description = models.TextField(max_length=999, default='Hello, Im new user!')
    # list of rates
    rates = models.IntegerField(default=5)
    rates_amount = models.IntegerField(default=1)