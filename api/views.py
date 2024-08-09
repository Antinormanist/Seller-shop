from django.shortcuts import render, get_object_or_404

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer, ProductSerializer
from user.models import User
from main.models import Products
# Create your views here.

@api_view(['GET'])
def user_view(request, id=None):
    if request.method == 'GET':
        if id:
            serializer = UserSerializer(get_object_or_404(User, id=int(id)))
        else:
            serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)
    
    
@api_view(['GET'])
def product_view(request, id=None):
    if request.method == 'GET':
        if id:
            serializer = ProductSerializer(get_object_or_404(Products, id=int(id)))
        else:
            serializer = ProductSerializer(Products.objects.all(), many=True)
        return Response(serializer.data)
    
    
def docs(request):
    context = {
        'title': 'API documentation'
    }
    return render(request, 'ap/api.html', context)