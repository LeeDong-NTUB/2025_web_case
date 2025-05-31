from django.db import models
from bakery_app.utils.upload_file import upload_slide_image

class Slide(models.Model):
    image = models.ImageField("圖片", upload_to=upload_slide_image)
    link = models.CharField("導向連結", max_length=1000, help_text="點擊圖片後導向的連結", blank=True)
    title = models.CharField("標題", max_length=20, help_text="輪播圖的標題", blank=True)
    sub_title = models.CharField("副標題", max_length=30, help_text="輪播圖的副標題", blank=True)

    def __str__(self):
        return self.title or "(無標題)"

    class Meta:
        app_label = "bakery_app"
        verbose_name = "輪播圖"
        verbose_name_plural = "輪播圖"
