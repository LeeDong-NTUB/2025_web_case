from django.db import models

class ProductType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'bakery_app'

    def __str__(self):
        return self.name