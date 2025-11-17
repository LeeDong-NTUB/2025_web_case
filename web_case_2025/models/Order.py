from django.db import models
from web_case_2025.models.Product import Product

class Order(models.Model):
    PAYMENT_METHODS = [
        ('cod', '貨到付款'),
        ('linepay', 'Line Pay'),
    ]

    customer_name = models.CharField("顧客姓名", max_length=100)
    customer_phone = models.CharField("顧客電話", max_length=20)
    customer_email = models.EmailField("顧客 Email", max_length=100)
    shipping_address = models.CharField("運送地址", max_length=255, blank=True)
    shipping_store = models.CharField("運送全家門市", max_length=255)

    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    paid_at = models.DateTimeField("付款時間", null=True, blank=True)
    total_price = models.DecimalField("總金額", max_digits=10, decimal_places=0)
    payment_method = models.CharField("付款方式", max_length=10, choices=PAYMENT_METHODS, default='cod')
    is_expected_income_loss = models.BooleanField("本訂單紀錄為費損", default=False)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "訂單"
        verbose_name_plural = "訂單"

    def __str__(self):
        return f"訂單 #{self.id} - {self.customer_name}"

    @property
    def is_paid(self):
        return self.paid_at is not None

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="所屬訂單")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.IntegerField("數量", default=1)
    price = models.DecimalField("單價", max_digits=10, decimal_places=0)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "訂單明細"
        verbose_name_plural = "訂單明細"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
