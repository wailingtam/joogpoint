from rest_framework import serializers
from .models import Playlist, Track


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    establishment = serializers.ReadOnlyField(source='establishment.name')
    playlist_of = serializers.HyperlinkedRelatedField(many=True, view_name='track-detail', read_only=True)

    class Meta:
        model = Playlist
        fields = ('url', 'establishment', 'spotify_url', 'original_creator', 'original_spotify_url', 'explicit_lyrics',
                  'playlist_of')


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    playlist = serializers.ReadOnlyField(source='playlist.spotify_url')
    request_user = serializers.ReadOnlyField(source='request_user.username')
    voters = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)

    class Meta:
        model = Track
        fields = ('url', 'playlist', 'spotify_uri', 'votes', 'order', 'request_user', 'voters')
