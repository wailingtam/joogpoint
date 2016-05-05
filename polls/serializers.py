from rest_framework import serializers
from .models import Playlist, Track


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    establishment = serializers.ReadOnlyField(source='establishment.name')
    tracks = serializers.HyperlinkedRelatedField(many=True, view_name='track-detail', read_only=True)

    class Meta:
        model = Playlist
        fields = ('url', 'establishment', 'spotify_url', 'tracks')


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    playlist = serializers.ReadOnlyField(source='playlist.spotify_url')

    class Meta:
        model = Track
        fields = ('url', 'playlist', 'votes', 'order', 'spotify_uri')
