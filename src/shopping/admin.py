from django.contrib import admin

from .models import (
    Store,
    StoreLogo,
    StoreCover,
    Visit, 
    Subscription, 
    RecruitmentRequest, 
    Product, 
    ProductPicture,
    Price, 
    Cart,
    CartProduct,
)

admin.site.register(Store)
admin.site.register(StoreLogo)
admin.site.register(StoreCover)
admin.site.register(Visit)
admin.site.register(Subscription)
admin.site.register(RecruitmentRequest)
admin.site.register(Product)
admin.site.register(ProductPicture)
admin.site.register(Price)
admin.site.register(Cart)
admin.site.register(CartProduct)
