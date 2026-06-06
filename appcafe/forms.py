from django import forms
from .models import Cafe

class ProductForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'description', 'price', 'category']