import requests
import time


from bs4 import BeautifulSoup
date=input("Enter the Date at which You want the Songs For(keep Format as yyyy-mm-dd):")
response=requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")

data=response.text
soup=BeautifulSoup(data,"html.parser")
songs=soup.select("li h3")
spec=soup.find_all(name="h3", class_="c-title")
# print(spec)
answer=[spec.getText().replace('\n', '').replace('\t', '').strip() for spec in songs if spec.getText().strip() != '']
print(answer)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://exampleforme.com/callback",
        client_id="",
        client_secret="",
        show_dialog=True,
        cache_path=".cache",
        username="",
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]

for song in answer:
    try:
        result = sp.search(q=f"{song} {year}", type="track", limit=1)
        uri = result["tracks"]["items"][0]["uri"]
        if song=="Account":
            break
        else:
            song_uris.append(uri)
        print(f"✅ Found: {song}")
    except IndexError:
        print(f"❌ Not found: {song}")
    time.sleep(0.2)

print(f"\n🎧 Total songs found on Spotify: {len(song_uris)}")

# Playlist creation
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
playlist_id = playlist["id"]

print("✅ Playlist created and populated successfully!")
