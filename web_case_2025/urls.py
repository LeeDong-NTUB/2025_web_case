from django.urls import include, path

from bakery_app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('latest-news/list/', views.latestNewsList, name='latest-news-list'),
    path('latest-news/page/<int:id>/', views.latestNewsPage, name='latest-news-page'),
    path('about/', views.about, name='about'),
    path('product/', views.product, name='product'),
    path('order/', views.order, name='order'),
    path('checkout/', views.checkout, name='checkout'),
    path("order/success/", views.order_success, name="order_success"),
    path('api/cart-details/', views.get_cart_details, name='api_cart_details'),
    path("linepay/confirm/", views.linepay_confirm, name="linepay_confirm"),
    path("order/success/", views.order_success, name="order_success"),
    path('validate-coupon/', views.validate_coupon, name='api_validate_coupon'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
