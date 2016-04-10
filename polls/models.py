from django.db import models


class Playlist (models.Model):
    establishment = models.ForeignKey('establishments.Establishment', related_name='playlist')
    url = models.URLField()


class Track (models.Model):
    playlist = models.ForeignKey('Playlist', related_name='tracks')
    url = models.URLField()
    votes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('playlist', 'url')
