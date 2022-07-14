import matplotlib.pyplot as plt
import pandas as pd
import spotipy
from sklearn import decomposition

np.random.seed(42)

# import the songs, project only some of the features.
songs_ori = pd.read_pickle("liked_songs_2022-07-08.pkl")
features = ["af_danceability", "af_energy","af_loudness","af_speechiness",
            "af_acousticness","af_mode","af_instrumentalness","af_liveness","af_valence"]
songs = songs_ori.loc[:,features]


# normalize loudness
songs["af_loudness"] = -songs["af_loudness"]
songs["af_loudness"] = [round((i - min(songs["af_loudness"])) / (max(songs["af_loudness"])
                            - min(songs["af_loudness"])), 3) for i in songs["af_loudness"]]


#do a PCA
pca = decomposition.PCA(n_components=2)
pca.fit(songs)
songs_PCA = pca.transform(songs)
print("PCA metrics")
print(pca.explained_variance_ratio_)
print(pca.singular_values_)
print(pca.components_)


#cluster the songs
from sklearn.cluster import KMeans
kmeans_model = KMeans(n_clusters=8, random_state=1).fit(songs)
labels = kmeans_model.labels_

#plot the songs with their labels in a PCA
plt.scatter(songs_PCA[:,0], songs_PCA[:,1], alpha = 0.3, c=labels)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()


#add clusters to the df
songs_ori["cluster"] = labels
songs = songs.astype("float")
songs["cluster"] = labels

#summarize stats
summary_stats = songs.groupby(["cluster"]).mean()
summary_stats["cluster"] = summary_stats.index
print(summary_stats.to_string())

#radar chart
import numpy as np
def make_spider(row, title, color):
    # number of variable
    categories = [word[3:].capitalize() for word in features]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(1, 1, 1, polar=True, )

    # If you want the first axis to be on top:
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75], ["0.25", "0.5", "0.75"], color="grey", size=7)
    plt.ylim(0, 1)

    # Ind1
    values = summary_stats.loc[row].drop('cluster').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=0.4)

    # Add a title
    plt.title(title, size=11, color=color)


# ------- PART 2: Apply the function to all individuals
# initialize the figure
my_dpi = 96


# Create a color palette:
my_palette = plt.cm.get_cmap("Set2", len(summary_stats.index))

# Loop to plot
import io
import base64

buffer_dict = {}
for row in range(0, len(summary_stats.index)):
    plt.figure(figsize=(400 / my_dpi, 400 / my_dpi), dpi=my_dpi)
    make_spider(row=row, title='Clusterlist.V0 - ' + str(row), color=my_palette(row))

    buffer_dict[row] = io.BytesIO()
    plt.savefig(buffer_dict[row])


#connect spotipy and get user id
from spotipy.oauth2 import SpotifyOAuth
scope = "playlist-modify-public,ugc-image-upload"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user = spotify.current_user()["id"]

#create new playlists
for cluster in range(0,8):
    spotify.user_playlist_create(user, name = "Clusterlist.V0 - {}".format(cluster),
                                 description = "A playlist created through Kmeans clustering")

#get all playlists
playlist_results = spotify.current_user_playlists()
playlists = playlist_results['items']
while playlist_results['next']:
    playlist_results = spotify.next(playlist_results)
    playlists.extend(playlist_results['items'])

#get the newly created playlists
new_playlist_ids = [pl["id"] for pl in playlists if pl["name"][0:14] == "Clusterlist.V0"]


#convert the clusters to playlists
for cluster, playlist_id in zip(range(0,8), new_playlist_ids):
    songs_to_add = songs_ori.loc[songs_ori["cluster"] == cluster].index
    i = 0
    length = len(songs_to_add)
    while i <= length:
        end = i+100
        spotify.playlist_add_items(playlist_id, songs_to_add[i:end])
        i = end

    b64 = base64.b64encode(buffer_dict[cluster].getvalue())

    spotify.playlist_upload_cover_image(playlist_id, b64)
