import json
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.utils.timezone import now
from web_case_2025.models.News import News
from web_case_2025.models.Order import Order, OrderItem
from web_case_2025.models.Product import Product, ProductType
from web_case_2025.models.Slide import Slide
from datetime import datetime

def home(request):
    news_qs = News.objects.filter(release_date__lte=now()).order_by('-release_date')[:4]
    product_types = ProductType.objects.all()
    slides = Slide.objects.all()
    return render(request, 'pages/home.html', {
        'news_list': news_qs,
        'slides': slides,
        'categories': product_types
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


def checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 創建訂單
            order = Order.objects.create(
                name=data.get('name', ''),
                phone=data.get('phone', ''),
                total_price=data.get('total_price', 0)
            )
            
            # 創建訂單項目
            for item in data.get('items', []):
                product = Product.objects.get(id=item.get('id'))
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.get('quantity', 1),
                    price=item.get('price', 0) * item.get('quantity', 1)
                )
            
            # 回傳成功的 JSON 回應
            return JsonResponse({
                'success': True,
                'order_id': order.id,
                'message': '訂單已成功提交'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': '無效的 JSON 數據'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    # 如果是 GET 請求，也回傳 JSON（而不是 HTML）
    return JsonResponse({
        'success': False,
        'error': '僅接受 POST 請求'
    }, status=405)



def contact(request):
    return render(request, 'pages/contact.html')