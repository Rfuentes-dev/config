from django.urls import path
from .views import index, menu;
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('admin/', admin.site.urls),
    path('accounts/', include('app_cafe.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]