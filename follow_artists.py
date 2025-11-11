import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys

# --- Your credentials ---
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

# --- The permissions your script needs ---
# 1. To read user's private playlists
# 2. To modify who the user follows
SCOPES = "playlist-read-private user-follow-modify"

def get_spotify_client():
    """Handles authentication and returns a Spotify client."""
    print("Connecting to Spotify...")
    
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPES,
        cache_path=".spotifycache"  # Caches the token
    )
    
    # This will automatically open a browser for you to log in
    # and grant permission the first time you run it.
    try:
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # Test the connection
        user = sp.current_user()
        print(f"Authenticated as: {user['display_name']} (ID: {user['id']})")
        return sp, user['id']
        
    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"Error authenticating: {e}")
        print("Please check your CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI.")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to connect. Is Spotipy installed? Error: {e}")
        sys.exit(1)

def get_all_artists_from_playlists(sp, user_id):
    """Fetches all playlists and extracts unique artist IDs."""
    
    print("Finding all your artists from all your playlists...")
    print("This may take a while if you have many playlists...")
    
    all_artist_ids = set()
    
    # 1. Get all playlists
    playlists = sp.user_playlists(user=user_id)
    
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(f"  -> Processing playlist: {playlist['name']}")
            
            # 2. Get all tracks from each playlist
            try:
                tracks = sp.playlist_tracks(playlist['id'])
                while tracks:
                    for item in tracks['items']:
                        if item['track']:
                            # 3. Get all artists from each track
                            for artist in item['track']['artists']:
                                all_artist_ids.add(artist['id'])
                    
                    # Check for more pages of tracks
                    tracks = sp.next(tracks) if tracks['next'] else None
            except Exception as e:
                print(f"    Error processing playlist {playlist['name']}: {e}")
                
        # Check for more pages of playlists
        playlists = sp.next(playlists) if playlists['next'] else None
        
    print(f"\nFound {len(all_artist_ids)} unique artists.")
    return list(all_artist_ids)

def follow_artists(sp, artist_ids):
    """Follows all artists in the list, in batches of 50."""
    
    if not artist_ids:
        print("No new artists to follow.")
        return

    print("Following artists...")
    
    # The API only allows following 50 artists at a time
    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i:i+50]
        try:
            sp.user_follow_artists(ids=batch)
            print(f"  -> Followed batch {i//50 + 1}")
        except Exception as e:
            print(f"  -> Error following batch: {e}")
            
    print("\nProcess complete! All artists have been followed.")

# --- Main script ---
if __name__ == "__main__":
    sp, user_id = get_spotify_client()
    
    if sp and user_id:
        artist_ids = get_all_artists_from_playlists(sp, user_id)
        
        if artist_ids:
            follow_artists(sp, artist_ids)
        else:
            print("Could not find any artists in your playlists.")