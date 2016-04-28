from polls.models import Playlist, Track
from polls.serializers import PlaylistSerializer, TrackSerializer
from rest_framework import permissions, viewsets
from establishments.permissions import IsOwnerOrReadOnly
import urllib
import json
from django.http import JsonResponse, HttpResponse
import spotipy
from rest_framework.decorators import detail_route, list_route
from django.dispatch import receiver
from django.db.models.signals import post_save
from polls.credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

class PlaylistViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # @detail_route(methods=['put'], url_path='change-playlist')
    # def set_playlist(self, request, pk):
    #     playlist = self.get_object()
    #     playlist.spotify_url = request.data['spotify_url'];
    #     playlist.save()
    #     return HttpResponse(playlist.spotify_url)


class TrackViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


def spotify_test(request):
    data = urllib.request.urlopen("https://api.spotify.com/v1/albums/0xM5ya1HwAoc8ubvL5GORB").read().decode("utf-8")
    dic = json.loads(data)
    return JsonResponse(dic)

import sys
import spotipy
import spotipy.util as util


def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print ("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))


@receiver(post_save, sender=Playlist)
def save_tracks(sender, **kwargs):
    scope = 'playlist-read-private'
    username = "wailing_10"
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
    # if token:
    #     sp = spotipy.Spotify(auth=token)
    #     playlists = sp.user_playlists(username)
    #     for playlist in playlists['items']:
    #         if playlist['owner']['id'] == username:
    #             print()
    #             print(playlist['name'])
    #             print ('  total tracks', playlist['tracks']['total'])
    #             results = sp.user_playlist(username, playlist['id'],
    #                                        fields="tracks,next")
    #             tracks = results['tracks']
    #             show_tracks(tracks)
    #             while tracks['next']:
    #                 tracks = sp.next(tracks)
    #                 show_tracks(tracks)
    # else:
    #     print("Can't get token for", username)
    # results = spotify.search(q='artist:' + "Arctic Monkeys", type='artist')
    # results = user_playlist(self.establishment.spotify_username)
    # data = urllib.request.urlopen(playlist_url).read().decode("utf-8")
    # dic = json.loads(data)
    # return HttpResponse(dic)

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)