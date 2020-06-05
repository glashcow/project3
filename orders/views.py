from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import RegisterForm
from .models import *


def index(request):
	return HttpResponseRedirect(reverse("menu"))


def register(response):
    if response.method == "POST":
	    form = RegisterForm(response.POST)
	    if form.is_valid():
	        form.save()
	    return HttpResponseRedirect(reverse("about"))
    else:
	    form = RegisterForm()
    return render(response, "orders/signup.html", {"form":form})    


def menu(request):
	context = {
		"pizzas" : BasePizza.objects.all(),
		"toppings" : Topping.objects.all(),
		"user" : request.user,
		"username" : request.user.username
	}
	return render(request, "orders/menu.html", context)


def pizzaorder(request):
	context = {
		"pizzas" : BasePizza.objects.all(),
		"toppings" : Topping.objects.all(),
		"user" : request.user,
		"username" : request.user.username
	}
	return render(request, "orders/pizzaorder.html", context)


def specialpizzaorder(request):
	context = {
		"pizzas" : BasePizza.objects.all(),
		"user" : request.user,
		"username" : request.user.username
	}
	return render(request, "orders/specialpizzaorder.html", context)	

@login_required
def pizzorderin(request):
	toppings = request.POST.getlist("toppings")
	if len(toppings) > 3:
		messages.success(request, "Too many Toppings, please pick a maximum of 3")
		return HttpResponseRedirect(reverse("pizzaorder"))
	else:	
		pizzatype = request.POST["pizzatype"]
		base = BasePizza.objects.get(pizzatype = pizzatype)
		size = request.POST["size"]
		if size == "large":
			large = True
		else:
			large = False	
		new_pizza = Pizza(base_pizza = base, ordered_by = request.user, large = large)
		new_pizza.save()
		p = Pizza.objects.filter(ordered_by=request.user).last()
		for topping in toppings:
			t = Topping.objects.get(name = topping)
			p.toppings.add(t)
		p.get_price()
		p.save()
		messages.success(request, "Added To Cart")
		return HttpResponseRedirect(reverse("menu"))

@login_required
def specialpizzorderin(request):
	pizzatype = request.POST["pizzatype"]
	base = BasePizza.objects.get(pizzatype = pizzatype)
	size = request.POST["size"]
	if size == "large":
		large = True
	else:
		large = False	
	new_pizza = Pizza(base_pizza = base, ordered_by = request.user, large = large)
	new_pizza.save()
	p = Pizza.objects.filter(ordered_by=request.user).last()
	for topping in Topping.objects.all():
		p.toppings.add(topping)
	p.get_price()
	p.save()
	messages.success(request, "Added To Cart")
	return HttpResponseRedirect(reverse("menu"))


def cart_total_price(request):
	total_price = 0
	for pizza in Pizza.objects.filter(ordered_by=request.user).filter(sent_to_kitchen=False):
		total_price += pizza.price
	return total_price	


@login_required
def cart(request):
	context = {
		"pizzas": Pizza.objects.filter(ordered_by=request.user).filter(sent_to_kitchen=False),
		"price" : cart_total_price(request)
	}
	return render(request, "orders/cart.html", context)

@login_required
def orders(request):
	context = {
		"orders" : Order.objects.filter(user=request.user),
		"pizzas": Pizza.objects.filter(sent_to_kitchen=True),
	}
	return render(request, "orders/yourorders.html", context)

@login_required
def placeorder(request):
	new_order = Order(user = request.user, price = cart_total_price(request))
	new_order.save()
	for pizza in Pizza.objects.filter(ordered_by=request.user).filter(sent_to_kitchen=False):
		pizza.order = new_order
		pizza.sent_to_kitchen = True
		pizza.save()
	messages.success(request, "Food is on it's way")	
	return HttpResponseRedirect(reverse("menu"))

@staff_member_required
def viewActiveOrders(request):
	context = {
		"orders" : Order.objects.filter(delivered = False)
	}
	return render(request, "orders/vieworders.html", context)

@staff_member_required
def individualOrder(request, order_id):
	context = {
		"pizzas" : Pizza.objects.filter(order = Order.objects.get(id = order_id)),
		"id" : order_id
	}
	return render(request, "orders/vieworder.html", context)

@staff_member_required
def orderdelivered(request):
	id = request.POST["order_id"]
	order = Order.objects.get(id=id)
	order.delivered = True
	now = NowTime()
	now.save()
	now = NowTime.objects.last()
	time_delivered = now.time
	time_ordered = order.time
	free = False
	if time_ordered+timedelta(minutes=1) < time_delivered:
		free = True
	order.free = free
	order.save()
	return HttpResponseRedirect(reverse("viewActiveOrders"))

def about(request):
	context = {
		"username" : request.user.username
	}
	return render(request, "orders/about.html", context)