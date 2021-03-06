from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivered = models.BooleanField(default=False)
    free = models.BooleanField(default=False)

    def __str__(self):
        if self.free:
            return  f"Order {self.id} ordered at {self.time} FREE"
        else:    
            return  f"Order {self.id} ordered at {self.time} costing ${self.price}"   

class NowTime(models.Model):
    time = models.DateTimeField(auto_now_add=True)

class Topping(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

class BasePizza(models.Model):
    pizzatype = models.CharField(max_length=28, unique=True)
    sm_0t = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sm_1t = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sm_2t = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sm_3t = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sm_st = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    la_0t = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    la_1t = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    la_2t = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    la_3t = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    la_st = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.pizzatype}"

class Pizza(models.Model):
    base_pizza = models.ForeignKey(BasePizza, on_delete=models.CASCADE, null=True)
    toppings = models.ManyToManyField(Topping, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="pizzas")
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_to_kitchen = models.BooleanField(default=False)
    large = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)

    def get_price(self):
        topping_count = self.toppings.all().count()
        if topping_count > 3: 
            topping_count = "s"
        else:    
            topping_count = str(topping_count)
        if self.large:
            price = "la_" + topping_count + "t"
        else:
            price = "sm_" + topping_count + "t"     
        self.price = eval("self.base_pizza."+ price)

    def __str__(self):
        topping_count = self.toppings.all().count()
        if topping_count == 0:
            if self.large:
                return f"Large {self.base_pizza.pizzatype} Pizza, at ${self.price}"         
            else:
                return f"Small {self.base_pizza.pizzatype} Pizza, at ${self.price}"  
        elif topping_count <= 3:
            if self.large:
                return f"Large {self.base_pizza.pizzatype} Pizza, with {topping_count} toppings at ${self.price}"         
            else:
                return f"Small {self.base_pizza.pizzatype} Pizza, with {topping_count} toppings at ${self.price}"
        else:
            if self.large:
                return f"Large {self.base_pizza.pizzatype} Special Pizza, at ${self.price}"         
            else:
                return f"Small {self.base_pizza.pizzatype} Special Pizza, at ${self.price}"              


class BasePasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} Pasta"

class Pasta(models.Model):
    base_pasta = models.ForeignKey(BasePasta, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="pastas")
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_to_kitchen = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)

    def get_price(self):
        self.price = self.base_pasta.price

    def __str__(self):
        return f"{self.base_pasta.name} at ${self.price}"    

class BaseSalad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name}"

class Salad(models.Model):
    base_salad = models.ForeignKey(BaseSalad, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="salads")
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_to_kitchen = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)

    def get_price(self):
        self.price = self.base_salad.price

    def __str__(self):
        return f"{self.base_salad.name} at ${self.price}"  

class BaseDinnerPlatters(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    large_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} Platter"

class DinnerPlatters(models.Model):
    base_platter = models.ForeignKey(BaseDinnerPlatters, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="dinnerplatters")
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_to_kitchen = models.BooleanField(default=False)
    large = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)

    def get_price(self):
        if self.large:
            self.price = self.base_platter.large_price
        else:
            self.price = self.base_platter.small_price    

    def __str__(self):
        if self.large:
            return f"Large {self.base_platter.name} Platter at ${self.price}"      
        else:
            return f"Small {self.base_platter.name} Platter at ${self.price}"          
