from django import forms
from django.contrib.auth import get_user_model

from .models import Store, Visit, Subscription, Product, Price

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ('logo', 'cover', 'user', 'created', 'updated')

class UpdateStoreForm(StoreForm):
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    closed = forms.BooleanField(required=False)
    workers = forms.ModelMultipleChoiceField(required=False, queryset=get_user_model().objects.all())


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('pictures', 'price', 'store', 'created', 'updated')

class UpdateProductForm(ProductForm):
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)


class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        exclude = ('product', 'created')

class UpdatePriceForm(PriceForm):
    value = forms.CharField(required=False)
