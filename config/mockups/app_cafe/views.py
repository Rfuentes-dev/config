from django.shortcuts import render
from .models import Producto

def home(request):
    products = Producto.objects.all()
    return render(request, 'home.html', {'products': products})

def menu(request):
    products = Producto.objects.all()
    return render(request, 'menu.html', {'products': products})