from establishments.models import Establishment
from establishments.serializers import EstablishmentSerializer
from rest_framework import permissions, viewsets
from establishments.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response


class EstablishmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # Associating establishments with users
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @list_route()
    def search(self, request):
        data = Establishment.objects.filter(name__icontains=request.GET.get('name', '')).values('id', 'name', 'address',
                                                                                                'postcode', 'city')
        return Response(dict(results=list(data)))
