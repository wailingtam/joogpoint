from rest_framework import serializers
from .models import Playlist, Track


class BasicTrackInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = ('id', 'title', 'artist', 'votes', 'order', 'in_playlist')


class VotedOrRequestedTrackSerializer(serializers.ModelSerializer):
    establishment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Track
        fields = ('id', 'title', 'artist', 'establishment')

    def get_establishment(self, obj):
        return obj.playlist.establishment.name


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    establishment = serializers.ReadOnlyField(source='establishment.name')
    playlist_of = BasicTrackInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ('url', 'establishment', 'spotify_url', 'original_creator',
                  'original_spotify_url', 'explicit_lyrics', 'playlist_of')


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    playlist = serializers.ReadOnlyField(source='playlist.spotify_url')
    request_user = serializers.ReadOnlyField(source='request_user.username')
    voters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Track
        fields = ('url', 'title', 'artist', 'playlist', 'spotify_uri', 'votes',
                  'order', 'request_user', 'voters')

    def get_voters(self, obj):
        users = []
        for voter in obj.voters.all():
            users.append({"username": voter.username, "id": voter.id})
        return users
