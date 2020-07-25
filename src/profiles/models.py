from django.db import models
from django.contrib.auth import get_user_model
from phone_field import PhoneField

class Profile(models.Model):
    bio = models.CharField(max_length=255, blank=True)
    phone = PhoneField(null=True)
    picture = models.ImageField(upload_to='profile-pictures')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
        