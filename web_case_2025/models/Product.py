from django.db import models
from bakery_app.utils.upload_file import upload_product_image, upload_product_type_image

class ProductType(models.Model):
    name = models.CharField("類別名稱", max_length=100)
    description = models.TextField("類別說明", blank=True)
    image = models.ImageField("類別圖片", upload_to=upload_product_type_image)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "商品類別"
        verbose_name_plural = "商品類別"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("商品名稱", max_length=100)
    product_type = models.ForeignKey(ProductType, verbose_name="商品類別", on_delete=models.DO_NOTHING)
    description = models.TextField("商品說明", blank=True)
    price = models.DecimalField("價格", max_digits=6, decimal_places=0)
    special_price = models.IntegerField(verbose_name='特價價格', null=True, blank=True, help_text="若無特價請留空或填0")
    image = models.ImageField("商品圖片", upload_to=upload_product_image)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    is_hot = models.BooleanField("是否為熱銷產品", default=False)
    stock = models.PositiveIntegerField("當前庫存數量(請謹慎維護)", default=0)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "商品"
        verbose_name_plural = "商品"

    @property
    def current_price(self):
        """如果設定了特價且大於0，回傳特價，否則回傳原價"""
        if self.special_price and self.special_price > 0:
            return self.special_price
        return self.price
    
    @property
    def is_on_sale(self):
        """判斷是否正在特價"""
        return self.special_price is not None and self.special_price > 0 and self.special_price < self.price
    
    def __str__(self):
        return self.name
