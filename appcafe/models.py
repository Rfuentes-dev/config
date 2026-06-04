from django.db import models

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