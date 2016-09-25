from rest_framework import serializers
from .models import Establishment
from pygeocoder import Geocoder


class EstablishmentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    customers = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True, many=True)
    establishment_playlist = serializers.HyperlinkedRelatedField(many=False, view_name='playlist-detail',
                                                                 read_only=True)

    class Meta:
        model = Establishment
        fields = ('url', 'owner', 'name', 'address', 'city', 'postcode', 'country', 'latitude', 'longitude',
                  'spotify_username', 'lastfm_username', 'customers', 'establishment_playlist')

    def create(self, validated_data):
        establishment = Establishment.objects.create(**validated_data)
        full_address = " ".join((establishment.address, establishment.city, establishment.country))

        if Geocoder.geocode(full_address).valid_address:
            location = Geocoder.geocode(full_address)
            establishment.latitude = location.coordinates[0]
            establishment.longitude = location.coordinates[1]
            establishment.save()
        # else print error

        return establishment


class EstablishmentBasicInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Establishment
        fields = ('url', 'name', 'address', 'city', 'country', 'postcode', 'latitude', 'longitude', 'establishment_playlist')
