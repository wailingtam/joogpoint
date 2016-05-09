from rest_framework import serializers
from .models import Establishment


class EstablishmentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    playlist = serializers.HyperlinkedRelatedField(view_name='playlist-detail', read_only=True)

    class Meta:
        model = Establishment
        fields = ('url', 'owner', 'name', 'address', 'city', 'postcode', 'country', 'latitude', 'longitude',
                  'spotify_username', 'lastfm_username', 'playlist')

