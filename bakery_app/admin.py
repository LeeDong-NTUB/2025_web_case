from django.contrib import admin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.utils.html import format_html
from django.urls import path

from web_case_2025.models.Product import Product, ProductType
from web_case_2025.models.Order import Order, OrderItem
from web_case_2025.models.News import News
from web_case_2025.models.Slide import Slide

admin.site.unregister(Group)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'created_at')
    search_fields = ('name',)
    list_filter = ('product_type',)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'release_date', 'category')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('category', 'release_date')
    ordering = ('-release_date',)

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title', 'link')
    search_fields = ('title', 'sub_title')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',  # 改正
        'customer_phone',  # 改正
        'customer_email',
        'created_at',
        'total_price',
        'payment_method',
        'display_payment_status',
        'notify_button'
    )
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_email')
    actions = ['notify_shipping']
    inlines = [OrderItemInline]

    def display_payment_status(self, obj):
        method_display = dict(Order.PAYMENT_METHODS).get(obj.payment_method, obj.payment_method)
        status_display = dict(Order.PAYMENT_CHOICES).get(obj.payment_status, obj.payment_status)

        if obj.payment_method == 'cod':
            return "貨到付款"
        return f"{status_display} ({method_display})"
    display_payment_status.short_description = "付款狀態"

    def notify_shipping(self, request, queryset):
        for order in queryset:
            self._send_notification(order)
        self.message_user(request, f"已通知出貨：{queryset.count()} 筆訂單")
    notify_shipping.short_description = "通知出貨（批次）"

    def notify_button(self, obj):
        return format_html(
            '<a class="button" href="{}">通知出貨</a>',
            f'notify/{obj.id}'
        )
    notify_button.short_description = "單筆通知"
    notify_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('notify/<int:order_id>', self.admin_site.admin_view(self.process_notify), name='order-notify'),
        ]
        return custom_urls + urls

    def process_notify(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        self._send_notification(order)
        self.message_user(request, f"訂單 #{order.id} 已通知出貨")
        return redirect(request.META.get('HTTP_REFERER', '/admin/'))

    def _send_notification(self, order):
        print(f"[通知出貨] 訂單 #{order.id} - {order.name}")