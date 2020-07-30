from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField

class Store(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='store-logos')
    cover = models.ImageField(upload_to='store-covers')
    closed = models.BooleanField(default=False)
    workers = models.ManyToManyField(get_user_model(), related_name='working_at_stores', blank=True)
    user = models.ForeignKey(get_user_model(), related_name='owned_stores', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Visit(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='visits', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='visits', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.store}'

class Subscription(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='subscriptions', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='subscriptions', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} => {self.store}'

class RecruitmentRequest(models.Model):
    accepted = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), related_name='recruitment_requests', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='recruitment_requests', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} @ {self.store}'

class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='product-pictures')
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Price(models.Model):
    value = MoneyField(max_digits=19, decimal_places=4, default_currency='USD')
    product = models.ForeignKey(Product, related_name='prices', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.value_currency}{str(self.value)}'

class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='carts', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='carts', blank=True)

    def __str__(self):
        return f'{self.user}\'s Cart'
