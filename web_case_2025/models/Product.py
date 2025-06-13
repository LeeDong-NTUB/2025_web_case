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
    image = models.ImageField("商品圖片", upload_to=upload_product_image)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    is_hot = models.BooleanField("是否為熱銷產品", default=False)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name
