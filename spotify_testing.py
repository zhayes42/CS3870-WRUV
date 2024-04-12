import os
import pandas as pd
import numpy as np
import matplotlib as plt

from bs4 import BeautifulSoup
import requests

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def main():
    token = spotify_connect()
    # note: Radiohead was in the example online, I did not think oh yes, Radiohead lol
    #print(get_genre_by_artist(token, 'Radiohead'))
    #print(spotify_search_song(token, 'Joni Mitchell', 'California'))
    #billboard_songs("beyonce", "Drunk In Love")
    #print(web_scrape_bb("faye webster"))
    #print(web_scrape_bb("beyonce"))
    spotify_search_song(token, "Taylor Swift", "Dress")

# global variable for valid genres in spinitron
GENRES = ['Rock',
 'Folk',
 'Electronic',
 'R&B/Soul',
 'World',
 'Hip Hop/Rap',
 'Reggae',
 'Classical',
 'Jazz',
 'Heavy Metal',
 'Blues',
 'Country',
 'Electro',
 'Metal',
 'R&B/Soul/Funk',
 'Rap/Hip Hop',
 'R&B',
 'R & B',
 'Reggaeton',
 'Experimental']

for g in range(len(GENRES)):
    GENRES[g] = (str(GENRES[g])).lower()


# function to interface with Spotify Web API app (created with id and secret below) STILL WIP!
def spotify_connect():
    # technically insecure to have client secret displayed like this (environment variable)
    CLIENT_ID = '344d3b062e344710a5bdb8427358a31d'
    CLIENT_SECRET = '9f886dde51184f989b1aff4f5ffb21f8'
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    auth_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        requests_session=True)

    sp = spotipy.Spotify(auth_manager=auth_manager)
    # this is our connection which we will need for any future query
    return sp


def get_genre_by_artist(sp, artist_name):
    # spotify queries are all based on Spotify URI IDs and usually return in JSON
    results = sp.search(q='artist:' + artist_name, type='artist', limit=10)
    # make sure that the result is for the artist we want
    result_name = results['artists']['items'][0]['name']
    i = 0
    while (result_name != artist_name) & (i < 10):
        result_name = results['artists']['items'][i]['name']
        i += 1
    genres = results['artists']['items'][0]['genres']  # for top result (in this case accurate, but probably not always)
    id = results['artists']['items'][0]['id']

    print(f'{artist_name} is associated with {genres}')
    for genre in genres:
        if genre in GENRES:
            # print(f'solution = {genre}')
            return genre
    return 'NA'


# next step: instead of returning result_string, return dictionary of values OR empty dictionary of NAs?
def spotify_search_song(sp, artist_name, song_name):
    # when i search california, it gives me teenage dream by katy Perry so not sure how well this works
    results = sp.search(q='track:' + song_name, type='track', limit=10)
    results_title = results['tracks']['items'][0]['name']
    results_album = results['tracks']['items'][0]['album']['name']
    results_artist = results['tracks']['items'][0]['artists'][0]['name']
    # then if this results title matches our song name and the artist matches our artist, find the audio features and add them (by spotify uri id for song)
    i = 0
    if (results_artist == artist_name) & (results_title == song_name):
        uri = results['tracks']['items'][0]['id']
        # these are audio features!! like danceability, energy, key, loudness..
        # stored in an array of length 1 containing a dictionary (key = audio feature, value = value of that feature)
        features = sp.audio_features(uri)
        result_string = f'TOP RESULT: {results_title} from {results_album} by {results_artist}. URI: {uri}'
        return_val = {'danceability': features[0]['danceability'], 'energy': features[0]['energy'], 'key' : features[0]['energy'],
                      'loudness': features[0]['loudness'], 'mode': features[0]['mode'], 'speechiness': features[0]['speechiness'],
                      'acousticness': features[0]['acousticness'], 'instrumentalness': features[0]['instrumentalness'],
                      'liveness': features[0]['liveness'], 'valence': features[0]['valence'], 'tempo': features[0]['tempo'],
                      'duration_ms': features[0]['duration_ms']}
        print(return_val)
        print(features[0])
        return result_string
    result_string = f'the search for {song_name} by {artist_name} was not found'
    return result_string


# function to scrape billboard site given artist name
def web_scrape_bb(artist_name):
    # convert artist name to - if spaces
    artist_name = artist_name.lower()
    artist_name = artist_name.replace(' ', '-')
    base = 'https://www.billboard.com/artist/'
    url = base + artist_name
    # need to add in try/excepts for if the artist is too obscure to have a billboard page
    page = requests.get(url)
    if page.reason == "Not Found":
        return 0
    else:
        soup = BeautifulSoup(page.content, "html.parser")
        top_100 = soup.find_all("div", class_ ="artist-chart-history-sticky-wrapper lrv-u-position-relative")
        #print(top_100[0].text.strip())
        text = top_100[0].text.strip('\n').strip('\t').strip().split('\t')[0]
        #print(text)
        if text == "Billboard Hot 100™":
            results = soup.find_all("span",
                                    class_="c-span a-font-primary-bold u-font-size-34 u-line-height-120 u-letter-spacing-0063 artist-stat-3")
            if len(results) < 1:
                return 0
                # print(results[0].text)
            hits = int(results[0].text.strip())

            # NOTE: currently coded to write flag or has or has not charted by artist not song
            if hits > 1:
                return 1
        return 0



def billboard_songs(artist_name, song_name):
    # convert artist name to - if spaces
    artist_name = artist_name.lower()
    artist_name = artist_name.replace(' ', '-')
    base = 'https://www.billboard.com/artist/'
    url = base + artist_name
    # need to add in try/excepts for if the artist is too obscure to have a billboard page
    page = requests.get(url)
    if page.reason == "Not Found":
        return 0
    else:
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("span",
                                class_="c-span a-font-primary-bold u-font-size-34 u-line-height-120 u-letter-spacing-0063 artist-stat-3")
        if len(results) < 1:
            return 0
            # print(results[0].text)
        hits = int(results[0].text.strip())
        if hits > 1:
            url = url + "/chart-history/hsi"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            songs = soup.find_all("div", class_ ="o-chart-results-list__item // lrv-u-flex lrv-u-flex-direction-column lrv-u-flex-grow-1 lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-lr-2 lrv-u-padding-lr-1@mobile-max lrv-u-padding-tb-050@mobile-max")
            billboard_songs = []
            for i in range(hits):
                song = songs[i].text.strip('\n')
                song = song.strip('\t')
                song = song.strip()
                song = song.split('\t')[0]
                if song_name == song:
                    print('billboard song!')
                #print(song)
                billboard_songs.append(song)
            #print(billboard_songs)
            return 1
        return 0

main()

