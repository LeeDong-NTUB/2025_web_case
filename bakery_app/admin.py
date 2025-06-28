from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin import SimpleListFilter

from web_case_2025.models.Product import Product, ProductType
from web_case_2025.models.Order import Order, OrderItem
from web_case_2025.models.News import News, NewsImage
from web_case_2025.models.Slide import Slide
from web_case_2025.models.Accounting import AccountCategory, AccountEntry
from web_case_2025.models.ContactMessage import ContactMessage
from web_case_2025.models.BusinessInfo import BusinessInfo, BusinessHour
from django.contrib import admin
from django.db.models import Sum

# 移除不必要的 Group 模型
admin.site.unregister(Group)


from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date

class MonthFilter(admin.SimpleListFilter):
    title = _('月份')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        today = timezone.now().date()
        months = []
        for i in range(6):  # 最近六個月
            y = today.year
            m = today.month - i
            if m <= 0:
                m += 12
                y -= 1
            months.append((f"{y}-{m:02d}", f"{y}年{m}月"))
        return months

    def queryset(self, request, queryset):
        if self.value():
            y, m = map(int, self.value().split('-'))
            start = date(y, m, 1)
            if m == 12:
                end = date(y + 1, 1, 1)
            else:
                end = date(y, m + 1, 1)
            return queryset.filter(created_at__gte=start, created_at__lt=end)
        return queryset


# 產品管理
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'created_at')
    search_fields = ('name',)
    list_filter = ('product_type',)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_pinned', 'created_at', 'release_date', 'category')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('category', 'release_date', 'is_pinned')
    ordering = ('-is_pinned', '-release_date')
    inlines = [NewsImageInline]

# 輪播圖
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title', 'link')
    search_fields = ('title', 'sub_title')


# 訂單明細內嵌
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# 自定義付款狀態過濾器
class PaidStatusFilter(SimpleListFilter):
    title = '付款狀態'
    parameter_name = 'is_paid'

    def lookups(self, request, model_admin):
        return (
            ('paid', '已付款'),
            ('unpaid', '未付款'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'paid':
            return queryset.filter(paid_at__isnull=False)
        if self.value() == 'unpaid':
            return queryset.filter(paid_at__isnull=True)
        return queryset


class OrderAdminForm(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        # 如果已經勾選 is_expected_income_loss，就設為唯讀
        if obj and obj.is_expected_income_loss:
            return self.readonly_fields + ('is_expected_income_loss',)
        return self.readonly_fields

# 訂單管理
@admin.register(Order)
class OrderAdmin(OrderAdminForm):
    list_display = (
        'id',
        'customer_name',
        'customer_phone',
        'customer_email',
        'shipping_address',
        'created_at',
        'total_price',
        'payment_method',
        'display_payment_status',
    )
    list_filter = (PaidStatusFilter, 'payment_method', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_email', 'shipping_address')
    inlines = [OrderItemInline]

    def display_payment_status(self, obj):
        method_display = dict(Order.PAYMENT_METHODS).get(obj.payment_method, obj.payment_method)
        if obj.paid_at:
            return f"已付款（{method_display}）"
        elif obj.payment_method == 'cod':
            return "-"
        else:
            return f"未付款（{method_display}）"
    display_payment_status.short_description = "付款狀態"
    def save_model(self, request, obj, form, change):
            if change:
                original = Order.objects.get(pk=obj.pk)
                if not original.is_expected_income_loss and obj.is_expected_income_loss:
                    if not AccountEntry.objects.filter(source_type='order-expected-loss', source_id=str(obj.id)).exists():
                        category, _ = AccountCategory.objects.get_or_create(
                            name='預期訂單收益損失', defaults={'is_income': False}
                        )
                        AccountEntry.objects.create(
                            category=category,
                            subject=f"訂單 #{obj.id} 預期收益損失",
                            amount=obj.total_price,
                            source_type='Order',
                            source_id=str(obj.id),
                            created_at=timezone.now()
                        )
            super().save_model(request, obj, form, change)

@admin.register(AccountCategory)
class AccountCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_income')


@admin.register(AccountEntry)
class AccountEntryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'category', 'amount', 'created_at')
    list_filter = (MonthFilter, 'category', 'created_at')
    search_fields = ('subject', 'source_id')
    change_list_template = "admin/accounting/change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
            categories = AccountCategory.objects.all()

            total_income = 0
            total_cost = 0

            for cat in categories:
                total = qs.filter(category=cat).aggregate(total=Sum('amount'))['total'] or 0
                if cat.is_income:
                    total_income += total
                else:
                    total_cost += total

            response.context_data['summary'] = {
                'income': total_income,
                'cost': total_cost,
                'profit': total_income - total_cost,
            }
        except (AttributeError, KeyError):
            pass

        return response
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'message_summary', 'created_at')
    search_fields = ('name', 'phone', 'message')
    readonly_fields = ('name', 'phone', 'message', 'created_at')
    ordering = ('-created_at',)

    def message_summary(self, obj):
        return (obj.message[:20] + '...') if len(obj.message) > 20 else obj.message
    message_summary.short_description = "留言摘要"


class BusinessHourInline(admin.TabularInline):
    model = BusinessHour
    extra = 1

class BusinessInfoAdmin(admin.ModelAdmin):
    inlines = [BusinessHourInline]

admin.site.register(BusinessInfo, BusinessInfoAdmin)
