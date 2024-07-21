from django.urls import path
from . views import (
    signup, 
    login, 
    getAndDeleteProfile, 
    listings, 
    listings_add, 
    listings_details, 
    shops, 
    shops_add,
    shops_details,
    orders,
    orders_add,
    order_details,
    deliveries,
    delivery_details
)

urlpatterns = [
    path("auth/signup/", signup),
    path("auth/login/", login),
    path("auth/users/<int:pk>/", getAndDeleteProfile),
    path("listings/", listings),
    path("listings/add/", listings_add),
    path("listings/<int:pk>/", listings_details),
    path("shops/", shops),
    path("shops/add/", shops_add),
    path("shops/<int:pk>/", shops_details),
    path("orders/", orders),
    path("orders/add/", orders_add),
    path("orders/<int:pk>/", order_details),
    path("deliveries/", deliveries),
    path("deliveries/<int:pk>/", delivery_details),
]
