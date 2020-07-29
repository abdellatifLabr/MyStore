from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.template.defaultfilters import timeuntil

from shopping.models import Product, Store

class Address(models.Model):
    country = CountryField()
    city = models.CharField(max_length=32)
    street = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=16)
    user = models.ForeignKey(get_user_model(), related_name='addresses', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.city}, {self.country}. {self.street}'

class DiscountCode(models.Model):
    code = models.CharField(max_length=32)
    value = models.IntegerField()
    expiry = models.DateTimeField()
    store = models.ForeignKey(Store, related_name='discount_codes', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def expired(self):
        return self.expiry < datetime.now()
    
    @property
    def expiry(self):
        return timeuntil(self.expiry)

    def __str__(self):
        return self.code

class Order(models.Model):
    done = models.BooleanField(default=False)
    shipping_address = models.OneToOneField(Address, related_name='shipping_orders', on_delete=models.SET_NULL, null=True, blank=True)
    billing_address = models.OneToOneField(Address, related_name='billing_orders', on_delete=models.SET_NULL, null=True, blank=True)
    discount_code = models.OneToOneField(DiscountCode, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    quantity = models.IntegerField(default=1)
    product = models.OneToOneField(Product, related_name='orders', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
