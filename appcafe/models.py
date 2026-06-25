from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cafe(models.Model):
    CATEGORY_CHOICES = [
        ('hot', 'Cafes Calientes'),
        ('cold', 'Cafes Frios'),
        ('desserts', 'Postres'),
        ('sandwiches', 'Sandwiches'),
        ('promotions', 'Promociones'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='hot')

    def __str__(self):
        return self.name

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    details = models.TextField()

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('shipped', 'Enviado')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Pedido #{self.id} - Total: ${self.total}"