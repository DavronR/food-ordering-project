from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('cart/', views.cart, name='cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('delivery-personal-dashboard/', views.delivery_personnel_dashboard, name='delivery_personnel_dashboard'), 
    path('pick-order/<int:order_id>/', views.pick_order, name='pick_order'),  
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),  
]
