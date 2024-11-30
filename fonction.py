import csv,os,shutil
import re
import ssl
from pytube import YouTube,Playlist
from pytube import request
from pytube import extract
from pytube.innertube import _default_clients
from pytube.exceptions import RegexMatchError

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID"]

import pytube, re
def patched_get_throttling_function_name(js: str) -> str:
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

ssl._create_default_https_context = ssl._create_unverified_context
pytube.cipher.get_throttling_function_name = patched_get_throttling_function_name

#variable

class Music:
    def __init__(self,filename,name,author,album):
        self.filename=filename
        self.name=name
        self.author=author
        self.album=album
    def __repr__(self):
        return f"{self.name} by {self.author}"

music_queue=[]


# remvoe emoji from str
def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", re.UNICODE)
    return re.sub(emoj, '', data).replace(',','').replace(u'\u200b', ' ')

# check if a music is download
def Is_File_Download(file_name):
    if file_name in os.listdir("music/Song"):
        return True
    else:
        return False
        
# Download youtube video with a link
def download_yt(link):
    file_name=f"{link[-11:]}.mp3"

    if Is_File_Download(file_name):
        album_song=read_album_bdd("Song")
        i=0
        #tant que la music n'est pas trouvé
        while i < len(album_song) and album_song[i]["filename"]!=file_name:
            i+=1
        v=album_song[i]
        m=Music(file_name,v["name"],"Youtube","Song")
        return m
    #youtube download
    else:
        ytb = YouTube(link).streams.filter(only_audio=True)
        ytb[0].download(filename=f"music/Song/{file_name}")

        print(f"file_name {file_name} \n titre: {remove_emojis(ytb[0].title)}")
        add_bdd(file_name,remove_emojis(ytb[0].title),"Youtube")

        m=Music(file_name,remove_emojis(ytb[0].title),"Youtube","Song")
        return m

# play album 
#return true if the album exist, false if it doesn't
def play_album(album_name):
    if album_name in os.listdir("music"):
        temp=read_album_bdd(album_name) # list of dict
        for music in temp:
            music_queue.append(Music(**music)) # pass value of dict as args
        return True
    else:
        return False


def clear_Song():
    folder = 'music/Song'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))



# csv

def add_bdd(filename,name,author):
    with open("bdd.csv", 'a', newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([filename,name,author,"Song"])



def read_album_bdd(album_name):
    with open("bdd.csv", 'r', newline='',encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        rows = [row for row in csv_reader if row["album"]==album_name]
    return rows


def clear_bdd(album):
    with open("bdd.csv", 'r', newline='', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        rows = [row for row in csv_reader if row["author"] != album]

    with open("bdd.csv", 'w', newline='', encoding="utf-8") as file:
        fieldnames = ["filename", "name", "author", "album"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
