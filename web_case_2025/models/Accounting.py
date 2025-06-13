from django.db import models

class AccountCategory(models.Model):
    name = models.CharField("科目分類名稱", max_length=50)
    is_income = models.BooleanField("是否為加項（收入）", default=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "記帳分類"
        verbose_name_plural = "記帳分類"

class AccountEntry(models.Model):
    category = models.ForeignKey(AccountCategory, on_delete=models.CASCADE, verbose_name="記帳分類")
    subject = models.CharField("說明", max_length=100)
    amount = models.DecimalField("金額", max_digits=12, decimal_places=2)
    created_at = models.DateTimeField("登記時間", auto_now_add=True)

    source_type = models.CharField("來源", max_length=50, blank=True)
    source_id = models.CharField("來源 ID", max_length=50, blank=True)

    def __str__(self):
        return f"{self.subject} ({self.amount})"

    class Meta:
        app_label = 'bakery_app'
        verbose_name = "記帳紀錄"
        verbose_name_plural = "記帳紀錄"
