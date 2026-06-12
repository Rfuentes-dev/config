from django.shortcuts import render, redirect
from .models import Cafe
from .forms import ProductForm
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages


# Create your views here.
def index(request):
    category_type = request.GET.get('type', None)
    
    if category_type:
        cafes = Cafe.objects.filter(category=category_type)
    else:
        cafes = Cafe.objects.all()
    
    return render(request, 'index.html', {'cafes': cafes, 'category_type': category_type})

def home(request):
    category_type = request.GET.get('type', None)
    
    if category_type:
        cafes = Cafe.objects.filter(category=category_type)
    else:
        cafes = Cafe.objects.all()
    
    return render(request, 'home.html', {'cafes': cafes, 'category_type': category_type})

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

def edit_cafe(request, cafe_id):
    cafe = Cafe.objects.get(id=cafe_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=cafe)
        if form.is_valid():
            form.save()
            return redirect('cafe_list')
    else:
        form = ProductForm(instance=cafe)
    return render(request, 'edit_cafe.html', {'form': form, 'cafe': cafe})

def delete_cafe(request, cafe_id):
    cafe = Cafe.objects.get(id=cafe_id)
    if request.method == 'POST':
        cafe.delete()
        return redirect('cafe_list')
    return render(request, 'delete_cafe.html', {'cafe': cafe})

def menu(request):
    category_type = request.GET.get('type', None)
    
    if category_type:
        cafes = Cafe.objects.filter(category=category_type)
    else:
        cafes = Cafe.objects.all()
    
    return render(request, 'menu.html', {'cafes': cafes, 'category_type': category_type})

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
                'id': product_id,
                'name': cafe.name,
                'price': cafe.price,
                'quantity': quantity,
                'total': cafe.price * quantity
            })
            total_price += cafe.price * quantity
    context = {'cart_items': cart_items, 'total': total_price}

    
    return render(request, 'carrito.html', context)

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_conf = request.POST.get('confirm_password')

        if password != password_conf:
            messages.error(request, 'No coinciden las contraseñas')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nombre de Usuario ya existe')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)

        login(request, new_user)
        return redirect('index')
    return render(request, 'register.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'username o contraseña invalida'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

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
        product_id = int(data.get('product_id'))
        quantity = int(data.get('quantity', 1))

        # Simulate adding to cart - replace with actual cart logic
        cart_session = request.session.get('cart', [])
        cart_session.append({'product_id': product_id, 'quantity': quantity})
        request.session['cart'] = cart_session
        request.session.modified = True

        return JsonResponse({'message': 'Producto agregado al carrito'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            if product_id is None:
                return JsonResponse({'error': 'product_id is required'}, status=400)
            
            product_id = int(product_id)
            
            cart_session = request.session.get('cart', [])
            cart_session = [item for item in cart_session if int(item.get('product_id')) != product_id]
            request.session['cart'] = cart_session
            request.session.modified = True

            return JsonResponse({'status': 'success', 'message': 'Producto quitado del carrito'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)
        except (ValueError, TypeError) as e:
            return JsonResponse({'error': f'Invalid product_id: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def category(request, category_name):
    cafes = Cafe.objects.filter(category=category_name)
    return render(request, 'category.html', {'cafes': cafes, 'category_name': category_name})
