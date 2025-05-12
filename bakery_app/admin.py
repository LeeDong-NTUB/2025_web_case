from django.contrib import admin
from web_case_2025.models.Product import Product
from web_case_2025.models.Order import Order
from web_case_2025.models.OrderItem import OrderItem
from web_case_2025.models.News import News
from web_case_2025.models.ProductType import ProductType


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(News)
admin.site.register(ProductType)