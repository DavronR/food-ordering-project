from django.db import models
from users.models import CustomUser
from restaurants.models import MenuItem

class Order(models.Model):
    STATUS_CHOICES = [
        ('Received', 'Received'),
        ('Picked Up', 'Picked Up'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    delivery_personnel = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    items = models.ManyToManyField(MenuItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"
