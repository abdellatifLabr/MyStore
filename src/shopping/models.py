from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

from .utils import build_store_cover_path, build_store_logo_path, build_product_picture_path

class StoreLogo(models.Model):
    original = ProcessedImageField(
                    upload_to=build_store_logo_path,
                    processors=[
                        ResizeToFill(180, 180)
                    ],
                    format='JPEG'
                )

    desktop = ImageSpecField(
                    source='original',
                    processors=[
                        ResizeToFill(170, 170)
                    ]
                )

    mobile = ImageSpecField(
                    source='original',
                    processors=[
                        ResizeToFill(128, 128)
                    ]
                )

    thumbnail = ImageSpecField(
                    source='original', 
                    processors=[
                        ResizeToFill(32, 32)
                    ]
                )

class StoreCover(models.Model):
    original = ProcessedImageField(
                    upload_to=build_store_logo_path,
                    processors=[
                        ResizeToFill(820, 312)
                    ],
                    format='JPEG'
                )

    mobile = ImageSpecField(
                    source='original',
                    processors=[
                        ResizeToFill(640, 360)
                    ]
                )

class Store(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    logo = models.OneToOneField(StoreLogo, on_delete=models.CASCADE, null=True)
    cover = models.OneToOneField(StoreCover, on_delete=models.CASCADE, null=True)
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

class ProductPicture(models.Model):
    original = ProcessedImageField(
                    upload_to=build_product_picture_path,
                    processors=[
                        ResizeToFill(200, 200)
                    ],
                    format='JPEG'
                )

class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    picture = models.OneToOneField(ProductPicture, on_delete=models.CASCADE, null=True)
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
