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
            if establ_pl.spotify_url != data['spotify_url']:
                username = establ_pl.establishment.spotify_username
                scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
                token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                                   client_secret=SPOTIFY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIFY_REDIRECT_URI)
                if token:
                    sp = spotipy.Spotify(auth=token)
                    # Get tracks from the original playlist
                    tracks = sp.user_playlist(data['owner'], data['spotify_url'],
                                              fields="name, tracks.items(track(uri))")
                    # Create a new playlist for the copy
                    pl = sp.user_playlist_create(username, "jp-" + tracks['name'], public=False)
                    # Remove tracks from previous playlist
                    Track.objects.filter(playlist_id=pk).delete()
                    # Get the tracks uris from the original playlist and create their track instances
                    tracks_uris = []
                    track_order = 0
                    for tr in tracks['tracks']['items']:
                        tracks_uris.append(tr['track']['uri'])
                        Track.objects.create(playlist_id=pk, spotify_uri=tr['track']['uri'], order=track_order)
                        track_order += 1
                    # Add tracks to the new playlist
                    snapshot_id = sp.user_playlist_add_tracks(username, pl['id'], tracks_uris)
                    # Save new playlist url
                    establ_pl.spotify_url = pl['external_urls']['spotify']
                    establ_pl.save()

                else:
                    return HttpResponse("Can't get token for", username)
            return HttpResponse(establ_pl.spotify_url, status=200)


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
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
    if token:
        data = {"results": []}
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            pl = {
                'spotify_url': playlist['external_urls']['spotify'],
                'name': playlist['name'],
                'owner': playlist['owner']['id'],
                'image': playlist['images'][0]['url']
            }
            data['results'].append(pl)
    else:
        return HttpResponse("Can't get token for", username)

    return JsonResponse(data)


def get_playlist_tracks(request):
    username = Establishment.objects.get(pk=request.GET.get('establishment')).spotify_username
    scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
    if token:
        sp = spotipy.Spotify(auth=token)
        tracks = sp.user_playlist(request.GET.get('owner'), request.GET.get('spotify_url'),
                                  fields="name, images, tracks.items(track(name, artists, album(images)))")
    else:
        return HttpResponse("Can't get token for", username)

    return JsonResponse(tracks)

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
