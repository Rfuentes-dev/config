from django.shortcuts import render
from .models import Cafe
from .forms import ProductForm
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

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
    cart_items = request.session.get('cart', [])
    if isinstance(cart_items, list):
        cart_items = cart_items
        request.session['cart'] = cart_items
        request.session.modified = True

    cart_items = []
    total_price = 0

    for item in request.session.get('cart', []):
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)
        cafe = Cafe.objects.filter(id=product_id).first()
        if cafe:
            cart_items.append({
                'name': cafe.name,
                'price': cafe.price,
                'quantity': quantity,
                'total': cafe.price * quantity
            })
            total_price += cafe.price * quantity
    context = {'cart_items': cart_items, 'total': total_price}

    
    return render(request, 'carrito.html', context)

@csrf_protect
def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return render(request, 'logout.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def resultado(request):
    return render(request, 'resultado.html')

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        # Simulate adding to cart - replace with actual cart logic
        cart_session = request.session.get('cart', [])
        cart_session.append({'product_id': product_id, 'quantity': quantity})
        request.session['cart'] = cart_session

        return JsonResponse({'message': 'Product added to cart'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def remove_from_cart(request):
    if request.method == 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        cart_session = request.session.get('cart', [])
        if product_id in cart:
            cart.pop(product_id)

        cart_session = [item for item in cart_session if item.get('product_id') != product_id]
        request.session['cart'] = cart_session
        request.session.modified = True

        total_price = 0
        for item in cart.values():
            cafe = Cafe.objects.filter(id=item.get('product_id')).first()
            if cafe:
                total_price += cafe.price * item.get('quantity', 1)

        return JsonResponse({'message': 'Product removed from cart'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def category(request, category_name):
    cafes = Cafe.objects.filter(category=category_name)
    return render(request, 'category.html', {'cafes': cafes, 'category_name': category_name})


