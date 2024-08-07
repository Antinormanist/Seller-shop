from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-in-mail/', views.sign_in_mail, name='sign-in-mail'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-up-code/', views.sign_up_code, name='sign-up-code'),
    path('sign-up-mail/', views.sign_up_mail, name='sign-up-mail'),
    path('balance/', views.balance, name='balance'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('email-code/', views.profile_code, name='email-code'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('product-add/', views.product_add, name='product-add'),
    path('seller-profile/<int:seller_id>/', views.seller_profile, name='seller-profile'),
    path('chats/', views.chats, name='chats'),
]