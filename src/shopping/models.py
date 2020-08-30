from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from djmoney.templatetags.djmoney import money_localize
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

from order.models import OrderItem
from .utils import build_store_cover_path, build_store_logo_path, build_product_picture_path

class StoreLogo(models.Model):
    original = ProcessedImageField(
                    upload_to=build_store_logo_path,
                    processors=[
                        ResizeToFill(180, 180)
                    ],
                    format='JPEG',
                    default='img/store/logo/default.jpg'
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
                    upload_to=build_store_cover_path,
                    processors=[
                        ResizeToFill(820, 312)
                    ],
                    format='JPEG',
                    default='img/store/cover/default.jpg'
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
    shipping = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
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
                        ResizeToFill(400, 400)
                    ],
                    format='JPEG'
                )

class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    pictures = models.ManyToManyField(ProductPicture)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    quantity = models.PositiveIntegerField(default=1)
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def in_carts_units(self):
        in_cart_units = CartProduct.objects.filter(product_id=self.id)
        return in_cart_units.aggregate(result=Sum('quantity'))['result']
    
    @property
    def ordered_units(self):
        ordered_units = OrderItem.objects.filter(product_id=self.id)
        return ordered_units.aggregate(result=Sum('quantity'))['result']

    @property
    def units_left(self):
        units_left_count = self.quantity - self.in_carts_units - self.ordered_units
        return units_left_count

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='carts', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='carts', on_delete=models.CASCADE)

    @property
    def total(self):
        total = 0

        for product in self.cart_products.iterator():
            total += product.cost
        
        return total


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_products', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='cart_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def cost(self):
        return self.product.price.value * self.quantity

    def __str__(self):
        return f'{self.product} - {self.cart.user}'
    
    class Meta:
        ordering = ['-created']
