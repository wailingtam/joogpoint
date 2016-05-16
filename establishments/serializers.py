from rest_framework import serializers
from .models import Establishment


class EstablishmentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    customers = serializers.ReadOnlyField(source='customers.username')
    establishment_plays = serializers.HyperlinkedRelatedField(many=False, view_name='playlist-detail', read_only=True)

    class Meta:
        model = Establishment
        fields = ('url', 'owner', 'name', 'address', 'city', 'postcode', 'country', 'latitude', 'longitude',
                  'spotify_username', 'lastfm_username', 'customers', 'establishment_plays')
