from django.db import models

class BusinessInfo(models.Model):
    address = models.CharField("地址", max_length=255)
    about = models.TextField("關於我們", max_length=10000)
    phone = models.CharField("電話", max_length=20)
    email = models.EmailField("電子郵件")

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "商家資訊"
        verbose_name_plural = "商家資訊"

    def __str__(self):
        return "商家資訊"

class BusinessHour(models.Model):
    business = models.ForeignKey(BusinessInfo, on_delete=models.CASCADE, related_name='business_hours')
    content = models.CharField("描述(eg.週一至週五：07:00 - 19:00)", max_length=50)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "營業時段"
        verbose_name_plural = "營業時段"

    def __str__(self):
        return f"{self.content}"
