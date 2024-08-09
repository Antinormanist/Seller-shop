from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from main.models import Products


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'email',
            'balance',
            'description',
        ]
        
    
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id',
            'name',
            'price',
            'description',
            'created_at'
        ]