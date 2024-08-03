from django.shortcuts import render, HttpResponse

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