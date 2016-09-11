from establishments.models import Establishment
from establishments.serializers import EstablishmentSerializer
from rest_framework import permissions, viewsets
from establishments.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import detail_route, list_route
from django.http import JsonResponse, HttpResponse
from django.db.models import Q


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

    @list_route()
    def search(self, request):
        query = request.GET.get('query', '')
        data = Establishment.objects.filter(Q(name__icontains=query) | Q(address__icontains=query) |
                                            Q(city__icontains=query) | Q(country__icontains=query)).values()
        return JsonResponse(dict(results=list(data)))

    @detail_route(methods=['post'], url_path='check-in')
    def check_in(self, request, pk):
        e = Establishment.objects.get(pk=pk)
        if e.customers.filter(pk=request.user.id).exists():
            e.customers.remove(request.user)
            return HttpResponse(request.user.username + " unchecked-in at " + e.name)
        else:
            e.customers.add(request.user)
            return HttpResponse(request.user.username + " checked-in at " + e.name)


