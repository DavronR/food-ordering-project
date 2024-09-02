from django.contrib import admin
from django.urls import path, include
from orders import views as order_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', order_views.home, name='home'),  
    path('orders/', include('orders.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('users/', include('users.urls')),
]
