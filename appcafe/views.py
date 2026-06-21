from django.shortcuts import render, redirect
from .models import Cafe, Pedido
from .forms import ProductForm
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection


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

def resultado(request):
    cart_session = request.session.get('cart', [])

    if not isinstance(cart_session, list):
        cart_session = []

    if not cart_session:
        return redirect('cart')

    total_price = 0
    gotProducts = []

    for item in cart_session:
        if isinstance(item, dict):
            p_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            if p_id is not None:
                cafe = Cafe.objects.filter(id=int(p_id)).first()
                if cafe:
                    total_price += cafe.price * quantity
                    gotProducts.append(f"{cafe.name} (x{quantity})")

    pedido = None
    if gotProducts:
        textDetails = ", ".join(gotProducts)
        userActual = request.user if request.user.is_authenticated else None

        pedido = Pedido.objects.create(
            user = userActual,
            total = total_price,
            details = textDetails
        )
    request.session['cart'] = []
    request.session.modified = True

    return render(request, 'resultado.html', {'pedido': pedido})

def historial_pedidos(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('index')
    
    pedidos_db = Pedido.objects.all().order_by('-date')

    if not pedidos_db.exists():
        tableName = Pedido._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = %s", [tableName])
            cursor.execute("DELETE FROM sqlite_sequence WHERE name LIKE '%%pedido%%'")

    
    return render(request, 'historial.html', {'pedidos': pedidos_db})

def delete_pedido(request, pedido_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('index')
    
    if request.method == 'POST':
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.delete()
        messages.success(request, f'El pedido #{pedido_id} fue eliminado con exito.', extra_tags='pedido_msg')

    return redirect('historial_pedidos')

def user_list(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('index')

    users = User.objects.all().order_by('id')
    return render(request, 'user_list.html', {'usuarios': users})

def add_user(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        es_admin = request.POST.get('is_superuser') == 'on'

        if User.objects.filter(username=username).exists():
            message.error(request, 'El nombre de usuario ya existe.')
            return redirect('add_user')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.is_superuser = es_admin
        new_user.is_staff = es_admin
        new_user.save()

        return redirect('user_list')

    return render(request, 'add_user.html')

def edit_user(request, user_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('index')

    userEdit = User.objects.get(id=user_id)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        es_admin = request.POST.get('is_superuser') == 'on'

        if User.objects.filter(username=new_username).exclude(id=user_id).exists():
            messages.error(request, 'nombre de usuario ocupado por otro.')
            return render(request, 'edit_user.html', {'usuario': userEdit})

        userEdit.username = new_username
        userEdit.email = new_email
        userEdit.is_superuser = es_admin
        userEdit.is_staff = es_admin

        new_password = request.POST.get('password')
        if new_password and new_password.strip() !="":
            userEdit.set_password(new_password)
        
        userEdit.save()
        return redirect('user_list')
    
    return render(request, 'edit_user.html', {'usuario': userEdit})

def delete_user(request, user_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('index')
    
    user = User.objects.get(id=user_id)

    if user == request.user:
        messages.error(request, "No puedes eliminar tu cuenta si eres el admin.")
        return redirect('user_list')
    
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    
    return render(request, 'delete_user.html', {'usuario': user})

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
