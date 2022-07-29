import sys
import spotifyplaylistmover
import webbrowser
import time


def main():
	old_account_dl= spotifyplaylistmover.download_from_origin()
	webbrowser.open('accounts.spotify.com/logout')	# logout from old account
	time.sleep(3)
	spotifyplaylistmover.upload_to_destination(old_account_dl)
	print("Done!")


if __name__ == '__main__':
	sys.exit(main())