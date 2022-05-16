# TODO track add number limit?

import spotipy
from spotipy.oauth2 import SpotifyImplicitGrant
import base64
import requests
# from pprint import pprint

print("Origin account")
spFrom= spotipy.Spotify(auth_manager=SpotifyImplicitGrant(client_id="86d6f354226d43b690e00e8594579a63", redirect_uri="http://localhost/"))
print("Destination account")
spTo= spotipy.Spotify(auth_manager=SpotifyImplicitGrant(client_id="86d6f354226d43b690e00e8594579a63", redirect_uri="http://localhost/", scope="playlist-modify-public playlist-modify-private ugc-image-upload"))

# print(spFrom.me())

# pprint(spFrom.current_user_playlists())

# Playlists
result= (spFrom.current_user_playlists())	# dict output -> list playlists -> dict playlist
playlists= result['items']
while result['next']:	# pages after first
	result= spFrom.next(result)
	playlists.extend(result['items'])
# print(playlists['items'][n]['id'])

for playlist in playlists:
	# Create playlist
	newPlaylist= spTo.user_playlist_create(spTo.me()['id'], playlist['name'], public= playlist['public'], collaborative= playlist['collaborative'], description= playlist['description'])

	# Set thumbnail
	thumbnail_b64= base64.b64encode(requests.get(playlist['images'][0]['url']).content)
	spTo.playlist_upload_cover_image(newPlaylist['id'], thumbnail_b64)

	# Set tracks
	result= spFrom.playlist_tracks(playlist)
	playlistTracks= result['items']
	while result['next']:
		result= spFrom.next(result)
		playlistTracks.extend(result['items'])
	trackList= []
	for track in playlistTracks:
		trackList.append(track['id'])
	spTo.playlist_add_item(newPlaylist['id'], trackList)
