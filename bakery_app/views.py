from django.shortcuts import render
from django.http import JsonResponse
import json

# models
from web_case_2025.models.News import News
from web_case_2025.models.Order import Order
from web_case_2025.models.OrderItem import OrderItem
from web_case_2025.models.Product import Product

# fake data
from .fake_data import news_list, slides, products, product_types

# 在導入後立即處理新聞資料
processed_news_list = News.process_news_data(news_list)

# 提取產品類別

def home(request):
    filtered_news = processed_news_list.copy()
    if len(filtered_news) > 4:
        filtered_news = filtered_news[:4]
    return render(request, 'pages/home.html', {'news_list': filtered_news, 'slides': slides})

def lastestNewsList(request):
    filtered_news = processed_news_list.copy()
    if len(filtered_news) > 10:
        filtered_news = filtered_news[:10]
    return render(request, 'pages/latest-news/list.html', {'news_list': filtered_news})

def lastestNewsPage(request, id):
    news = {}
    for news_item in processed_news_list:
        if news_item.get('id') == id:
            news = news_item
            break
    
    return render(request, 'pages/latest-news/page.html', {'news': news})

def order(request):
    return render(request, 'pages/order.html', {'products': products, 'categories': product_types})

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