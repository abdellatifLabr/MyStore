from django import forms

from .models import Profile

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    
    class Meta:
        model = Profile
        exclude = ('avatar', 'user', 'created', 'updated')
