from django.contrib import admin
from .models import Topping, Order, BasePizza, Pizza

admin.site.register(Pizza)
admin.site.register(BasePizza)
admin.site.register(Topping)
admin.site.register(Order)