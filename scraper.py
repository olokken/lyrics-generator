import re

import lyricsgenius


class Scraper:
    def __init__(self, artist_name):
        self.artist_name = artist_name

    def scrape(self, max_songs=15):
        genius = lyricsgenius.Genius('l8-nnpE9RfPvXrIpXq1zhiO1SOdcwCD5m3sOUw9rZlrtWRY1f-9K4wD5tdWK2xN6')
        genius.timeout = 15
        artist = genius.search_artist(self.artist_name, max_songs=max_songs, sort='popularity')
        print(artist)
        songs = []
        for song in artist.songs:
            songs.append(self.preprocess(song.lyrics))
        return songs

    def preprocess(self, lyrics):
            song_lyrics = re.sub(r'\[.*?\]', '', lyrics) #Remove bracket words like [Verse 1]
            song_lyrics = re.sub(r'\d+$', '', song_lyrics) #Remove trailing digits at the end of a string
            song_lyrics = re.sub(r'^.*Contributor.*\n?', '', song_lyrics) #Remove Contributor lines
            song_lyrics = str(song_lyrics).lstrip().rstrip() #Remove leading or trailing whitespace
            song_lyrics = str(song_lyrics).replace("\n\n", "\n")
            song_lyrics = re.sub(' +', ' ', song_lyrics)
            song_lyrics = str(song_lyrics).replace('"', "")
            song_lyrics = str(song_lyrics).replace("'", "")
            song_lyrics = str(song_lyrics).replace("*", "")
            song_lyrics = song_lyrics.replace('You might also like', '')
            return song_lyrics
    
    def scrape_and_save(self, max_songs=15):
        songs = self.scrape(max_songs)
        with open(f'data/{self.artist_name}.txt', 'w') as file:
            for string in songs:
                file.write(string + '\n')
        return songs