from django.db import models
from .ProductType import ProductType


class Product(models.Model):
    
    name = models.CharField(max_length=100)
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'bakery_app'

    def __str__(self):
        return self.name