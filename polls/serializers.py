from rest_framework import serializers
from .models import Playlist, Track


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    establishment = serializers.ReadOnlyField(source='establishment.name')

    class Meta:
        model = Playlist
        fields = ('url', 'establishment', 'spotify_url')


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    playlist = serializers.ReadOnlyField(source='playlist.spotify_url')

    class Meta:
        model = Track
        fields = ('url', 'playlist', 'votes', 'spotify_url')
