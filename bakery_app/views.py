from django.shortcuts import render
from django.http import JsonResponse
import json

# models
from web_case_2025.models.News import News
from web_case_2025.models.Order import Order
from web_case_2025.models.OrderItem import OrderItem
from web_case_2025.models.Product import Product

# fake data
from .fake_data import news_list, slides, products

# 在導入後立即處理新聞資料
processed_news_list = News.process_news_data(news_list)

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

def product_list(request):
    categories = [product.type for product in products]
    return render(request, 'pages/product_list.html', {'products': products, 'categories': categories})

def checkout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # 創建訂單
        order = Order.objects.create(
            name=data['name'],
            phone=data['phone'],
            total_price=data['total_price']
        )
        
        # 創建訂單項目
        for item in data['items']:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price'] * item['quantity']
            )
        
        return JsonResponse({'success': True, 'order_id': order.id})
    
    return render(request, 'shop/checkout.html')

def contact(request):
    return render(request, 'pages/contact.html')