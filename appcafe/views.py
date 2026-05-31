from django.shortcuts import render
from .models import Cafe
from .forms import ProductForm
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def add_cafe(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'add_cafe.html', {'form': ProductForm(), 'success': True})
    else:
        form = ProductForm()
    return render(request, 'add_cafe.html', {'form': form})

def cafe_list(request):
    cafes = Cafe.objects.all()
    return render(request, 'cafe_list.html', {'cafes': cafes})

def menu(request):
    cafes = Cafe.objects.all()
    return render(request, 'menu.html', {'cafes': cafes})

def cart(request):
    return render(request, 'carrito.html')

@csrf_protect
def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    return render(request, 'logout.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')



