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
