from django.contrib import admin
from .models import Cafe

class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'description')
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')

admin.site.register(Cafe, CafeAdmin)