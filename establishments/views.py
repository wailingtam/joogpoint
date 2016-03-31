from establishments.models import Establishment
from establishments.serializers import EstablishmentSerializer
from rest_framework import generics, permissions, viewsets
from establishments.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'establishments': reverse('establishment-list', request=request, format=format)
#     })


# class EstablishmentList(generics.ListCreateAPIView):
#     queryset = Establishment.objects.all()
#     serializer_class = EstablishmentSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
#
#     # Associating establishments with users
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class EstablishmentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Establishment.objects.all()
#     serializer_class = EstablishmentSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class EstablishmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)