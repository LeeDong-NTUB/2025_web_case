from django.urls import path

from bakery_app import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]