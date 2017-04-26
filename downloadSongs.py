##download files from soundflush.com
try:
    import urllib.request as urllib2
except:
    import urllib2
import bs4
from bs4 import BeautifulSoup
import requests
import os

NUM_OF_RESULTS = 5
DOWNLOAD_DIR = "D:\\Acads\\Python\\Music\\"

LOG_LEVELS = {
    "DEBUG" : 100,
    "INFO" : 200,
    "ERROR" : 300,
    "NONE" : 400
}
LOGLVL=LOG_LEVELS["INFO"]

def log_error(exception, location):
    if(LOGLVL <= LOG_LEVELS["ERROR"]):
        print("Exception encountered : " + str(type(exception)) + " in " + location)
        print("Exception : " + str(exception))

def log_info(string):
    if(LOGLVL <= LOG_LEVELS["INFO"]):
        print(string)

def log_debug(string):
    if(LOGLVL <= LOG_LEVELS["DEBUG"]):
        print(string)
        
def download(track_url):
    payload = {"track_url": track_url, "btn_download": "Download"}
    response = requests.post("http://soundflush.com/", data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    url = soup.find_all(class_="button button--save")[0]['href']
    filename = soup.find_all(class_="button button--save")[0]['download']
    if os.path.isfile(DOWNLOAD_DIR + filename):
        log_info("File is already present. Skipping :" + track_url)
        return
    log_debug("Downloading : " + filename)
    try:
        f = urllib2.urlopen(url)
        data = f.read()
        with open(DOWNLOAD_DIR + filename, "wb") as code:
            code.write(data)
    except Exception as e:
        log_debug("Error while trying to download : " + track_url + " with soundflush. Trying 9soundclouddownloader instead.")
        payload = {"csrfmiddlewaretoken": "Ewuhk9o5KKnzkxVAdvukOQy85pTYZVZK", "sound-url": "https://soundcloud.com/haydenjamesartist/beginnings"}
        headers = {'Cookie': 'csrftoken=Ewuhk9o5KKnzkxVAdvukOQy85pTYZVZK; _ga=GA1.2.1686624080.1493168131'}
        response = requests.post("http://9soundclouddownloader.com/download-sound-track", data=payload, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        url = soup.select("center a")[0]['href']
        filename = track_url.split("/")[len(track_url.split("/")) - 1].replace("\n", "") + ".mp3"
        if os.path.isfile(DOWNLOAD_DIR + filename):
            log_info("File is already present. Skipping :" + track_url)
            return
        log_debug("Downloading : " + filename)
        try:
            f = urllib2.urlopen(url)
            data = f.read()
            with open(DOWNLOAD_DIR + filename, "wb") as code:
                code.write(data)
        except Exception as e:
            log_error(e, "Error while trying to download " + track_url)
    

f = open('D:\\Acads\\Python\\soundcloud-search-texts.txt', 'r')
for line in f:
    query = '+'.join(line.split(' '))
    request = "https://soundcloud.com/search/sounds?q=" + query
    log_debug("Searching SoundCloud for " + line)
    req = urllib2.Request(request, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read(), "html.parser")
    anchors = soup.select("h2 a")
    for i in range(0, NUM_OF_RESULTS+1):
        try:
            track_url = "https://soundcloud.com" + anchors[i]['href']
            download(track_url)
        except Exception as e:
            log_error(e, "Error while trying to access : " + str(i) + " of ")
            log_error(e, anchors)
    response.close()
f.close()

f = open('D:\\Acads\\Python\\soundcloud-search-urls.txt', 'r')
for line in f:
    try:
        log_debug("Downloading : " + line)
        download(line)
    except Exception as e:
        log_error(e, "Error while trying to download : " + line)
f.close()
