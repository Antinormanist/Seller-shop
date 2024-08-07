from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator

import stripe

from .utils import create_token, EMAIL_MESSAGE, AUTHENTICATION_MESSAGE, DELETE_MESSAGE
from .models import User, Commentary
from .forms import UserRegistrationForm

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

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
def balance(request):
    session_id = request.GET.get('session_id')
    if session_id:
        print("session yes")
        session = stripe.checkout.Session.retrieve(session_id)
        if session and session['payment_status'] == 'paid':
            print("balance")
            request.user.balance += int(request.GET['amount'])
            request.user.save()
            return redirect(reverse('user:balance'))
    elif request.POST:
        amount = request.POST.get('amount')
        if amount and amount.isdigit():
            amount = int(amount)
            session_data = {
                'mode': 'payment',
                'success_url': request.build_absolute_uri(reverse('user:balance')) + '?session_id={CHECKOUT_SESSION_ID}&amount=' + f'{amount}',
                'cancel_url': request.build_absolute_uri(reverse('user:balance')),
                'line_items': [{
                    'price_data': {
                        'unit_amount': amount * 100,
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Top up balance'
                        }
                    },
                    'quantity': 1
                }],
            }
            
            session = stripe.checkout.Session.create(**session_data)
            # TOP UP BALANCE
            return redirect(session.url, code=303)
        
    context = {
        'title': 'Top up balance'
    }
    return render(request, 'user/balance.html', context)


@login_required
def profile(request):
    page = int(request.GET.get('page', 1))
    paginator = Paginator(Commentary.objects.filter(relate_user=request.user), 5)
    page_obj = paginator.get_page(page)
    
    context = {
        'title': 'Profile',
        'page_obj': page_obj,
    }
    
    if request.POST:
        name = request.POST.get('bio-name')
        description = request.POST.get('bio-desc')
        avatar = request.FILES.get('bio-ava')
        if name and description and avatar:
            user = User.objects.filter(username=request.user.username)
            request.user.username = name
            request.user.description = description
            request.user.image = avatar
            request.user.save()
            request.user.refresh_from_db()
    return render(request, 'user/profile.html', context)


def profile_code(request):
    token = create_token()
    if request.POST.get('success'):
        if request.user.is_authenticated:
            request.user.delete()
        return JsonResponse({'success': True, 'status': 200})
        
    if request.POST.get('need_code'):
        email = EmailMessage(
            'Deletion and account on seller shop',
            DELETE_MESSAGE.format(username=request.user.username, code=token),
            settings.EMAIL_HOST_USER,
            [request.user.email]
        )
        email.fail_silently = False
        email.send()
        return JsonResponse({'code': token})
    return JsonResponse({'error': True})


def user_logout(request):
    logout(request)
    return redirect(reverse('main:welcome'))


def like(request):
    id = request.POST.get('comment_id')
    if id:
        comment = Commentary.objects.get(id=int(id))
        if request.user.username not in comment.took:
            comment.people_like = comment.people_like + 1
            comment.took.append(request.user.username)
            comment.save()
            return JsonResponse({'success': True, 'status': 200})
    return JsonResponse({'error': True, 'status': 400})


def dislike(request):
    id = request.POST.get('comment_id')
    if id:
        comment = Commentary.objects.get(id=int(id))
        if request.user.username not in comment.took:
            comment.people_dislike = comment.people_dislike + 1
            comment.took.append(request.user.username)
            comment.save()
            return JsonResponse({'success': True, 'status': 200})
    return JsonResponse({'error': True, 'status': 400})