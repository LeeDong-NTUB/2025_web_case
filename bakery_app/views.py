import json
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils.timezone import now
from web_case_2025.models import Order
from web_case_2025.models.News import News
from web_case_2025.models.Product import Product, ProductType
from web_case_2025.models.Accounting import AccountCategory, AccountEntry
from web_case_2025.models.Slide import Slide
from django.core.paginator import Paginator

def home(request):
    product_types = ProductType.objects.all()
    hot_products = Product.objects.filter(is_hot=True)
    slides = Slide.objects.all()
    return render(request, 'pages/home.html', {
        'slides': slides,
        'categories': product_types,
        'hot_products': hot_products
    })

def latestNewsList(request):
    qs = News.objects.filter(release_date__lte=now())
    paginator = Paginator(qs, 5)  # 每頁6筆
    page = request.GET.get('page')
    news_list = paginator.get_page(page)
    slides = Slide.objects.all()

    return render(request, 'pages/latest-news/list.html', {
        'news_list': news_list,
        'slides': slides,
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
    category_id = request.GET.get('category')
    product_types = ProductType.objects.all()

    if category_id:
        filtered_products = Product.objects.filter(product_type__id=category_id)
    else:
        filtered_products = Product.objects.all()

    return render(request, 'pages/product.html', {
        'products': filtered_products,
        'categories': product_types
    })


from .form import ContactMessageForm, OrderForm, OrderItemFormSet

# views.py

def checkout(request):
    # 1. 處理 GET 請求：顯示結帳頁面
    if request.method == 'GET':
        return render(request, 'pages/checkout.html')

    # 2. 處理 POST 請求：接收訂單資料 (維持您原有的邏輯)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_form = OrderForm({
                'customer_name': data.get('name'),
                'customer_phone': data.get('phone'),
                'customer_email': data.get('email'),
                'shipping_address': data.get('address'), # 店到店時這裡可能會存門市名稱
                'shipping_store': data.get('store'),     # 門市 ID 或代號
                'payment_method': data.get('payment', 'cod'),
                'note': data.get('note'),                # 新增備註欄位
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

                # 庫存檢查
                for form in order_item_formset:
                    product = form.cleaned_data['product']
                    quantity = form.cleaned_data['quantity']
                    if product.stock < quantity:
                        return JsonResponse({
                            'success': False,
                            'error': f"商品 {product.name} 庫存不足，剩餘 {product.stock} 件"
                        }, status=400)

                order.save()

                # 計算商品總價
                total_price = 0
                for form in order_item_formset:
                    order_item = form.save(commit=False)
                    order_item.order = order
                    order_item.price = order_item.product.price
                    order_item.save()
                    total_price += order_item.price * order_item.quantity

                    # 扣庫存
                    order_item.product.stock -= order_item.quantity
                    order_item.product.save()

                # 加運費（滿 1800 免運）
                shipping_fee = 0 if total_price >= 1800 else 120
                final_price = total_price + shipping_fee

                # 最終金額寫回 DB
                order.total_price = final_price
                order.save()

                # 記帳邏輯 (維持原樣)
                income_category, created = AccountCategory.objects.get_or_create(
                    name='訂單收入',
                    defaults={'is_income': True}
                )
                
                AccountEntry.objects.create(
                    category=income_category,
                    subject=f"訂單編號 #{order.id} 收入",
                    amount=final_price,
                    source_type='Order',
                    source_id=str(order.id)
                )
                
                return JsonResponse({
                    'success': True,
                    'order_id': order.id,
                    'redirect_url': f'/order/success/?id={order.id}'
                })
            else:
                errors = dict(order_form.errors.items())
                
                error_msgs = []
                for field, messages in errors.items():
                    if field == '__all__':
                        error_msgs.append(f"{messages[0]}")
                    else:
                        error_msgs.append(f"{messages[0]}")
                reason_str = "、".join(error_msgs)                
                return JsonResponse({
                    'success': False,
                    'error': f"{reason_str}",
                    'details': errors
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

def about(request):
    success = None
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/about/?success=1')
        else:
            return render(request, 'pages/about.html', {
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


def get_cart_details(request):
    """接收前端傳來的 ID 列表，回傳即時產品資訊"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_ids = data.get('ids', [])
            
            # 從資料庫查詢這些 ID 的產品
            products = Product.objects.filter(id__in=product_ids)
            
            response_data = []
            for product in products:
                response_data.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price, 
                    'image_url': product.image.url if product.image else '',
                    'stock': product.stock, 
                })
            
            return JsonResponse({'products': response_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)