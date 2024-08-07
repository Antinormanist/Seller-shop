from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Products, Categories
from .utils import q_search

# Create your views here.
def welcome(request):
    if request.user.is_authenticated:
        return redirect(reverse('user:profile'))
    context = {
        'title': 'Welcome',
    }
    return render(request, 'main/welcome.html', context)


def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'main/about.html', context)



def goods_page(request, cat_id=None):
    if cat_id:
        products = Products.objects.filter(category__id=cat_id)
    else:
        products = Products.objects.all()
        
    if request.method == 'POST':
        search = request.POST.get('search')
        if search:
            q = q_search(search)
            products = products.filter(q)
            
    if request.method == 'GET':
        if (price := request.GET.get('price')):
            if price == 'asc':
                products = products.order_by('price')
            else:
                products = products.order_by('-price')
        if (date := request.GET.get('date')):
            if date == 'asc':
                products = products.order_by('created_at')
            else:
                products = products.order_by('-created_at')
        if (price := request.GET.get('first-range-price')):
            products = products.filter(price__gte=int(price))
        if (price := request.GET.get('second-range-price')):
            products = products.filter(price__lte=int(price))
    
    context = {
        'title': 'Goods',
        'prods': products,
        'categories': Categories.objects.all(),
    }
    return render(request, 'main/goods_page.html', context)


@login_required
def product_detail(request, prod_id):
    product = Products.objects.get(id=prod_id)
    product_asq = Products.objects.filter(id=prod_id)
    if request.GET.get('sold'):
        if request.user == product.seller:
            pass
        else:
            if request.user.balance >= product.price:
                request.user.balance -= product.price
                request.user.save()
                product.seller.balance += product.price
                product.seller.save()
                product_asq.delete()
                return redirect(reverse('main:goods_page'))
            
    if request.GET.get('del'):
        if request.user == product.seller:
            product_asq.delete()
            return redirect(reverse('main:goods_page'))
            
    has_changes = False
    if name := request.POST.get('name'):
        product_asq.update(name=name)
        has_changes = True
    if price := request.POST.get('price'):
        product_asq.update(price=int(price))
        has_changes = True
    if description := request.POST.get('description'):
        product_asq.update(description=description)
        has_changes = True
        
    if has_changes:
        return redirect(request.path)
        
    rate = round(product.seller.rates / product.seller.rates_amount, 1)
    context = {
        'title': 'Product detail',
        'prod': product,
        'rate': rate,
    }
    return render(request, 'main/product-detail.html', context)


@login_required
def product_add(request):
    if request.POST:
        image = request.FILES.get('image', '')
        name = request.POST.get('name', '')
        price = request.POST.get('price', '')
        description = request.POST.get('description', '')
        category = request.POST.get('category')
        if category:
            category = Categories.objects.get(name=category)
        if name and price:
            Products.objects.create(
                image=image,
                name=name,
                price=int(price),
                description=description,
                category=category,
                seller=request.user
            )
    
    context = {
        'title': 'Product add'
    }
    return render(request, 'main/product-add.html', context)


@login_required
def user_products(request):
    context = {
        'title': 'Your products',
        'prods': Products.objects.filter(seller=request.user)
    }
    return render(request, 'main/user-products.html', context)