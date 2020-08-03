from django.db import models
from django.contrib.auth import get_user_model
from phone_field import PhoneField
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

from .utils import build_avatar_path

class Avatar(models.Model):
    original = ProcessedImageField(
        upload_to=build_avatar_path,
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

class Profile(models.Model):
    bio = models.CharField(max_length=255, blank=True)
    phone = PhoneField(null=True)
    avatar = models.OneToOneField(Avatar, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
        