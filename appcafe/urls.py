from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.cafe_list, name='cafe_list'),
    path('add/', views.add_cafe, name='add_cafe'),
    path('edit/<int:cafe_id>/', views.edit_cafe, name='edit_cafe'),
    path('delete/<int:cafe_id>/', views.delete_cafe, name='delete_cafe'),
    path('home/', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('resultado/', views.resultado, name='resultado'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('historial/', views.historial_pedidos, name='historial_pedidos'),
    path('historial/delete/<int:pedido_id>/', views.delete_pedido, name='delete_pedido'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]