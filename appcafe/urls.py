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
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('resultado/', views.resultado, name='resultado'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
]