from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from polls.models import Playlist


class Establishment(models.Model):
    owner = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              related_name='owner_of')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    spotify_username = models.CharField(max_length=100)
    lastfm_username = models.CharField(max_length=100)
    customers = models.ManyToManyField('auth.User',
                                       related_name='checked_in')

    class Meta:
        ordering = ('name', 'country', 'city')

    def __str__(self):
        return self.name


# This code is triggered whenever a new establishment has been created and saved
# to the database
@receiver(post_save, sender=Establishment)
def create_playlist(sender, instance=None, created=False, **kwargs):
    if created:
        Playlist.objects.create(establishment=instance)
