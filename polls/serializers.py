from rest_framework import serializers
from .models import Playlist, Track


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    establishment = serializers.ReadOnlyField(source='establishment.name')

    class Meta:
        model = Playlist
        fields = ('url', 'owner', 'establishment', 'spotify_url')


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    playlist = serializers.ReadOnlyField(source='playlist.url')

    class Meta:
        model = Track
        fields = ('url', 'playlist', 'votes', 'spotify_url')
