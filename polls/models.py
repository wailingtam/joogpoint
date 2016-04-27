from django.db import models


class Playlist (models.Model):
    owner = models.ForeignKey('auth.User', related_name='playlists')
    establishment = models.OneToOneField('establishments.Establishment',
                                         on_delete=models.CASCADE,
                                         related_name='playlist')
    spotify_url = models.URLField()


class Track (models.Model):
    playlist = models.ForeignKey('Playlist', related_name='tracks')
    spotify_url = models.URLField()
    votes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('playlist', 'spotify_url')
