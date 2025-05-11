from django.db import models


class Product(models.Model):
    PRODUCT_TYPES = (
        ('baozi', '包子'),
        ('mochi', '麻糬'),
        ('mantou', '饅頭'),
    )
    
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    image = models.ImageField(upload_to='products/')

    class Meta:
        app_label = 'bakery_app'

    def __str__(self):
        return self.name