from django.urls import path

from bakery_app import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('latest-news/list', views.lastestNewsList, name='latest-news-list'),
    path('latest-news/page/<int:id>', views.lastestNewsPage, name='latest-news-page'),
]