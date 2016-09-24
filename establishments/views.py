from establishments.models import Establishment
from establishments.serializers import EstablishmentSerializer
from rest_framework import permissions, viewsets
from rest_framework import response, status
from establishments.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import detail_route, list_route
from django.db.models import Q
from pygeocoder import Geocoder


class EstablishmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    # Associating establishments with users
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        full_address = " ".join((instance.address, instance.city, instance.country))

        if Geocoder.geocode(full_address).valid_address:
            location = Geocoder.geocode(full_address)
            instance.latitude = location.coordinates[0]
            instance.longitude = location.coordinates[1]
            instance.save()
        # else error


    @list_route()
    def search(self, request):
        query = request.GET.get('query', '')
        query.replace('+', ' ')
        results = Establishment.objects.filter(Q(name__icontains=query) | Q(address__icontains=query) |
                                            Q(city__icontains=query) | Q(country__icontains=query))
        serializer = EstablishmentSerializer(results, context={'request': request}, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['put'], url_path='check-in')
    def check_in(self, request, pk):
        establishment = Establishment.objects.filter(pk=pk)
        if establishment:
            if establishment[0].customers.filter(pk=request.user.id).exists():
                establishment[0].customers.remove(request.user)
            else:
                establishment[0].customers.add(request.user)
            serializer = EstablishmentSerializer(establishment[0], context={'request': request})
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response(status=status.HTTP_404_NOT_FOUND)