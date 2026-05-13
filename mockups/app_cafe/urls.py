from django.urls import path
from .views import index, menu;
from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
]