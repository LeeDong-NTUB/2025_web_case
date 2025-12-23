from django.db import models

class BusinessInfo(models.Model):
    address = models.CharField("地址", max_length=255)
    phone = models.CharField("電話", max_length=20)
    email = models.EmailField("電子郵件")
    fb_link = models.TextField("FB連結", max_length=10000)
    ig_link = models.TextField("IG連結", max_length=10000)
    line_link = models.TextField("LINE連結", max_length=10000)
    ship = models.TextField("運送/保存方式", max_length=100000)

    feature_title_1 = models.CharField("首頁特色1-標題", max_length=100, default="手工製作")
    feature_content_1 = models.TextField("首頁特色1-內容", max_length=5000, default="堅持傳統工藝\n保留食物原味")
    
    feature_title_2 = models.CharField("首頁特色2-標題", max_length=100, default="使用本地食材")
    feature_content_2 = models.TextField("首頁特色2-內容", max_length=5000, default="精選當地新鮮食材\n支持在地農業")
    
    feature_title_3 = models.CharField("首頁特色3-標題", max_length=100, default="無防腐劑")
    feature_content_3 = models.TextField("首頁特色3-內容", max_length=5000, default="不添加人工色素\n讓您吃得安心")

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

class BrandHistory(models.Model):
    business = models.ForeignKey(BusinessInfo, on_delete=models.CASCADE, related_name='brand_histories')
    title = models.CharField("區塊標題", max_length=100)
    content = models.TextField("文案內容", max_length=2000, blank=True, null=True)
    image = models.ImageField("介紹圖片", upload_to='brand_history/', blank=True, null=True)
    order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "品牌歷史區塊"
        verbose_name_plural = "品牌歷史區塊"
        ordering = ['order']

    def __str__(self):
        return self.title