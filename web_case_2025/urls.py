from django.urls import path

from bakery_app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('latest-news/list/', views.lastestNewsList, name='latest-news-list'),
    path('latest-news/page/<int:id>/', views.latestNewsPage, name='latest-news-page'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product, name='product'),
    path('order/', views.order, name='order'),
    path('checkout/', views.checkout, name='checkout'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)