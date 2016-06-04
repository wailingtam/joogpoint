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
import spotipy
import spotipy.util as util
from rest_framework.decorators import api_view
from polls.permissions import IsOwnerOrReadOnly
from joogpoint.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, LASTFM_API_KEY


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    @detail_route(methods=['put'], url_path='set-playlist')
    def copy_set_playlist(self, request, pk):
        if request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            playlist = Playlist.objects.get(pk=pk)
            if playlist.spotify_url != data['spotify_url']:
                username = playlist.establishment.spotify_username
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
                    playlist.spotify_url = pl['external_urls']['spotify']
                    playlist.original_creator = data['owner']
                    playlist.original_spotify_url = data['spotify_url']
                    playlist.save()

                else:
                    return HttpResponse("Can't get token for", username)
            return HttpResponse(playlist.spotify_url)

    @detail_route(methods=['post'], url_path='request-song')
    def submit_song_request(self, request, pk):
        playlist = Playlist.objects.get(pk=pk)
        if request.data['explicit_lyrics'] == "False":
            if not Track.objects.filter(playlist=playlist, spotify_uri=request.data['spotify_uri']):
                username = playlist.establishment.spotify_username
                scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
                token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                                   client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)

                if token:
                    # add track to spotify playlist
                    sp = spotipy.Spotify(auth=token)
                    resp = sp.user_playlist_add_tracks(user=username, playlist_id=playlist.spotify_url,
                                                       tracks=[request.data['spotify_uri']])
                    # save track with 1 vote
                    no_songs = Track.objects.filter(playlist=playlist.id).count()
                    tr = Track.objects.create(playlist_id=playlist.id, spotify_uri=request.data['spotify_uri'],
                                              order=no_songs, votes=1, request_user=request.user)
                    tr.voters.add(request.user)
                    # sort playlist
                    sort_playlist(playlist)
                    new_order = Track.objects.get(spotify_uri=request.data['spotify_uri'], playlist=playlist).order
                    results = sp.user_playlist_reorder_tracks(user=username, playlist_id=playlist.spotify_url,
                                                              range_start=no_songs,
                                                              insert_before=new_order, snapshot_id=resp['snapshot_id'])
                    return JsonResponse(results)
                else:
                    return HttpResponse("Can't get token for", username)
            else:
                return HttpResponse("The song is already in the playlist.")
        else:
            return HttpResponse("Explicit lyrics are not allowed.")

    @detail_route(methods=['put'], permission_classes=[IsOwnerOrReadOnly], url_path='reset-votes')
    def reset_votes(self, request, pk):
        Track.objects.filter(playlist_id=pk).update(votes=0)
        return HttpResponse("Votes reset")

    @detail_route(methods=['put'], url_path='reset-playlist')
    def reset_playlist(self, request, pk):
        playlist = Playlist.objects.get(pk=pk)
        username = playlist.establishment.spotify_username
        scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
        token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
                                           client_secret=SPOTIFY_CLIENT_SECRET,
                                           redirect_uri=SPOTIFY_REDIRECT_URI)

        if token:
            sp = spotipy.Spotify(auth=token)

            # Empty the modified playlist
            old_tracks_uris = Track.objects.filter(playlist_id=playlist.id).values_list('spotify_uri', flat=True)
            sp.user_playlist_remove_all_occurrences_of_tracks(user=username, playlist_id=playlist.spotify_url,
                                                              tracks=old_tracks_uris)
            # Remove tracks from modified playlist
            Track.objects.filter(playlist_id=playlist.id).delete()

            # Get tracks from the original playlist
            tracks = sp.user_playlist(playlist.original_creator, playlist.original_spotify_url,
                                      fields="tracks.items(track(uri))")

            # Get the tracks uris from the original playlist and create their track instances
            tracks_uris = []
            track_order = 0
            for tr in tracks['tracks']['items']:
                tracks_uris.append(tr['track']['uri'])
                Track.objects.create(playlist_id=playlist.id, spotify_uri=tr['track']['uri'], order=track_order)
                track_order += 1

            # Add tracks to the playlist
            resp = sp.user_playlist_add_tracks(username, playlist.spotify_url, tracks_uris)
            return JsonResponse(resp)

        else:
            return HttpResponse("Can't get token for", username)

    @detail_route(methods=['get'], url_path='current-song')
    def get_most_recent_track(self, request, pk):
        return JsonResponse(get_most_recent_track2(pk))

    @detail_route(methods=['get'], url_path='playlist-on')
    def playlist_is_on(self, request, pk):
        playlist = Playlist.objects.get(pk=pk)
        username = playlist.establishment.lastfm_username
        results = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" +
                                         username + "&api_key=" + LASTFM_API_KEY + "&format=json&limit=1"
                                         ).read().decode("utf-8")
        dic = json.loads(results)

        return HttpResponse(len(dic['recenttracks']['track']) > 1)


class TrackViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(methods=['put'], url_path='vote')
    def vote(self, request, pk):
        voted_track = Track.objects.get(pk=pk)
        if not voted_track.voters.filter(pk=request.user.id).exists():
            playlist = voted_track.playlist
            voted_track.votes += 1
            voted_track.save()
            voted_track.voters.add(request.user)
            sort_playlist(playlist)
            new_order = Track.objects.get(pk=pk).order

            username = playlist.establishment.spotify_username
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
        else:
            return HttpResponse("You've already voted this song.")


# def get_account_access(request):
#     username = Establishment.objects.get(pk=request.GET.get('establishment')).spotify_username
#     scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
#     token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
#                                        client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
#     return HttpResponse(token)


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
def get_spotify_playlist_tracks(request):
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


def get_most_recent_track2(playlist_pk):
    playlist = Playlist.objects.get(pk=playlist_pk)
    username = playlist.establishment.lastfm_username
    results = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" +
                                     username + "&api_key=" + LASTFM_API_KEY + "&format=json&limit=1"
                                     ).read().decode("utf-8")
    dic = json.loads(results)
    data = {
        'now_playing': True,
        'spotify_uri': ""
    }
    for t in dic['recenttracks']['track']:
        # if there are the currently playing song and the last played song (>1) and it's the currently playing song
        # or there is only the last played song (==1)
        if len(dic['recenttracks']['track']) > 1 and '@attr' in t \
                or len(dic['recenttracks']['track']) == 1:
                data['name'] = t['name']
                data['artist'] = t['artist']['#text']
                data['album'] = t['album']['#text']
                if '@attr' not in t:
                    data['now_playing'] = False

    # Search song on Spotify
    sp = spotipy.Spotify()
    query = str(data['artist']) + " " + str(data['name'])
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
        if Track.objects.filter(spotify_uri=t['spotify_uri'], playlist=playlist):
            data['spotify_uri'] = t['spotify_uri']
            data['name'] = t['name']
            data['artist'] = t['artist']
            break

    return data


def sort_playlist(playlist):
    current_song = get_most_recent_track2(playlist.id)
    current_track = Track.objects.get(spotify_uri=current_song['spotify_uri'], playlist=playlist)
    next_tracks = Track.objects.order_by('-votes', 'order').filter(playlist=playlist, order__gt=current_track.order)
    new_order = current_track.order + 1
    for nt in next_tracks:
        nt.order = new_order
        nt.save()
        new_order += 1


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
