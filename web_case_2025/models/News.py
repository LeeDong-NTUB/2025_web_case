from datetime import datetime
from django.db import models

class News(models.Model):
    category = models.CharField("分類", max_length=10, blank=False)
    title = models.CharField("標題", max_length=30, blank=False)
    summary = models.TextField("摘要", blank=False, max_length=50)
    content = models.TextField("內容", blank=False)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    release_date = models.DateTimeField("發布日期", blank=False)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "最新消息"
        verbose_name_plural = "最新消息"

    @property
    def year(self):
        return self.release_date.year if self.release_date else None

    @property
    def month(self):
        return f"{self.release_date.month:02d}" if self.release_date else None

    @property
    def day(self):
        return f"{self.release_date.day:02d}" if self.release_date else None

    def __str__(self):
        return f"{self.title}"
