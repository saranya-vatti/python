##code to extract lyrics of songs and place them in a text file

##get a way to flag wrong lyrics and search for ??
##-the next search result next time the program is run
##-song name+artist
##-song name+album
##write an android app to insert link into the music player:
##-link to lyrics if present in local; else
##-link to google to search if net is connected; else
##-disabled link

try:
    import urllib.request as urllib2
except:
    import urllib2
import bs4
from bs4 import BeautifulSoup
import re
import json
import os
import time
import urllib
import shutil
from tinytag import TinyTag

#sourceDir = 'E:\\Music\\English'
sourceDir = 'D:\\Move\\tmp\\'
#destDir = 'E:\\Music\\Lyrics\\'
destDir = 'D:\\Move\\Lyrics\\'
lyricRepo = 'E:\\Music\\Lyrics\\'

LOG_LEVELS = {
    "DEBUG" : 100,
    "INFO" : 200,
    "ERROR" : 300,
    "NONE" : 400
}
LOGLVL=LOG_LEVELS["NONE"]
unabletoparse=[]

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
        
def parseFilename(filename):
    #check out id3 for recently downloaded files
    try:
        newfilename = TinyTag.get(sourceDir+filename).title
        if newfilename and newfilename is not None:
            log_info("Filename " + filename + " parsed to ")
            filename = newfilename
    except Exception as e:
        log_error(e, "parseFileName while parsing " + filename)
    try:
        filename = filename[re.search("[a-zA-Z]", filename).start():]
    except Exception as e:
        log_error(e, "parseFileName after parsing " + filename + " to " + newfilename)
    filename = re.sub(r'\([^)]*\)', '', filename)
    filename = re.sub(r'\[[^\]]*\]', '', filename)
    filename = re.sub(r'(?i)(www.(.*).com)','',filename)
    filename = re.sub(r'(?i)(www.(.*).eu)','',filename)
    filename = re.sub(r'(?i)(www.(.*).pk)','',filename)
    filename = filename.split(',')[0]
    filename = filename.split('.mp3')[0]
    filename = re.sub(r'[-+_.]', ' ', filename)
    filename = re.sub(r' +',' ',filename).strip()
    log_info(filename);
    return filename;

def getQuery(filename):
    return '+'.join(parseFilename(filename).split(' '))

def createFile(newfilename, content):
    try:
        file = open(destDir+newfilename+'.txt', 'wb')
        file.write(parseTextToFileFormat(content))
        log_info("File created : " + destDir+newfilename+'.txt')
        file.close()
        file = open(lyricRepo+newfilename+'.txt', 'wb')
        file.write(parseTextToFileFormat(content))
        log_info("File created : " + lyricRepo+newfilename+'.txt')
        file.close()
    except Exception as e:
        log_error(e, "createFile")

def getURLFromGoogleSearchAPI(filename):
    query=getQuery(filename) + "+lyrics"
    try:
        requestString='http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + query
        req = urllib2.Request(requestString, headers={"User-Agent" : "Magic Browser"})
        response = urllib2.urlopen(req)
        str_response = response.readall().decode('utf-8')
        testjson = json.loads(str_response)
        return testjson["responseData"]["results"][0]["unescapedUrl"]
    except Exception as e:
        return False

def getURLFromGoogleSearch(filename):
    query=getQuery(filename) + "+lyrics"
    try:
        requestString='http://www.google.com/search?client=aff-maxthon-maxthon4&channel=t26&q=' + query
        req = urllib2.Request(requestString, headers={"User-Agent" : "Magic Browser"})
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response.read())
        response.close()
        return soup.find(id="ires").find_all('a')[0].get('href').split("/url?q=")[1].split("&")[0]
    except Exception as e:
        return False

def parseLyricsMania(response):
    soup = BeautifulSoup(response.read())
    response.close()
    print(soup.prettify())
    
def parseTextToFileFormat(str):
    try:
        output='\n'.join(str.split('\\r\\n'))
        output=re.sub(r'(\s\s)','~',output)
        output='\n'.join(output.split('\\n\\n'))
        output=re.sub(r'(~)+\n','\n',output)
        output='\n'.join(output.split('~'))
        output='\n'.join(output.split('\\n'))
        output='\''.join(output.split('\\\''))
        output=re.sub(r'\n\n*','\n',output)
        output=output.strip()
        return output.encode('utf8').replace(b'\n',b'\r\n')
    except Exception as e:
        log_error(e, "parseTextToFileFormat")

def parseLyrics(filename):
    url=getURLFromGoogleSearch(filename)
    req = urllib2.Request(url, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen(req)
    domain=url.split("http://")[1].split("/")[0]
    newfilename=parseFilename(filename)
    soup = BeautifulSoup(response.read())
    response.close()
    if "www.azlyrics.com" in url:
        createFile(newfilename,str(soup).split("<!-- start of lyrics -->")[1].split("<!-- end of lyrics -->")[0].replace("<br/>","\n"))
    elif "www.lyricsmasti.com" in url:
        createFile(newfilename,BeautifulSoup(str(soup.find(id="lcontent1"))).get_text("\n"))
    elif "www.lyricsintelugu.com" in url or "www.lyriclahari.com" in url or ".blogspot." in url:
        createFile(newfilename,BeautifulSoup(str(soup.find_all(class_="post-body entry-content")[0])).get_text("\n"))
    elif "www.lyricsmania.com" in url:
        createFile(newfilename,parseLyricsMania(response))
    elif "www.lyricsmint.com" in url:
        createFile(newfilename,soup.find_all(class_="post-entry")[0].get_text("\n"))
    elif "www.glamsham.com" in url:
        createFile(newfilename,soup.find_all(class_="general")[6].get_text("\n"))
    elif "www.metrolyrics.com" in url:
        createFile(newfilename,soup.find(id="lyrics-body-text").get_text("\n"))
    elif "annamacharya-lyrics.blogspot" in url:
        createFile(newfilename,soup.find_all(class_="post-body")[0].get_text("\n"))
    elif "www.justsomelyrics.com" in url:
        createFile(newfilename,soup.find_all(class_="core-left")[0].get_text("\n"))
    elif "www.lyricsmode.com" in url:
        createFile(newfilename,soup.find(id="lyrics_text").get_text("\n"))
    elif "www.lyricsfreak.com" in url:
        createFile(newfilename,soup.find(id="content_h").get_text("\n"))
    elif "songlyrics.blogsplug.in" in url:
        createFile(newfilename,soup.find_all(class_="entry")[0].get_text("\n"))
    elif "www.thelyricarchive.com" in url:
        createFile(newfilename,soup.find_all("td")[9].get_text("\n"))
    elif "www.stlyrics.com" in url:
        createFile(newfilename,soup.find(id="page").get_text("\n"))
    elif "www.releaselyrics.com" in url:
        createFile(newfilename,soup.find(id="id-content").get_text("\n"))
    elif "www.songlyrics.com" in url:
        createFile(newfilename,soup.find(id="songLyricsDiv").get_text("\n"))
    elif "songmeanings.com" in url:
        createFile(newfilename,soup.find_all(class_="holder lyric-box")[0].get_text("\n"))
    elif "www.lyrster.com" in url:
        createFile(newfilename,soup.find(id="lyrics").get_text("\n"))
    elif "www.animelyrics.com" in url:
        createFile(newfilename,soup.find_all(class_="lyrics")[0].get_text("\n"))
    elif "www.bobdylan.com" in url:
        createFile(newfilename,soup.find_all(class_="field-items")[0].get_text("\n"))
    elif "www.hindilyrics.net" in url:
        createFile(newfilename,soup.find_all("font")[0].get_text("\n"))
    elif "razarumi.com" in url:
        createFile(newfilename,soup.find_all(class_="content")[0].get_text("\n"))
    elif "www.lyriczz.com" in url:
        createFile(newfilename,soup.find_all(class_="lyriczz")[0].get_text("\n"))
    elif "www.lyricsoff.com" in url:
        createFile(newfilename,soup.find(id="main_lyrics").get_text("\n"))
    else:
        log_info("Domain is : " + domain + " . URL is : " + url + " .Unable to parse. Skipping...")
        unabletoparse.append("Domain : " + domain + ". URL :" + url)
    
songslist=[]
for name in os.listdir(sourceDir):
    if(name.endswith('.mp3')):
        songslist.append(name)
total=len(songslist)
i=0
print("Extracting lyrics", end="")
for filename in songslist:
#filename="sore feet song.mp3"
    i=i+1
    #print(str(round(i*100/total, 1)) + "% done")
    print(".", end="")
    newfilename=parseFilename(filename)
    if os.path.isfile(destDir + newfilename + '.txt'):
        log_info('Lyrics ' + destDir + newfilename + '.txt' + ' already present. Skipping..')
    elif os.path.isfile(lyricRepo + newfilename + '.txt'):
        log_info('Copying lyrics from repo for : ' + newfilename + '...')
        shutil.copyfile(lyricRepo + newfilename + '.txt', destDir + newfilename + '.txt')
    else:
        time.sleep(5)
        try:
            parseLyrics(filename)
        except Exception as e:
            log_error(e, "searching lyrics via google")
            unabletoparse.append(filename)

print("Lyrics not found for : ")
print(unabletoparse)
