import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import numpy as np

# setup creditials for spotify app
client_credentials_manager = SpotifyClientCredentials(client_id='d27549c5062d4f02838b372c31eb15bf', client_secret='b21dc57bb058493e863c3725dcf93062')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# getting example user and playlist
playlists = sp.user_playlists('lovethecat123456789')
tracks = sp.playlist_tracks(playlists['items'][9]['id'])

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

lower = np.quantile(feature_list, 0.25)
mid = np.quantile(feature_list, 0.5)
upper = np.quantile(feature_list, 0.75)
print(lower)
print(mid)
print(upper)
    
# x-coordinates of left sides of bars 
left = [x for x in range(len(features))]
    
# heights of bars
height = feature_list
    
# labels for bars
tick_label = name_list
    
    # plotting a bar chart
plt.bar(left, height, width = 0.8, color = ['lightgreen', 'darkgreen'])

plt.xticks(left, tick_label, rotation = 'vertical')
    
    # naming the x-axis
plt.xlabel('tracks')
    # naming the y-axis
plt.ylabel(user_feature)
    # plot title
plt.title('playlist songs vs. ' + user_feature)

    # function to show the plot
plt.show()
