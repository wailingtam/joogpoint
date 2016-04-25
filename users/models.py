from django.db import models
from django.contrib.auth.models import User


# class UserProfile(models.Model):
#     # This line is required. Links UserProfile to a User model instance.
#     user = models.OneToOneField(User)
#
#     spotify_username = models.CharField(max_length=50, blank=True)
#     # user = models.ForeignKey(User)
#
#     # representation of the object
#     def __str__(self):
#         return self.user.username
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)