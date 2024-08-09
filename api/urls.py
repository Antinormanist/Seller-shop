from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('users/', views.user_view, name='user'),
    path('users/<int:id>/', views.user_view, name='user-id'),
    path('prods/', views.product_view, name='prod'),
    path('prods/<int:id>/', views.product_view, name='prod-id')
]