from django.db import models


class Playlist (models.Model):
    establishment = models.OneToOneField('establishments.Establishment',
                                         on_delete=models.CASCADE,
                                         related_name='playlist')
    spotify_url = models.URLField(blank=True)
    original_creator = models.CharField(max_length=100, blank=True)
    original_spotify_url = models.URLField(max_length=100, blank=True)


class Track (models.Model):
    playlist = models.ForeignKey('Playlist', related_name='tracks')
    spotify_uri = models.CharField(max_length=36)
    votes = models.IntegerField(default=0)
    order = models.IntegerField()
    requested = models.BooleanField(default=False)

    class Meta:
        unique_together = ('playlist', 'spotify_uri')
