import sys, requests
from bs4 import BeautifulSoup
import json

def currentSong():
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    payload = {}
    headers = { 'Authorization': 'YOUR SPOTIFY OAUTH TOKEN'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    respnoseJson = response.json()
    artistName = respnoseJson['item']['artists'][0]['name']
    songName = respnoseJson['item']['name']

    return {'artist': artistName, 'title': songName}

def Searchgenius(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'YOUR GENIUS TOKEN'}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def removeSongUrl(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

def main():
    
    #Get the song we trying to find lyrics for
    args_length = len(sys.argv)
    if args_length == 1:
        # Show lyrics for what user is playing on Spotify
        current_song = currentSong()
        artist_name = current_song['artist']
        song_title = current_song['title']
    elif args_length == 3:
        # Use input as song title and artist name
        song_info = sys.argv
        artist_name, song_title = song_info[1], song_info[2]
    else:
        print('Wrong number of arguments.\n' \
                       'Use two parameters to perform a custom search ' \
                       'or none to get the song currently playing on Spotify.')
        return

    print('{} by {}'.format(song_title, artist_name))

    # Search for matches in request response
    response = Searchgenius(song_title[:30], artist_name)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break

    # Extract lyrics from URL if song was found
    if remote_song_info:
        song_url = remote_song_info['result']['url']
        lyrics = removeSongUrl(song_url)
        print(lyrics)
    else:
        print('Error 404: No lyrics found')

if __name__ == '__main__':
    main()
