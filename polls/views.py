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
from polls.credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, LASTFM_API_KEY
import spotipy
import spotipy.util as util
from rest_framework.decorators import api_view


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
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
    return HttpResponse(token)


@api_view()
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
                'image': playlist['images']
            }
            data['results'].append(pl)
    else:
        return HttpResponse("Can't get token for", username)

    return JsonResponse(data)


@api_view()
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


@api_view()
def song_search(request):
    # Encode spaces with the hex code %20 or +,
    # genre  Use double quotation marks (%22) around the genre keyword string if it contains spaces.
    # Limit Default: 10. Minimum: 1. Maximum: 50
    sp = spotipy.Spotify()
    query = request.GET.get('value')
    results = sp.search(q=query, type='track')
    data = {
        'tracks': [],
        'next': results['tracks']['next']
    }
    for r in results['tracks']['items']:
        tr = {
            'artist': []
        }
        for a in r['artists']:
            tr['artist'].append(a['name'])
        tr['images'] = r['album']['images']
        tr['explicit'] = r['explicit']
        tr['spotify_uri'] = r['uri']
        tr['name'] = r['name']
        data['tracks'].append(tr)
    return JsonResponse(data)


@api_view(['POST'])
def submit_song_request(request):
    username = Establishment.objects.get(pk=request.data['establishment']).spotify_username
    scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
    playlist = Establishment.objects.get(pk=request.data['establishment']).playlist

    if token:
        # add track to spotify playlist
        sp = spotipy.Spotify(auth=token)
        resp = sp.user_playlist_add_tracks(user=username, playlist_id=playlist.spotify_url,
                                           tracks=[request.data['spotify_uri']])
        # save track with 1 vote
        no_songs = Track.objects.filter(playlist=playlist.id).count()
        Track.objects.create(playlist_id=playlist.id, spotify_uri=request.data['spotify_uri'], order=no_songs,
                             votes=1)
        # sort playlist
        sort_playlist(request.data['establishment'], playlist.id)
        new_order = Track.objects.get(spotify_uri=request.data['spotify_uri'], playlist=playlist).order
        results = sp.user_playlist_reorder_tracks(user=username, playlist_id=playlist.spotify_url, range_start=no_songs,
                                                  insert_before=new_order, snapshot_id=resp['snapshot_id'])
        return JsonResponse(results)
    else:
        return HttpResponse("Can't get token for", username)


@api_view()
def get_most_recent_track(request):
    return JsonResponse(get_most_recent_track2(request.GET.get('establishment')))


def get_most_recent_track2(establishment_pk):
    username = Establishment.objects.get(pk=establishment_pk).lastfm_username
    results = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" +
                                     username + "&api_key=" + LASTFM_API_KEY + "&format=json&limit=1"
                                     ).read().decode("utf-8")
    dic = json.loads(results)
    data = {
        'now_playing': True,
        'spotify_uri': ""
    }
    for t in dic['recenttracks']['track']:
        if len(dic['recenttracks']['track']) > 1 and '@attr' in t \
                or len(dic['recenttracks']['track']) == 1:
                data['name'] = t['name']
                data['artist'] = t['artist']['#text']
                data['album'] = t['album']['#text']
                if '@attr' not in t:
                    data['now_playing'] = False

    # Seach song on Spotify
    sp = spotipy.Spotify()
    query = " artist:" + str(data['artist']) + " track:" + str(data['name'])
    results = sp.search(q=query, type='track')
    tracks = []
    for r in results['tracks']['items']:
        tr = {
            'artist': []
        }
        for a in r['artists']:
            tr['artist'].append(a['name'])
        tr['spotify_uri'] = r['uri']
        tr['name'] = r['name']
        tracks.append(tr)

    # Search song in saved tracks
    for t in tracks:
        if Track.objects.filter(spotify_uri=t['spotify_uri'],
                                playlist=Establishment.objects.get(pk=establishment_pk).playlist):
            data['spotify_uri'] = t['spotify_uri']
            data['name'] = t['name']
            data['artist'] = t['artist']

    return data


def sort_playlist(establishment_pk, playlist):
    current_song = get_most_recent_track2(establishment_pk)
    current_track = Track.objects.get(spotify_uri=current_song['spotify_uri'], playlist=playlist)
    next_tracks = Track.objects.order_by('-votes', 'order').filter(playlist=playlist, order__gt=current_track.order)
    new_order = current_track.order + 1
    for nt in next_tracks:
        nt.order = new_order
        nt.save()
        new_order += 1


@api_view(['PUT'])
def upvote(request):
    data = json.loads(request.body.decode('utf-8'))
    playlist = Establishment.objects.get(pk=data['establishment']).playlist
    voted_track = Track.objects.get(spotify_uri=data['spotify_uri'], playlist=playlist.id)
    voted_track.votes += 1
    voted_track.save()
    sort_playlist(data['establishment'], playlist.id)
    new_order = Track.objects.get(spotify_uri=data['spotify_uri'], playlist=playlist).order

    username = Establishment.objects.get(pk=data['establishment']).spotify_username
    scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)

    if token:
        # reorder spotify playlist
        sp = spotipy.Spotify(auth=token)
        results = sp.user_playlist_reorder_tracks(user=username, playlist_id=playlist.spotify_url,
                                                  range_start=voted_track.order, insert_before=new_order)
    else:
        return HttpResponse("Can't get token for", username)

    return JsonResponse(results)

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
