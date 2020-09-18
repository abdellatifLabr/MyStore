from django import forms
from django.contrib.auth import get_user_model

from .models import Store, Visit, Subscription, Product

class StoreForm(forms.ModelForm):
    cover = forms.ImageField(required=False)
    logo = forms.ImageField(required=False)

    class Meta:
        model = Store
        exclude = ('shipping', 'user', 'created', 'updated')

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
    quantity = forms.IntegerField(required=False)
