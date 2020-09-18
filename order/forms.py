from django import forms

from .models import Address, DiscountCode, Order

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'created', 'updated')

class UpdateAddressForm(AddressForm):
    country = forms.CharField(required=False)
    city = forms.CharField(required=False)
    street = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)


class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        exclude = ('store', 'created', 'updated')

class UpdateDiscountCodeForm(DiscountCodeForm):
    code = forms.CharField(required=False)
    value = forms.IntegerField(required=False)
    expiry = forms.DateTimeField(required=False)
