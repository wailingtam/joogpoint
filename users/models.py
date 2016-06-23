from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)


class Profile(models.Model):
    # This line is required. Links Profile to a User model instance.
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')

    spotify_username = models.CharField(max_length=50, blank=True)
    facebook_username = models.CharField(max_length=50, blank=True)
    twitter_username = models.CharField(max_length=15, blank=True)
    fav_artists = models.TextField(blank=True, null=True)
    fav_genres = models.TextField(blank=True, null=True)

    # representation of the object
    def __str__(self):
        return self.user.username
