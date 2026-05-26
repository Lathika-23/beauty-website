from django.contrib import admin
from .models import Category, Customer, Product
from .models import ShippingAddress
from .models import Order, OrderItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
