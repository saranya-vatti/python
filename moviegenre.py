#goes through each file/folder name in the sourceDir
#gets each one's name and searches in imdb
#in imdb movie category page, goes to the first movie's page
#in the imdb movie page, gets the genre
#if a folder named as that genre already exists in destDir, moves the movie into that folder
#else, creates a new folder and moves it

try:
    import urllib.request as urllib2
except:
    import urllib2
import bs4
from bs4 import BeautifulSoup
import os
import re
import shutil
import time

sourceDir = 'E:\\Movies\\Not seen\\'
destDir = 'E:\\Movies\\'
LOG_LEVELS = {
    "DEBUG" : 100,
    "INFO" : 200,
    "ERROR" : 300,
    "NONE" : 400
}
LOGLVL=LOG_LEVELS["ERROR"]

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
    filename = os.path.splitext(filename)[0]
    try:
        filename = filename[re.search("[a-zA-Z]", filename).start():]
    except Exception as e:
        log_error(e, "parseFileName after parsing " + filename + " to " + newfilename)
    filename = re.sub(r'\([^)]*\)', '', filename)
    filename = re.sub(r'\{[^}]*\}', '', filename)
    filename = re.sub(r'\[[^\]]*\]', '', filename)
    filename = re.sub(r'(?i)(www.(.*).com)','',filename)
    filename = re.sub(r'(?i)(www.(.*).eu)','',filename)
    filename = re.sub(r'(?i)(www.(.*).pk)','',filename)
    filename = re.sub(r'(\d{4})','',filename)
    filename = re.sub(r'[-+_.]', ' ', filename)
    nonostrings=["dvdrip","brrip","yify","bluray","XviD",
                 "WEBRip","x264","AC3","MiLLENiUM","Extended",
                 "uncut","720p","1080p","Bluray","anoXmous",
                 "WEB-DL","AAC","HDStar","JNS","DVDSCR","DivXNL",
                 "axxo","scOrp","MaNuDiL","SilverRG","MitZep",
                 "LIMITED","bdrip","saphire","etrg","FRENCH",
                 "HDRip","English"];
    for nonostring in nonostrings:
        filename = re.sub(r'(?i)('+nonostring+')','',filename)
    filename = filename.split(',')[0]
    filename = filename.split('.mp3')[0]
    filename = re.sub(r' +',' ',filename).strip()
    log_info(filename);
    return filename;

def getQuery(filename):
    return '+'.join(parseFilename(filename).split(' '))

for filename in os.listdir(sourceDir):
    #if(os.path.isfile(sourceDir+filename)):
    newfilename=parseFilename(filename)
    query=getQuery(newfilename)
    requestString='http://www.imdb.com/find?ref_=nv_sr_fn&q=' + query + '&s=tt'
    try:
        req = urllib2.Request(requestString, headers={"User-Agent" : "Magic Browser"})
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response.read())
        response.close()    
        movieurl="http://www.imdb.com"+soup.find_all(class_="findList")[0].find_all("a")[0].get('href')
        req = urllib2.Request(movieurl, headers={"User-Agent" : "Magic Browser"})
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response.read())
        response.close()
        genre=soup.find_all(class_="infobar")[0].find_all('a')[0].get('href').split('/genre/')[1]
        genre=genre.split("?")[0]
        if not os.path.exists(destDir+genre):
            os.makedirs(destDir+genre)
        shutil.move(sourceDir+filename, destDir+genre)
    except Exception as e:
        log_error(e, "requestString " + requestString)
