from rest_framework import serializers
from .models import Establishment


class EstablishmentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Establishment
        fields = ('url', 'owner', 'name', 'street', 'number', 'city', 'postcode', 'country', 'latitude', 'longitude')
