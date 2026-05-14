from django.shortcuts import render, redirect
from .models import Producto
from django.contrib.auth import authenticate, login, logout

def home(request):
    products = Producto.objects.all()
    return render(request, 'home.html', {'products': products})

def menu(request):
    products = Producto.objects.all()
    return render(request, 'menu.html', {'products': products})

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
         })
    return render(request, 'login.html')

def logout_usuario(request):
    logout(request)
    return redirect('home')