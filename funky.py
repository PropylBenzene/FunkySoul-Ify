import pprint
import sys
import requests
import lxml
import bs4
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import simplejson as json

username = ''
client_id = ''
client_secret = ''
redirect_uri = ''
scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
URL = "https://www.allmusic.com/newreleases"
playlist_id = ''

artists = []
titles = []
combined = {}
new_releases = []
X = 0
album_uri = []
tracks_uri = []

r = requests.get(URL,headers=headers)

soup = BeautifulSoup(r.content, 'lxml')

table = soup.find('div', attrs = {'class':'new-release-items-container'})

#Assemble all the Artists
for row in table.findAll('div', attrs = {'class':'artist'}):
   artist = ""
   artist = row.a.text
   artists.append(artist)

#Assemble all the Album Titles   
for row in table.findAll('div', attrs = {'class':'title'}):
   title = ""
   title = row.a.text
   titles.append(title)
   

#How many in this batch?
print(len(artists))   

#Create a list as 'Artist, Album Title' in the variable new_releases
while X < len(artists):
   combined = {}
   combined = (artists[X], titles[X])
   new_releases.append(combined)
   X += 1

#Show the compiled list of newly released albums.
#print(new_releases)

yodel = ""
x = 0
total_tracks = []

#Generates the album_uri's.
while x < len(new_releases):
   yodel = new_releases[x][0] + ", " + new_releases[x][1]
   cray, zee, daze = yodel.partition('/')
   print(cray)
   print(yodel)
   if token:
      sp = spotipy.Spotify(auth=token)
      result = sp.search(q = cray, type = "album")
#      pprint.pprint(result)
      try:
         album_uri.append(result['albums']['items'][0]['uri'])
         total_tracks.append(result['albums']['items'][0]['total_tracks'])
         x += 1
      except:
         x += 1
         pass         
   else:
      print("Can't get token for", username)

print(album_uri)      
print(total_tracks)

#for x in result['albums']['items'][0]['uri']:
#   print(x)


#Grab track URI's.

x = 0
y = 1
while x < len(album_uri):
   tracks = sp.album_tracks(album_uri[x])
   while y < total_tracks[x]:
      tracks_uri.append(tracks['items'][y]['uri'])
      print(tracks_uri)
      y += 1
   x += 1
   y = 1

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    nun = 0
    while nun <= len(tracks_uri):
       results = sp.user_playlist_add_tracks(username, playlist_id, tracks_uri[:100])
       print(results)
       del tracks_uri[0:100]       
