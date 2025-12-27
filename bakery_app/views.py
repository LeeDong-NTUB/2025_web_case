import base64
import hashlib
import hmac
import json
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils.timezone import now
from bakery_app.utils.email_utils import send_order_confirmation
from web_case_2025.models import Order
from web_case_2025.models.News import News
from web_case_2025.models.Product import Product, ProductType
from web_case_2025.models.Accounting import AccountCategory, AccountEntry
from web_case_2025.models.Slide import Slide
from django.core.paginator import Paginator
from web_case_2025.models.BusinessInfo import BusinessInfo

def home(request):
    news_qs = News.objects.filter(release_date__lte=now()).order_by('-release_date')[:4]
    product_types = ProductType.objects.all()
    hot_products = Product.objects.filter(is_hot=True)
    slides = Slide.objects.all()
    
    business = BusinessInfo.objects.first()

    return render(request, 'pages/home.html', {
        'news_list': news_qs,
        'slides': slides,
        'categories': product_types,
        'hot_products': hot_products,
        'business': business
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
    business = BusinessInfo.objects.first()

    if category_id:
        filtered_products = Product.objects.filter(product_type__id=category_id)
    else:
        filtered_products = Product.objects.all()

    return render(request, 'pages/product.html', {
        'products': filtered_products,
        'categories': product_types,
        'business':business
    })


from .form import ContactMessageForm, OrderForm, OrderItemFormSet

# views.py
def checkout(request):
    if request.method == 'GET':
        return render(request, 'pages/checkout.html')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_form = OrderForm({
                'customer_name': data.get('name'),
                'customer_phone': data.get('phone'),
                'customer_email': data.get('email'),
                'shipping_address': data.get('address'),
                'shipping_store': data.get('store'),
                'payment_method': data.get('payment', 'cod'),
                'note': data.get('note'),
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

                for form in order_item_formset:
                    product = form.cleaned_data['product']
                    quantity = form.cleaned_data['quantity']
                    if product.stock < quantity:
                        return JsonResponse({
                            'success': False,
                            'error': f"商品 {product.name} 庫存不足，剩餘 {product.stock} 件"
                        }, status=400)

                order.save()

                total_price = 0
                for form in order_item_formset:
                    order_item = form.save(commit=False)
                    order_item.order = order
                    order_item.price = order_item.product.current_price
                    order_item.save()
                    total_price += order_item.price * order_item.quantity

                    order_item.product.stock -= order_item.quantity
                    order_item.product.save()

                shipping_fee = 0 if total_price >= 1800 else 120
                final_price = total_price + shipping_fee

                order.total_price = final_price
                order.save()

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
                if order.payment_method == 'cod':
                    send_order_confirmation(order)
                if order.payment_method == 'linepay':
                    try:
                        uri_path = "/v3/payments/request"
                        nonce = str(int(time.time() * 1000))
                        order_uuid = str(uuid.uuid4())

                        body = {
                            "amount": int(order.total_price),
                            "currency": "TWD",
                            "orderId": str(order.id),
                            "packages": [{
                                "id": "package-1",
                                "name": "宏農手工之家線上訂單",
                                "amount": int(order.total_price),
                                "products": [{
                                    "id": f"order-{order.id}",
                                    "name": "宏農手工之家線上訂單",
                                    "quantity": 1,
                                    "price": int(order.total_price),
                                    "originalPrice": int(order.total_price),
                                }]
                            }],
                            "redirectUrls": {
                                "confirmUrl": f"{settings.LINE_PAY['confirm_url']}?order_id={order.id}",
                                "cancelUrl": settings.LINE_PAY["cancel_url"]
                            },
                            "options": {
                                "display": {
                                    "locale": "zh_TW",
                                    "checkConfirmUrlBrowser": False
                                }
                            }
                        }

                        body_str = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
                        signature = generate_linepay_signature(
                            settings.LINE_PAY['channel_secret'], uri_path, body_str, nonce
                        )

                        headers = {
                            "Content-Type": "application/json; charset=UTF-8",
                            "X-LINE-ChannelId": settings.LINE_PAY["channel_id"],
                            "X-LINE-Authorization-Nonce": nonce,
                            "X-LINE-Authorization": signature
                        }

                        response = requests.post(
                            f"{settings.LINE_PAY['api_base']}{uri_path}",
                            headers=headers,
                            data=body_str.encode('utf-8')
                        )
                        res_data = response.json()

                        if response.status_code == 200 and res_data.get("returnCode") == "0000":
                            return JsonResponse({
                                "success": True,
                                "payment_url": res_data["info"]["paymentUrl"]["web"],
                                "order_id": order.id
                            })
                        else:
                            print(res_data)
                            return JsonResponse({
                                "success": False,
                                "error": "LINE Pay 建立付款失敗",
                                "detail": res_data
                            }, status=500)
                    except Exception as e:
                        print(e)
                        return JsonResponse({
                            "success": False,
                            "error": "LINE Pay 錯誤",
                            "detail": str(e)
                        }, status=500)

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
                'business': business,
                'form': form,
            })
    else:
        form = ContactMessageForm()
    business = BusinessInfo.objects.first()
    success_param = request.GET.get('success')
    return render(request, 'pages/contact.html', {
        'form': form,
        'brand_histories': business.brand_histories.all() if business else [],
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
            
            products = Product.objects.filter(id__in=product_ids)
            
            response_data = []
            for product in products:
                response_data.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'special_price': product.special_price if product.is_on_sale else None,
                    'current_price': product.current_price,
                    'image_url': product.image.url if product.image else '',
                    'stock': product.stock, 
                })
            
            return JsonResponse({'products': response_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

from web_case_2025 import settings
import requests
from django.views.decorators.csrf import csrf_exempt
import time

def generate_linepay_signature(channel_secret, uri, body_str, nonce):
    signature_raw = channel_secret + uri + body_str + nonce
    signature = base64.b64encode(
        hmac.new(channel_secret.encode('utf-8'), signature_raw.encode('utf-8'), hashlib.sha256).digest()
    ).decode('utf-8')
    return signature


@csrf_exempt
def linepay_confirm(request):
    order_id = request.GET.get("order_id")
    transaction_id = request.GET.get("transactionId")

    if not order_id or not transaction_id:
        return JsonResponse({"success": False, "error": "缺少必要參數"}, status=400)

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"success": False, "error": "訂單不存在"}, status=404)

    uri_path = f"/v3/payments/{transaction_id}/confirm"
    nonce = str(int(time.time() * 1000))
    body = {
        "amount": int(order.total_price),
        "currency": "TWD"
    }
    body_str = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
    signature = generate_linepay_signature(
        settings.LINE_PAY['channel_secret'], uri_path, body_str, nonce
    )

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-LINE-ChannelId": settings.LINE_PAY["channel_id"],
        "X-LINE-Authorization-Nonce": nonce,
        "X-LINE-Authorization": signature
    }

    confirm_url = f"{settings.LINE_PAY['api_base']}{uri_path}"
    res = requests.post(confirm_url, headers=headers, data=body_str.encode("utf-8"))
    res_data = res.json()

    if res.status_code == 200 and res_data.get("returnCode") == "0000":
        order.paid_at = now()
        order.save()
        send_order_confirmation(order)
        return render(request, "pages/payment_success.html", {"order": order})
    else:
        return render(request, "pages/payment_failed.html", {
            "order": order,
            "error": res_data.get("returnMessage", "付款確認失敗")
        })