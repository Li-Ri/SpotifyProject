import json
import time
import numpy as np
import requests
import spotipy
import spotipy.util as util
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


class Favourites:

    def current_playlists(self, scope='playlist-read-collaborative'):

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        playlists = {}

        cur_play = self.sp.current_user_playlists(limit=50)

        for play in range(len(cur_play)):

            playlists[cur_play['items'][play]['name']] = cur_play['items'][play]['id']

        return playlists
    @staticmethod
    def playlist_create(name, scope='playlist-modify'):

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        for i in range(len(sp.current_user_playlists())):

            if sp.current_user_playlists()['items'][i]['name'] == name:

                print(f'{name} playlist alrady exists try adding updating songs')
                break
            else:

                return sp.user_playlist_create('117039222', name)

    def current_top_artists(self, limit=1, scope="user-top-read"):

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        top_artists = []
       
        artists = self.sp.current_user_top_artists(limit=limit)['items']
 
        for i in range(len(artists)):
            top_artists.append('spotify:artist:'+artists[i]['id'])

        return top_artists

    def get_top_songs(self,scope='user-top-read', top_artists=[]):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        tracks = []


        for i in range(len(top_artists)):
            for j in range(10):
                tracks.append(self.sp.artist_top_tracks(top_artists[i],'US')['tracks'][j]['uri'])
                

        return tracks
    def add_top_songs_to_playlist(self, name, scope='playlist-modify', tracks=[]):

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        playlists = self.current_playlists()

        for track in tracks:

            self.sp.playlist_add_items(playlists[name],[track])

        print(str(len(tracks)) + ' Songs added To playlist!!')

    def read_recently_played(self, scope='user-read-recently-played'):

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        
        items = self.sp.current_user_recently_played(limit=50)['items']

        track_uris = []
        for track in range(len(items)):
            track_uris.append(items[track]['track']['id'])

        return track_uris

class AudioFeatures(Favourites):

    def analyze_audio(self,token=None,scope='user-top-read'):

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        tracks = self.read_recently_played()
        urls = ["https://api.spotify.com/v1/audio-features/"+ track for track in tracks]

        audio_features = []
    
        if token:
            for url in urls:
                with requests.session() as sesh:
                    header = {'Authorization': 'Bearer {}'.format(token)}
                    response= sesh.get(url, headers=header)
                    feature = str(bs(response.content, 'html.parser'))
                    audio_features.append(json.loads(feature))

        else:
            print('invalid token')
        
        return audio_features

    def pull_audio_dataset(self, name, token=None):

        data_all = self.analyze_audio(token)

        pulled_data = [] 

        for data in range(len(data_all)):
            pulled_data.append(data_all[data][name])

        return pulled_data
        
        





if __name__ == '__main__':

    play = AudioFeatures()
    scope='user-top-read'
    token = util.prompt_for_user_token(scope=scope, client_id='',client_secret='')
    print(play.analyze_audio(token))
