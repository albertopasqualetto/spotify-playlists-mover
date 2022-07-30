# TODO track add number limit?

import spotipy
from spotipy.oauth2 import SpotifyImplicitGrant
import base64
import requests
# from pprint import pprint



def download_from_origin():
	print("Login to Origin account")
	sp_from= spotipy.Spotify(auth_manager=SpotifyImplicitGrant(client_id="f22a36cd6eed407f88ce13a771388461", redirect_uri="http://localhost/", scope="user-library-read"))
	print(sp_from.me()['id'])

	# Playlists
	print("Downloading playlists...")
	result= sp_from.current_user_playlists()	# dict output -> list playlists -> dict playlist
	playlists= result['items']
	while result['next']:	# pages after first
		result= sp_from.next(result)
		playlists.extend(result['items'])
	# print(playlists[0]['id'])
	# pprint(playlists)

	for playlist in playlists:
		# playlist dictionary playlist:[trackList]
		result= sp_from.playlist_tracks(playlist)
		playlist_tracks= result['items']
		while result['next']:
			result= sp_from.next(result)
			playlist_tracks.extend(result['items'])
		track_list= []
		for track in playlist_tracks:
			track_list.append(track['track']['uri'])
		playlist['trackList']= track_list


	# Saved tracks
	print("Downloading saved tracks...")
	result= sp_from.current_user_saved_tracks()
	saved_tracks= result['items']
	while result['next']:
		result= sp_from.next(result)
		saved_tracks.extend(result['items'])
	saved_tracks_list= []
	for saved_track in saved_tracks:
		saved_tracks_list.append(saved_track['track']['id'])

	return (playlists, saved_tracks_list)	# return tuple of playlists and saved tracks


def upload_to_destination(playlists_dict_and_saved_tracks_list_tuple):
	playlists_dict= playlists_dict_and_saved_tracks_list_tuple[0]
	saved_tracks_list= playlists_dict_and_saved_tracks_list_tuple[1]

	print("Log in to Destination account")
	sp_to= spotipy.Spotify(auth_manager=SpotifyImplicitGrant(client_id="f22a36cd6eed407f88ce13a771388461", redirect_uri="http://localhost/", scope="playlist-modify-public playlist-modify-private ugc-image-upload user-library-modify"))
	print(sp_to.me()['id'])

	# Playlists
	print("Uploading playlists...")
	for playlist in playlists_dict:
		# Create playlist
		new_playlist= sp_to.user_playlist_create(sp_to.me()['id'], playlist['name'], public= playlist['public'], collaborative= playlist['collaborative'], description= playlist['description'])

		# Set thumbnail
		thumbnail_b64= base64.b64encode(requests.get(playlist['images'][0]['url']).content)
		""" File "C:\Users\alber\Desktop\SpotifyPlaylistsMover\spotifyplaylistmover.py", line 68, in upload_to_destination
    thumbnail_b64= base64.b64encode(requests.get(playlist['images'][0]['url']).content)
IndexError: list index out of range """
		sp_to.playlist_upload_cover_image(new_playlist['id'], thumbnail_b64)

		# Set tracks
		sp_to.playlist_add_item(new_playlist['id'], playlist['trackList'])


	# Saved tracks
	print("Uploading saved tracks...")
	sp_to.current_user_saved_tracks_add(saved_tracks_list)