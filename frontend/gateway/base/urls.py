from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard'),

    path('home/<int:user_id>/', views.home, name='home'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_edit/', views.products_edit, name='product_edit'),
    path('product_add/', views.products_add, name='product_add'),
    path('product_delete/', views.product_delete, name='product_delete'),

    path('shops/', views.shop, name='shops'),
    path('shop_detail/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('shop_add/', views.shop_add, name='shop_add'),
    path('shop_edit/', views.shop_edit, name='shop_edit'),
    path('shop_delete/', views.shop_delete, name='shop_delete'),

    path('orders/<int:user_id>/', views.order, name='orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
     path('order_add/', views.order_add, name='order_add'),

    path('contacts/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

]