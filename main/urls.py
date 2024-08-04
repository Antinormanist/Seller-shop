from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('goods/', views.goods_page, name='goods_page'),
    path('goods/<int:cat_id>', views.goods_page, name='goods_page'),
    path('product-detail/<int:prod_id>', views.product_detail, name='product-detail')
]