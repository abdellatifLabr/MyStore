from django import forms
from django.contrib.auth import get_user_model

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
