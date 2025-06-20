import json
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils.timezone import now
from web_case_2025.models import Order
from web_case_2025.models.News import News
from web_case_2025.models.Product import Product, ProductType
from web_case_2025.models.Accounting import AccountCategory, AccountEntry  # 根據實際路徑調整
from web_case_2025.models.Slide import Slide
from datetime import datetime

def home(request):
    news_qs = News.objects.filter(release_date__lte=now()).order_by('-release_date')[:4]
    product_types = ProductType.objects.all()
    hot_products = Product.objects.filter(is_hot=True)
    slides = Slide.objects.all()
    return render(request, 'pages/home.html', {
        'news_list': news_qs,
        'slides': slides,
        'categories': product_types,
        'hot_products': hot_products
    })

def lastestNewsList(request):
    news_qs = News.objects.filter(release_date__lte=datetime.now()).order_by('-release_date')[:10]
    return render(request, 'pages/latest-news/list.html', {
        'news_list': news_qs
    })

def latestNewsPage(request, id):
    news = get_object_or_404(News, id=id)
    return render(request, 'pages/latest-news/page.html', {'news': news})

from django.shortcuts import render

def order(request):
    products = Product.objects.all()
    product_types = ProductType.objects.all()
    return render(request, 'pages/order.html', {
        'products': products,
        'categories': product_types
    })

def product(request):
    category_name = request.GET.get('category')
    product_types = ProductType.objects.all()

    if category_name:
        filtered_products = Product.objects.filter(product_type__name=category_name)
    else:
        filtered_products = Product.objects.all()

    return render(request, 'pages/product.html', {
        'products': filtered_products,
        'categories': product_types
    })


from .form import ContactMessageForm, OrderForm, OrderItemFormSet

def checkout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_form = OrderForm({
            'customer_name': data.get('name'),
            'customer_phone': data.get('phone'),
            'customer_email': data.get('email'),
            'shipping_address': data.get('address'),
            'payment_method': data.get('payment', 'cod'),
        })

        formset_data = {
            'items-TOTAL_FORMS': str(len(data.get('items', []))),
            'items-INITIAL_FORMS': '0',
            'items-MIN_NUM_FORMS': '0',
            'items-MAX_NUM_FORMS': '1000',
        }

        for i, item in enumerate(data.get('items', [])):
            formset_data[f'items-{i}-product'] = item.get('product_id')
            formset_data[f'items-{i}-quantity'] = item.get('quantity', 1)

        order_item_formset = OrderItemFormSet(formset_data, prefix='items')

        if order_form.is_valid() and order_item_formset.is_valid():
            order = order_form.save(commit=False)
            order.total_price = 0
            order.save()

            total_price = 0
            for form in order_item_formset:
                order_item = form.save(commit=False)
                order_item.order = order
                order_item.price = order_item.product.price
                order_item.save()
                total_price += order_item.price * order_item.quantity

            order.total_price = total_price
            order.save()

            income_category, created = AccountCategory.objects.get_or_create(
                name='訂單收入',
                defaults={'is_income': True}
            )
            
            AccountEntry.objects.create(
                category=income_category,
                subject=f"訂單編號 #{order.id} 收入",
                amount=order.total_price,
                source_type='Order',
                source_id=str(order.id)
            )
            
            return JsonResponse({
                'success': True,
                'order_id': order.id,
                'message': '訂單已成功提交',
                'redirect_url': f'/order/success/?id={order.id}'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': order_form.errors,
                'formset_errors': order_item_formset.errors
            }, status=400)


def contact(request):
    success = None
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contact/?success=1')
        else:
            return render(request, 'pages/contact.html', {
                'form': form,
            })
    else:
        form = ContactMessageForm()

    success_param = request.GET.get('success')
    return render(request, 'pages/contact.html', {
        'form': form,
        'success': success_param,
    })

def order_success(request):
    order_id = request.GET.get("id")
    order = get_object_or_404(Order, id=order_id)
    return render(request, "pages/payment_success.html", {"order": order})