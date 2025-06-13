from django.db import models

class ContactMessage(models.Model):
    name = models.CharField("姓名", max_length=100)
    phone = models.CharField("電話", max_length=20)
    message = models.TextField("訊息內容")
    created_at = models.DateTimeField("送出時間", auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "回饋訊息"
        verbose_name_plural = "回饋訊息"