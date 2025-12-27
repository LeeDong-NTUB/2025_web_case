from django.db import models
import string
import random

class DiscountCode(models.Model):
    name = models.CharField("折扣名稱", max_length=50)
    code = models.CharField("折扣碼", max_length=20, unique=True, blank=True)
    amount = models.IntegerField("折扣金額")
    min_spend = models.IntegerField("最低消費金額", default=0)
    is_active = models.BooleanField("是否啟用", default=True)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "折扣碼"
        verbose_name_plural = "折扣碼"

    def save(self, *args, **kwargs):
        if not self.code:
            chars = string.ascii_uppercase + string.digits
            self.code = ''.join(random.choices(chars, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"