from django.db import models


class Playlist (models.Model):
    establishment = models.OneToOneField('establishments.Establishment',
                                         on_delete=models.CASCADE,
                                         related_name='establishment_plays')
    spotify_url = models.URLField(blank=True)
    original_creator = models.CharField(max_length=100, blank=True)
    original_spotify_url = models.URLField(max_length=100, blank=True)
    explicit_lyrics = models.BooleanField(default=False)


class Track (models.Model):
    playlist = models.ForeignKey('Playlist',
                                 on_delete=models.CASCADE,
                                 related_name='playlist_of')
    spotify_uri = models.CharField(max_length=36)
    votes = models.IntegerField(default=0)
    order = models.IntegerField()
    request_user = models.ForeignKey('auth.User',
                                     related_name='requested',
                                     blank=True,
                                     null=True)
    voters = models.ManyToManyField('auth.User',
                                    related_name='voted')

    class Meta:
        unique_together = ('playlist', 'spotify_uri')
