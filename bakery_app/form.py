from django import forms
from django.core.validators import RegexValidator, EmailValidator
from web_case_2025.models.Order import Order, OrderItem
from web_case_2025.models.ContactMessage import ContactMessage
from django.forms import inlineformset_factory

class OrderForm(forms.ModelForm):
    customer_phone = forms.CharField(
        label='顧客電話',
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?886\d{9}$|^09\d{8}$',
                message="請輸入正確的手機號碼（例如：0912345678 或 +886912345678）"
            )
        ]
    )

    customer_email = forms.EmailField(
        label='顧客 Email',
        max_length=100,
        validators=[
            EmailValidator(message="請輸入有效的 Email 地址")
        ]
    )

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_phone',
            'customer_email',
            'shipping_address',
            'payment_method',
        ]
        labels = {
            'customer_name': '顧客姓名',
            'shipping_address': '運送地址',
            'payment_method': '付款方式',
        }
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 2}),
            'payment_method': forms.RadioSelect,
        }

OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True
)

class ContactMessageForm(forms.ModelForm):
    phone = forms.CharField(
        label='電話',
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^(\+8869\d{8}|09\d{8})$',
                message="請輸入正確的手機號碼（例如：0912345678 或 +886912345678）"
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': '請填入您的電話號碼',
            'class': 'w-full pl-10 pr-4 py-3 bg-cream border border-cream-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-300'
        })
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '請填入您的姓名',
                'class': 'w-full pl-10 pr-4 py-3 bg-cream border border-cream-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-300'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': '請填入您的訊息內容',
                'rows': 6,
                'class': 'w-full px-4 py-3 bg-cream border border-cream-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-300'
            }),
        }
