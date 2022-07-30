import sys
import spotify_playlist_mover
import webbrowser
import time


def main():
	spotify_logout()
	old_account_dl= spotify_playlist_mover.download_from_origin()
	spotify_logout()
	spotify_playlist_mover.upload_to_destination(old_account_dl)
	print("Done!")

def spotify_logout():
	webbrowser.open('accounts.spotify.com/logout')	# logout from old account
	time.sleep(3)

if __name__ == '__main__':
	sys.exit(main())