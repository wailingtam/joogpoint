from polls.models import Playlist, Track
from polls.serializers import PlaylistSerializer, TrackSerializer
from rest_framework import generics, permissions, viewsets
from establishments.permissions import IsOwnerOrReadOnly
import urllib
import json
from django.http import JsonResponse

class PlaylistViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class TrackViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Track.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


def spotify_test(request):
    data = urllib.request.urlopen("https://api.spotify.com/v1/albums/0xM5ya1HwAoc8ubvL5GORB").read().decode("utf-8")
    dic = json.loads(data)
    return JsonResponse(dic)


# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
