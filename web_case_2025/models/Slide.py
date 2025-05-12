from django.db import models

class Slide(models.Model):
    """
    Represents a slide for a carousel or similar component.
    """
    src = models.ImageField(upload_to='slides/')
    link = models.CharField(max_length=255, help_text="點擊圖片後導向的連結")
    title = models.CharField(max_length=100, help_text="幻燈片的標題", blank=True)
    sub_title = models.CharField(max_length=255, help_text="幻燈片的副標題", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "bakery_app"
        verbose_name = "幻燈片"
        verbose_name_plural = "幻燈片"