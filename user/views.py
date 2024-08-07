from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.core.cache import cache

import stripe

from .utils import create_token, EMAIL_MESSAGE, AUTHENTICATION_MESSAGE, DELETE_MESSAGE
from .models import User, Commentary, Chat
from .forms import UserRegistrationForm
from main.models import Products, Categories
from .tasks import send_mail

REDIS_EMAIL_KEY = 'email-key-for-id-{id}'

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
            cache.set(REDIS_EMAIL_KEY.format(id=user.id), 'exists', timeout=60 * 60 * 24 * 7)
            login(request, user)
            return JsonResponse({'success': 1, 'status': 200})
        
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
            if cache.get(REDIS_EMAIL_KEY.format(id=user.id)):
                login(request, user)
                return JsonResponse({'cache': True, 'status': 200})
            
            send_mail.delay_on_commit(
                head='Authentication on seller shop',
                body=AUTHENTICATION_MESSAGE.format(username=user, code=token),
                sender=settings.EMAIL_HOST_USER,
                getters=[user.email]
            )
            
            return JsonResponse({'code': token})
    return JsonResponse({'status': 400, 'error': 1})

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
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'status': 400})
        form = UserRegistrationForm(data)
        if form.is_valid():
            
            send_mail.delay_on_commit(
                head='Registration on seller shop',
                body=EMAIL_MESSAGE.format(username=request.POST['username'], code=token),
                sender=settings.EMAIL_HOST_USER,
                getters=[request.POST['email']]
            )
            
            return JsonResponse({'code': token, 'status': 200})
    return JsonResponse({'hello': 1})


def sign_up_mail(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        user = form.save()
        cache.set(REDIS_EMAIL_KEY.format(id=user.id), 'exists', timeout=60 * 60 * 24 * 7)
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
        
        # CONTINUE WITH CELERY
        send_mail.delay_on_commit(
            head='Deletion and account on seller shop',
            body=DELETE_MESSAGE.format(username=request.user.username, code=token),
            sender=settings.EMAIL_HOST_USER,
            getters=[request.user.email]
        )
        
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
        print(comment)
        if request.user.username not in comment.took:
            comment.people_dislike = comment.people_dislike + 1
            comment.took.append(request.user.username)
            comment.save()
            return JsonResponse({'success': True, 'status': 200})
    return JsonResponse({'error': True, 'status': 400})


@login_required
def product_add(request):
    if request.POST:
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        if name and price and price.isdigit() and description and image and category:
            Products.objects.create(
                name=name,
                price=int(price),
                description=description,
                image=image,
                category=Categories.objects.get(name=category),
                seller=request.user,
            )
        
    context = {
        'title': 'Product add'
    }
    return render(request, 'user/product-add.html', context)


@login_required
def seller_profile(request, seller_id):
    user = User.objects.get(id=seller_id)
    if user == request.user:
        return redirect(reverse('user:profile'))
    if request.POST:
        comment = request.POST.get('commentary')
        rate = request.POST.get('rate')
        if comment and rate:
            Commentary.objects.create(
                comment_user=request.user,
                relate_user=user,
                rate=int(rate),
                comment=comment,
                took=[request.user.username]
            )
            user.rates += int(rate)
            user.rates_amount += 1
            user.save()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(Commentary.objects.filter(relate_user=user), 5)
    page_obj = paginator.get_page(page)
    
    context = {
        'title': 'Seller\'s profile',
        'user': user,
        'page_obj': page_obj,
    }
    return render(request, 'user/seller_profile.html', context)


@login_required
def chats(request):
    context = {
        'title': 'Chats',
        'chats': Chat.objects.filter(main_user=request.user).distinct('relate_user__username')
    }
    return render(request, 'user/chats.html', context)


@login_required
def chat_detail(request, seller_id):
    relate = User.objects.get(id=int(seller_id))
    if request.GET.get('block'):
        Chat.objects.filter(main_user=request.user, relate_user=relate).update(
            relate_is_blocked=True
        )
        Chat.objects.filter(main_user=relate, relate_user=request.user).update(
            main_is_blocked=True
        )
    if request.GET.get('unblock'):
        Chat.objects.filter(main_user=request.user, relate_user=relate).update(
            relate_is_blocked=False
        )
        Chat.objects.filter(main_user=relate, relate_user=request.user).update(
            main_is_blocked=False
        )
    
    if message := request.POST.get('user-message'):
        if not Chat.objects.filter(main_user=request.user, relate_user=relate).first().relate_is_blocked:
            Chat.objects.create(
                main_user=request.user,
                relate_user=relate,
                comment=message,
                comment_user=request.user
            )
            Chat.objects.create(
                main_user=relate,
                relate_user=request.user,
                comment=message,
                comment_user=request.user
            )
    a_chats = Chat.objects.filter(main_user=request.user, relate_user=User.objects.get(id=int(seller_id)))
    context = {
        'title': 'Chat',
        'chats': a_chats,
        'main_blocked': a_chats.first().main_is_blocked,
        'relate_blocked': a_chats.first().relate_is_blocked,
        'relate_name': a_chats.first().relate_user.username,
    }
    return render(request, 'user/chat_detail.html', context)