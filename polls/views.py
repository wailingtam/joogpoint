from polls.models import Playlist, Track
from polls.serializers import PlaylistSerializer, TrackSerializer
from rest_framework import permissions, viewsets
from establishments.models import Establishment
import urllib
import json
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import detail_route, list_route
from django.dispatch import receiver
from django.db.models.signals import post_save
from polls.credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_USERNAME
import spotipy
import spotipy.util as util


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(methods=['put'], url_path='set-playlist')
    def copy_set_playlist(self, request, pk):
        if request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            establ_pl = Playlist.objects.get(pk=pk)
            username = establ_pl.establishment.spotify_username
            scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
            username = SPOTIFY_USERNAME
            token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
            if token:
                sp = spotipy.Spotify(auth=token)
                # Get tracks from the original playlist
                tracks = sp.user_playlist(data['owner'], data['spotify_id'], fields="name, tracks.items(track(uri))")
                # Create a new playlist for the copy
                pl = sp.user_playlist_create(username, "jp-" + tracks['name'], public=False)
                # Get the tracks uris from the original playlist
                tracks_uris = []
                for tr in tracks['tracks']['items']:
                    tracks_uris.append(tr['track']['uri'])
                # Add tracks to the new playlist
                snapshot_id = sp.user_playlist_add_tracks(username, pl['id'], tracks_uris)
                # Save new playlist url
                establ_pl.spotify_url = pl['external_urls']['spotify']
                establ_pl.save()

            else:
                return HttpResponse("Can't get token for", username)
            return HttpResponse(status=200)


class TrackViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


def spotify_test(request):
    # data = urllib.request.urlopen("https://api.spotify.com/v1/albums/0xM5ya1HwAoc8ubvL5GORB").read().decode("utf-8")
    # dic = json.loads(data)
    # return JsonResponse(dic)
    return HttpResponse(request.user.username)


def get_account_access(request):
    username = Establishment.objects.get(pk=request.GET.get('establishment')).spotify_username
    scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
    username = SPOTIFY_USERNAME
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
    return HttpResponse(token)


def get_spotify_playlists(request):
    username = Establishment.objects.get(pk=request.GET.get('establishment')).spotify_username
    scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
    username = SPOTIFY_USERNAME
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
    if token:
        data = {"results": []}
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            pl = {
                'id': playlist['id'],
                'name': playlist['name'],
                'owner': playlist['owner']['id'],
                'image': playlist['images'][0]['url']
            }
            data['results'].append(pl)
    else:
        return HttpResponse("Can't get token for", username)

    return JsonResponse(data)


# @receiver(post_save, sender=Playlist)
# def save_tracks(sender, **kwargs):
#     scope = 'playlist-read-private, playlist-modify-public, playlist-modify-private'
#     username = SPOTIFY_USERNAME
#     token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
#                                        client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
#     if token:
#         sp = spotipy.Spotify(auth=token)
#         playlists = sp.user_playlists(username)
#         # print(type(playlists))
#         # return HttpResponse(playlists)
#         for playlist in playlists['items']:
#             if playlist['owner']['id'] == username:
#                 print()
#                 print(playlist['name'])
#                 print ('  total tracks', playlist['tracks']['total'])
#                 results = sp.user_playlist(username, playlist['id'],
#                                            fields="tracks,next")
#                 tracks = results['tracks']
#                 show_tracks(tracks)
#                 while tracks['next']:
#                     tracks = sp.next(tracks)
#                     show_tracks(tracks)
#     else:
#         print("Can't get token for", username)

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
