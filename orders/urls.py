from django.urls import path
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("menu/pizzaorder", views.pizzaorder, name="pizzaorder"),
    path("menu/specialpizzaorder", views.specialpizzaorder, name="specialpizzaorder"),
    path("orderin", views.pizzorderin, name="pizzorderin"),
    path("specialorderin", views.specialpizzorderin, name="specialpizzorderin"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("orders/", views.orders, name="orders"),
    path("placeorder", views.placeorder, name="placeorder"),
    path("viewActiveOrders/", views.viewActiveOrders, name="viewActiveOrders"),
    path("<int:order_id>", views.individualOrder, name ="individualOrder"), 
    path("orderdelivered", views.orderdelivered, name ="orderdelivered"), 
    path("about/", views.about, name ="about"), 
    path('', include("django.contrib.auth.urls")),
]

