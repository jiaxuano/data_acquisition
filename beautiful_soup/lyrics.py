import sys
from bs4 import BeautifulSoup
import requests
import argparse
import numpy as np
import re


def get_content_soup_from_url(url):
    result = requests.get(url)
    content = result.text
    return BeautifulSoup(content, "lxml")


def clean_text(text):
    """Given a string of text return clean text
    Clean issues with text
    "1. Hola" --> "Hola" 
    "Hola." --> "Hola" 
    "Hola (L)" --> "Hola"
    "Hola (1790)"  --> "Hola"
    "Hola 1790"  --> "Hola"
    """
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"[0-9]", "", text)
    text = text.replace(".", "")
    return text.strip()


def process_row(row):
    """ Inputs a row of a table and returns the song, album and url

    The input should follow this format:
        <tr valign="bottom">
        <td align="left">
        Ain't No Cure For Love </td>
        <td align="left">
        <a href="album9.html" style="text-decoration:none">I'm Your Man (L)</a> </td>
        </tr>
    Ouputs: three strings, as shown in the example
        "Ain't No Cure For Love", "I'm Your Man", "album9.html"

    To ensure cleanliness and avoid duplicates, the following actions are performed:
      -- remove "(L)"
      -- remove years
    from album names and song names
    """
    # soup = BeautifulSoup(row, "lxml")
    song_text = clean_text(row.find('td', {'align':'left'}).text)
    album_text = clean_text(row.find('a').text)
    html_text = row.find('a', href = True)['href']
    return song_text,album_text,html_text


def get_albums():
    """ Scrape album names from 
    "https://www.leonardcohenfiles.com/songind.html"

    Return a list of unique names in alfabetical order
    To ensure cleanliness and avoid duplicates, the following actions are performed:
      -- remove "(L)"
      -- remove years
    """
    url = "https://www.leonardcohenfiles.com/songind.html"
    soup2 = get_content_soup_from_url(url)
    a = soup2.find_all('a', {'style':'text-decoration:none'})
    albums = a[1:-5]
    albums_set = set()
    for i in range(len(albums)):
        albums_set.add(clean_text(albums[i].text))
    return sorted(list(albums_set))

def get_songs():
    """ Scrape song urls from
    "https://www.leonardcohenfiles.com/songind.html"

    Return a list of unique names in alfabetical order
    Some cleaning to avoid duplicates:
      -- remove "(L)"
    """
    url = "https://www.leonardcohenfiles.com/songind.html"
    soup2 = get_content_soup_from_url(url)
    tables = soup2.find_all('table')
    trs = tables[1].find_all('tr')
    set_songs = set()
    list_songs = list()
    for i in range(len(trs)):
        row = process_row(trs[i])
        if clean_text(row[0]) not in set_songs:
            set_songs.add(clean_text(row[0]))
            list_songs.append(clean_text(row[0]))
    return sorted(list_songs)

def scrape_lyrics_from_url(song, url):
    """ Given a song and a url return the lyric of the song
    
    Inputs:
       song: string example: "Bird on the Wire"
       url: 'https://www.leonardcohenfiles.com/album2.html'
    
    Return the text of the lyrics:

    Like a bird on the wire,
    like a drunk in a midnight choir
    I have tried in my way to be free.
    Like a worm on a hook, 
    ...
    """
    soup3 = get_content_soup_from_url(url)
    block = soup3.find_all('blockquote')
    songs = soup3.find_all('a',{'style':'text-decoration:none'})
    song_names = [songs[i].text.strip() for i in range(len(songs))]
    index = 0
    for i in range(len(song_names)):
        if song_names[i] == song:
            index = i
    lyrics = block[index].text
    lyrics = lyrics.replace('\r',' ').strip('').strip('\n')
#     lyrics = lyrics.replace('\n',' ')
    return lyrics



def get_lyrics(s):
    """ Given an input song scrape and return the lyric
    """
    url = "https://www.leonardcohenfiles.com/songind.html"
    soup = get_content_soup_from_url(url)
    tables = soup.find_all('table')
    trs = tables[1].find_all('tr')
    for tr in trs:
        row = process_row(tr)
        if clean_text(row[0].lower())==clean_text(s.lower()):
            link = 'https://www.leonardcohenfiles.com/'+row[2]
    lyrics = scrape_lyrics_from_url(s, link)
    return lyrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="Generates a list of songs", action='store_true')
    parser.add_argument("-a", help="Generates a list of albums", action='store_true')
    parser.add_argument("-l", help="Print lyrics for a given song", type=str)
    args = parser.parse_args()
    if args.s:
        songs = get_songs()
        for song in songs:
            print(song)
    if args.a:
        albums = get_albums()
        for a in albums:
            print(a)
    if args.l:
        lyric = get_lyrics(args.l)
        if lyric is None:
            print("No lyric was found")
        else:
            print(lyric)
