from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    owner_of = serializers.HyperlinkedRelatedField(
        many=True, view_name='establishment-detail', read_only=True)
    checked_in = serializers.HyperlinkedRelatedField(
        many=True, view_name='establishment-detail', read_only=True)
    voted = serializers.HyperlinkedRelatedField(
        many=True, view_name='track-detail', read_only=True)
    requested = serializers.HyperlinkedRelatedField(
        many=True, view_name='track-detail', read_only=True)
    user_profile = serializers.HyperlinkedRelatedField(
        many=False, view_name='profile-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'owner_of',
                  'checked_in', 'voted', 'requested',
                  'user_profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class BasicUserInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'checked_in', 'voted', 'requested')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = BasicUserInfoSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('url', 'user', 'spotify_username', 'facebook_username',
                  'twitter_username', 'fav_artists', 'fav_genres')
