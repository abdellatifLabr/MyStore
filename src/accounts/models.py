from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from profiles.models import Profile, Avatar

def create_profile(sender, instance, created, **kwargs):
    if not instance.is_staff:
        if created:
            avatar = Avatar()
            avatar.save()
            Profile.objects.create(user=instance, avatar=avatar)

post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
