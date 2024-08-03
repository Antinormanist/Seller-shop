from django.db import models

from user.models import User

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=20)
    price = models.SmallIntegerField()
    description = models.TextField(max_length=999)
    image = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(to='Categories', on_delete=models.SET_NULL)
    seller = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        db_table = 'products'
        
        
class Categories(models.Model):
    name = models.CharField(max_length=20)