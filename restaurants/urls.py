from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.owner_dashboard, name='restaurant_owner_dashboard'),
    path('owner-dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('create-restaurant/', views.owner_dashboard, name='create_restaurant'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:pk>/menu/', views.restaurant_menu, name='restaurant_menu'),
    path('restaurant/<int:pk>/manage-menu/', views.manage_menu, name='manage_menu'),  
]
