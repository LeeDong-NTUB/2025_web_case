from django.shortcuts import render

from web_case_2025.models.News import News
from .fake_data import news_list

# 在導入後立即處理新聞資料
processed_news_list = News.process_news_data(news_list)

def home(request):
    filtered_news = processed_news_list.copy()
    if len(filtered_news) > 4:
        filtered_news = filtered_news[:4]
    return render(request, 'pages/home.html', {'news_list': filtered_news})

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