# spotify-follow-artists
A python script to follow all artists in your Spotify playlists

Requirements:
- A free developer account on Spotify
- Both Python and Spotipy installed on your computer

To use this script you will need to set up an account and create an app at the Spotify developers portal. To do this is very easy:

1. Go to https://developer.spotify.com/dashboard
2. Ckick "Log in"
3. Log in with your Spotify account
4. Click "Create app"
5. Complete the required fields on the form as follows:\
   App name: `Spotify-follow-artists`\
   App description: `Follows all artists in all your Spotify playlists`\
   Redirect URIs: `http://127.0.0.1:8888/callback`\
   Under "Which API/SDKs are you planning to use?" check Web API\
   Check "I agree"\
   Click Save
6. From the next screen you will need to copy the Client ID and Client sectret into the marked location at the start of the deduplicate.py file

You will need both Python and Spotipy installed on your computer.
The following instructions are for Mac, but should be similar for other platforms:

1. If you don't have Python, you can get it from https://www.python.org/.
2. Once Python is installed, open your Terminal and type:
   `pip install spotipy`
   Note: depending on your Python installation you may need to use `pip3 install spotipy` if the above command does not work
3. Navigate to the folder where you saved the follow_artists.py file. For example, if it's on your Desktop:
   `cd ~/Desktop`
4. Run the script:
   `python follow_artists.py`\
   Note: depending on your Python installation you may need to use `python3 follow_artists.py` if the above does not work
6. Watch your web browser. It will pop open with a Spotify login page. Log in and click "Agree" to give your own script permission.\
   The browser will then show a "Success" message. You can close the browser tab.
7. The script will handle the rest and let you know when it has completed.
