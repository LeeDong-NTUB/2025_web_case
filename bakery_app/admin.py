from django.contrib import admin
from web_case_2025.models.Product import Product
from web_case_2025.models.Order import Order
from web_case_2025.models.OrderItem import OrderItem


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)