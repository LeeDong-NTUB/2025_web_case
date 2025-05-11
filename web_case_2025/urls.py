from django.urls import path

from bakery_app import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('latest-news/list/', views.lastestNewsList, name='latest-news-list'),
    path('latest-news/page/<int:id>/', views.lastestNewsPage, name='latest-news-page'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product_list, name='product_list'),
    path('checkout/', views.checkout, name='checkout'),
]