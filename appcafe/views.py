from django.shortcuts import render
from .models import Cafe
from .forms import ProductForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

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