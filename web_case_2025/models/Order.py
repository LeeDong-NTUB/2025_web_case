from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        app_label = 'bakery_app'

    def __str__(self):
        return f"訂單 #{self.id} - {self.name}"