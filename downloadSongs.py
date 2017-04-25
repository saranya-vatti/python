##download files from soundflush.com
try:
    import urllib.request as urllib2
except:
    import urllib2
import bs4
from bs4 import BeautifulSoup
import requests

NUM_OF_RESULTS = 5
DOWNLOAD_DIR = "D:\\Acads\\Python\\Music\\"

LOG_LEVELS = {
    "DEBUG" : 100,
    "INFO" : 200,
    "ERROR" : 300,
    "NONE" : 400
}
LOGLVL=LOG_LEVELS["DEBUG"]

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
    log_debug("Downloading : " + filename)
    f = urllib2.urlopen(url)
    data = f.read()
    with open(DOWNLOAD_DIR + filename + ".mp3", "wb") as code:
        code.write(data)
    

f = open('D:\\Acads\\Python\\soundcloud-search-texts.txt', 'r')
for line in f:
    query = '+'.join(line.split(' '))
    request = "https://soundcloud.com/search/sounds?q=" + query
    log_debug("Searching SoundCloud for " + line)
    req = urllib2.Request(request, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read(), "html.parser")
    anchors = soup.select("h2 a")
    for i in range(0, NUM_OF_RESULTS):
        try:
            track_url = "https://soundcloud.com" + anchors[i]['href']
            log_debug("Downloading : " + track_url)
            download(track_url)
        except Exception as e:
            log_error(e, "Error while trying to access : " + str(i) + " of ")
            log_error(e, anchors)
    response.close()
