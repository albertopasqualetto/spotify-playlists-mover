import sys
import spotifyplaylistmover
import webbrowser
import time


def main():
	spotify_logout()
	old_account_dl= spotifyplaylistmover.download_from_origin()
	spotify_logout()
	spotifyplaylistmover.upload_to_destination(old_account_dl)
	print("Done!")

def spotify_logout():
	webbrowser.open('accounts.spotify.com/logout')	# logout from old account
	time.sleep(3)

if __name__ == '__main__':
	sys.exit(main())