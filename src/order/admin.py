from django.contrib import admin

from .models import Address, DiscountCode, Order, OrderItem

admin.site.register(Address)
admin.site.register(DiscountCode)
admin.site.register(Order)
admin.site.register(OrderItem)
