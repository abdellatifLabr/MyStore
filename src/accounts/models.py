from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from profiles.models import Profile

def create_profile(sender, instance, **kwargs):
    Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
