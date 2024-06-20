import spotipy
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials

# setup creditials for spotify app
client_credentials_manager = SpotifyClientCredentials(client_id='d27549c5062d4f02838b372c31eb15bf', client_secret='b21dc57bb058493e863c3725dcf93062')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def artist_graph():
    # get artist name from user input
    query = input("Enter the artist name: ")
    results = sp.search(q=query, type='artist')

    id = results['artists']['items'][0]['id']
    urn = 'spotify:artist:' + id

    # get artist top tracks
    artist_tracks = sp.artist_top_tracks(urn)

    acoustic_list = []
    tracks = []

    feature = input("What audio feature do you want to see? Options: 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'tempo', 'valence' (high is postive/happy, low is negative/sad). Enter feature here: ")

    # for each top track (10), get the selected feature and append to list
    for x in range(10):
        track_id = artist_tracks['tracks'][x]['id']
        tracks.append(artist_tracks['tracks'][x]['name'][:9])
        features = sp.audio_features(track_id)
        acoustic_list.append(features[0][feature])
    
    # x-coordinates of left sides of bars 
    left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # heights of bars
    height = acoustic_list
    
    # labels for bars
    tick_label = tracks
    
    # plotting a bar chart
    plt.bar(left, height, tick_label = tick_label,
            width = 0.8, color = ['lightgreen', 'darkgreen'])
    
    # naming the x-axis
    plt.xlabel('tracks')
    # naming the y-axis
    plt.ylabel(feature)
    # plot title
    plt.title('Artist Songs vs. ' + feature)
    
    # function to show the plot
    plt.show()


artist_graph()