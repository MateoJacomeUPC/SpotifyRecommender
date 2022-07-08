import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = spotify.current_user_saved_tracks()

tracks = results['items']
while results['next']:
    results = spotify.next(results)
    tracks.extend(results['items'])

liked_songs_uris = []
liked_songs_df = pd.DataFrame(columns=["track_name", "added_date",
                                       "track_release_date", "track_popularity",
                                       "af_danceability", "af_energy", "af_key",
                                       "af_loudness", "af_mode", "af_speechiness",
                                       "af_acousticness", "af_instrumentalness",
                                       "af_liveness", "af_valence", "af_tempo", "af_type",
                                       "af_duration", "af_time_signature", "main_artist_uri",
                                       "main_artist_name", "main_artist_followers",
                                       "main_artist_genres", "main_artist_popularity"])
# for idx, item in enumerate(tracks):
#     track = item['track']
#     track_uri = track["uri"]
#
#     liked_songs_uris.append(track_uri)
#
#     liked_songs_df.loc[track_uri, "added_date"] = item["added_at"]
#     liked_songs_df.loc[track_uri, "track_name"] = track["name"]
#     liked_songs_df.loc[track_uri, "track_release_date"] = track["album"]["release_date"]
#     liked_songs_df.loc[track_uri, "track_popularity"] = track["popularity"]
#
#     audio_features = spotify.audio_features([track_uri])[0] #function requires a list
#
#     liked_songs_df.loc[track_uri, "af_danceability"] = audio_features["danceability"]
#     liked_songs_df.loc[track_uri, "af_energy"] = audio_features["energy"]
#     liked_songs_df.loc[track_uri, "af_key"] = audio_features["key"]
#     liked_songs_df.loc[track_uri, "af_loudness"] = audio_features["loudness"]
#     liked_songs_df.loc[track_uri, "af_mode"] = audio_features["mode"]
#     liked_songs_df.loc[track_uri, "af_speechiness"] = audio_features["speechiness"]
#     liked_songs_df.loc[track_uri, "af_acousticness"] = audio_features["acousticness"]
#     liked_songs_df.loc[track_uri, "af_instrumentalness"] = audio_features["instrumentalness"]
#     liked_songs_df.loc[track_uri, "af_liveness"] = audio_features["liveness"]
#     liked_songs_df.loc[track_uri, "af_valence"] = audio_features["valence"]
#     liked_songs_df.loc[track_uri, "af_tempo"] = audio_features["tempo"]
#     liked_songs_df.loc[track_uri, "af_type"] = audio_features["type"]
#     liked_songs_df.loc[track_uri, "af_duration"] = audio_features["duration_ms"]
#     liked_songs_df.loc[track_uri, "af_time_signature"] = audio_features["time_signature"]
#
#     main_artist_uri = track["artists"][0]["uri"]
#     liked_songs_df.loc[track_uri, "main_artist_uri"] = main_artist_uri
#     main_artist = spotify.artist(main_artist_uri)
#     liked_songs_df.loc[track_uri, "main_artist_name"] = main_artist["name"]
#     liked_songs_df.loc[track_uri, "main_artist_followers"] = main_artist["followers"]["total"]
#     liked_songs_df.loc[track_uri, "main_artist_genres"] = main_artist["genres"]
#     liked_songs_df.loc[track_uri, "main_artist_popularity"] = main_artist["popularity"]
#
#     print(idx, track["name"])
#
# liked_songs_df.to_pickle("liked_songs.pkl")

liked_songs_df = pd.read_pickle("liked_songs_2022-07-08.pkl")

print(liked_songs_df.to_string())



