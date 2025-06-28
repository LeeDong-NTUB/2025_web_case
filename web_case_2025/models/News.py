from datetime import datetime
from django.db import models

class News(models.Model):
    category = models.CharField("分類", max_length=10)
    title = models.CharField("標題", max_length=30)
    summary = models.TextField("摘要", max_length=50)
    content = models.TextField("內容")
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    release_date = models.DateTimeField("發布日期")
    is_pinned = models.BooleanField("置頂", default=False)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "最新消息"
        verbose_name_plural = "最新消息"
        ordering = ['-is_pinned', '-created_at']

    @property
    def year(self): return self.release_date.year
    @property
    def month(self): return f"{self.release_date.month:02d}"
    @property
    def day(self): return f"{self.release_date.day:02d}"

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField("圖片說明", max_length=100, blank=True)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "最新消息附加圖片"
        verbose_name_plural = "最新消息附加圖片"
    def __str__(self):
        return f"圖片 for {self.news.title}"
