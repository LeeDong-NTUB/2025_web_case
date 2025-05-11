from django.db import models

from web_case_2025.models.Order import Order
from web_case_2025.models.Product import Product


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        app_label = 'bakery_app'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"