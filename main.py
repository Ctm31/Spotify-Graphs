import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import numpy as np

# setup creditials for spotify app
client_credentials_manager = SpotifyClientCredentials(client_id='id', client_secret='secret')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_user_playlist(user='lovethecat123456789', p_num=9):
    # getting example user and playlist
    playlists = sp.user_playlists(user)
    tracks = sp.playlist_tracks(playlists['items'][p_num]['id'])

    # getting just the tracklist of playlist
    tracks = tracks['items']
    features = {}

    # features dict is key name and feature value
    for track in tracks:
        name = track['track']['name']
        feature = sp.audio_features(track['track']['id'])
        features[name] = feature
    
    user_feature = input("What feature would you like to see the results of? Options: 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'tempo', 'valence' (high is postive/happy, low is negative/sad). Enter feature here: ")

    # for each playlist track, get the selected feature and append to list
    feature_list = []
    name_list = []
    for name in features:
        name_list.append(name)
        feature_list.append(features[name][0][user_feature])

    return user_feature, feature_list, name_list, features

def get_artist():
    # get artist name from user input
    query = input("Enter the artist name: ")
    results = sp.search(q=query, type='artist')

    id = results['artists']['items'][0]['id']
    urn = 'spotify:artist:' + id

    # get artist top tracks
    artist_tracks = sp.artist_top_tracks(urn)

    feature_list = []
    name_list = []

    feature = input("What audio feature do you want to see? Options: 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'tempo', 'valence' (high is postive/happy, low is negative/sad). Enter feature here: ")

    # for each top track (10), get the selected feature and append to list
    for x in range(10):
        track_id = artist_tracks['tracks'][x]['id']
        name_list.append(artist_tracks['tracks'][x]['name'])
        features = sp.audio_features(track_id)
        feature_list.append(features[0][feature])

    return feature, feature_list, name_list

def get_quartiles(feature_list):
    lower = np.quantile(feature_list, 0.25)
    mid = np.quantile(feature_list, 0.5)
    upper = np.quantile(feature_list, 0.75)
    print(lower)
    print(mid)
    print(upper)

def grapher(feature_list, name_list, user_feature, features=[1]*10):
    # x-coordinates of left sides of bars 
    left = [x for x in range(len(features))]
        
    # heights of bars
    height = feature_list
        
    # labels for bars
    tick_label = name_list
        
        # plotting a bar chart
    plt.bar(left, height, width = 0.8, color = ['lightgreen', 'darkgreen'])

    plt.xticks(left, tick_label, rotation = 45)
        
        # naming the x-axis
    plt.xlabel('tracks')
        # naming the y-axis
    plt.ylabel(user_feature)
        # plot title
    plt.title('playlist songs vs. ' + user_feature)

        # function to show the plot
    plt.show()

run_type = input("Artist ('A') or playlist ('P')? ")
if run_type == 'A':
    feature, feature_list, name_list = get_artist()
    grapher(feature_list, name_list, feature)
elif run_type == 'P':
    feature, feature_list, name_list, features = get_user_playlist()
    grapher(feature_list, name_list, feature, features)
else:
    print("Hey! You didn't type the right thing :(")

get_quartiles(feature_list)
