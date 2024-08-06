from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-in-mail/', views.sign_in_mail, name='sign-in-mail'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-up-code/', views.sign_up_code, name='sign-up-code'),
    path('sign-up-mail/', views.sign_up_mail, name='sign-up-mail'),
    path('balance/', views.balance, name='balance')
]