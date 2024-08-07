from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=21, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users-pfps', default='anonymous_pfp.png')
    balance = models.IntegerField(default=0)
    description = models.TextField(max_length=999, default='Hello, Im new user!')
    # list of rates
    rates = models.IntegerField(default=5)
    rates_amount = models.IntegerField(default=1)


class Commentary(models.Model):
    comment_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='comment_user')
    relate_user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, related_name='relate_user')
    rate = models.SmallIntegerField()
    comment = models.TextField(max_length=999)
    people_like = models.IntegerField(default=0)
    people_dislike = models.IntegerField(default=0)
    took = ArrayField(base_field=models.CharField(max_length=21))
    
    
class Chat(models.Model):
    main_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='main_us')
    relate_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='relate_us')
    comment = models.TextField(max_length=256, default='')
    created_at = models.DateTimeField(auto_now_add=True)