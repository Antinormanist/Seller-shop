from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate

from .utils import create_token, EMAIL_MESSAGE, AUTHENTICATION_MESSAGE
from .models import User
from .forms import UserRegistrationForm

# Create your views here.
def sign_in(request):
    context = {
        'title': 'Sign in'
    }
    return render(request, 'user/sign-in.html', context)


def sign_in_mail(request):
    token = create_token()
    if request.POST.get('success'):
        print('suces')
        eol = request.POST.get('eol')
        eol_type = request.POST.get('eol_type')
        password = request.POST.get('password')
        if eol_type == 'login':
            username = eol
        else:
            username = User.objects.filter(email=eol)[0]
            if username:
                username = username.username
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        
    else:
        eol = request.POST.get('eol')
        eol_type = request.POST.get('eol_type')
        password = request.POST.get('password')
        password = request.POST.get('password')
        if eol_type == 'login':
            username = eol
        else:
            username = User.objects.filter(email=eol)[0]
            if username:
                username = username.username
        user = authenticate(username=username, password=password)
        if user:
            email = EmailMessage(
                'Authentication on seller shop',
                AUTHENTICATION_MESSAGE.format(username=user, code=token),
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.fail_silently = False
            email.send()
            return JsonResponse({'code': token})
            # login(request, user)
    return JsonResponse({'success': 1, 'status': 200})

def sign_up(request):
    context = {
        'title': 'Sign up'
    }
    return render(request, 'user/sign-up.html', context)


def sign_up_code(request):
    if request.POST:
        token = create_token()
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password1': request.POST.get('password1'),
            'password2': request.POST.get('password2'), 
        }
        form = UserRegistrationForm(data)
        if form.is_valid():
            email = EmailMessage(
                'Registration on seller shop',
                EMAIL_MESSAGE.format(username=request.POST['username'], code=token),
                settings.EMAIL_HOST_USER,
                [request.POST['email']],
            )
            
            email.fail_silently = False
            email.send()
            return JsonResponse({'code': token, 'status': 200})
    return JsonResponse({'hello': 1})


def sign_up_mail(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return HttpResponse('<h1>COngrats</h1>')
    return HttpResponse('something is wrong')


@login_required
def profile(request):
    pass