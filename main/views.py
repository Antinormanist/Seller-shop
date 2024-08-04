from django.shortcuts import render, HttpResponse

from .models import Products, Categories
from .utils import q_search

# Create your views here.
def welcome(request):
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
            products.filter(q)
            
    if request.method == 'GET':
        if (price := request.GET.get('price')):
            if price == 'asc':
                products.order_by('price')
            else:
                products.order_by('-price')
        if (date := request.GET.get('date')):
            if date == 'asc':
                products.order_by('created_at')
            else:
                products.order_by('-created_at')
        if (price := request.GET.get('first-range-price')):
            products.filter(price__gte=int(price))
        if (price := request.GET.get('second-range-price')):
            products.filter(price__lte=int(price))
    
    context = {
        'title': 'Goods',
        'prods': products,
        'categories': Categories.objects.all(),
    }
    return render(request, 'main/goods_page.html', context)