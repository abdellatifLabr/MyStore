from datetime import datetime
import pytz

from django.db import models
from django.db.models import Sum, F
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField


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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def expired(self):
        utc = pytz.UTC
        return self.expiry < utc.localize(datetime.now())

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

    @property
    def total(self):
        items = OrderItem.objects.filter(order_id=self.id)
        items_total = items.aggregate(result=Sum(F('product__price__value') * F('quantity'), output_field=models.FloatField()))['result']

        if (self.discount_code):
            return items_total - (items_total * self.discount_code.value / 100)
        
        return items_total


    def __str__(self):
        return f'Order ({self.user})'

class OrderItem(models.Model):
    quantity = models.IntegerField()
    product = models.OneToOneField('shopping.Product', related_name='orders', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def cost(self):
        return self.product.price.value * self.quantity

    def __str__(self):
        return f'{self.product} ({self.quantity})'
