from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.cafe_list, name='cafe_list'),
    path('add/', views.add_cafe, name='add_cafe'),
]