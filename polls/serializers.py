from rest_framework import serializers
from .models import Playlist, Track
from django.contrib.auth.models import User


class BasicTrackInfoSerializer(serializers.ModelSerializer):
    request_user_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Track
        fields = ('id', 'title', 'artist', 'votes', 'order', 'in_playlist', 'request_user_id', 'cover_image_url')

    def get_request_user_id(self, obj):
        if isinstance(obj.request_user, User):
            return obj.request_user.user_profile.id
        return -1


class VotedOrRequestedTrackSerializer(serializers.ModelSerializer):
    establishment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Track
        fields = ('id', 'title', 'artist', 'establishment', 'cover_image_url')

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
                  'order', 'request_user', 'voters', 'cover_image_url')

    def get_voters(self, obj):
        users = []
        for voter in obj.voters.all():
            users.append({"username": voter.username, "profile_id": voter.user_profile.id})
        return users
