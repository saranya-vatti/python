#TODO :
#use dictionaries in modules instead of creating and destroying every time it runs

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
from mutagen.id3 import ID3

sourceDir = 'I:\\Music\\'
lyricRepo = 'E:\\Music\\Lyrics\\'
#sourceDir = 'E:\\Music\\Hindi\\'
destDir = 'I:\\Lyrics\\'
#destDir = 'E:\\Music\\Lyrics\\'
languageList=['tamil','telugu','hindi','english']
songsDir={
    'tamil':'E:\\Music\\Tamil\\',
    'telugu':'E:\\Music\\Telugu\\',
    'hindi':'E:\\Music\\Hindi\\',
    'english':'E:\\Music\\English\\'
}
wordList = {
    'tamil':[],
    'telugu':[],
    'hindi':[],
    'english':[]
}
lyricsnotfound = []
LOG_LEVELS = {
    "DEBUG" : 100,
    "INFO" : 200,
    "ERROR" : 300,
    "NONE" : 400
}
LOGLVL=LOG_LEVELS["DEBUG"]

def getQuery(filename):
    return '+'.join(parseFilename(filename).split(' '))

def parseFilename(filename):
    #check out id3 for recently downloaded files
    try:
        audio = ID3(sourceDir+filename)
        filename = audio["TIT2"].text[0]
        log_info("Filename::" + filename)
    except Exception as e:
        log_error(e, "parseFileName")
    filename = filename[re.search("[a-zA-Z]", filename).start():]
    filename = re.sub(r'\([^)]*\)', '', filename)
    filename = re.sub(r'\[[^\]]*\]', '', filename)
    filename = re.sub(r'(?i)(www.(.*).com)','',filename)
    filename = re.sub(r'(?i)(www.(.*).eu)','',filename)
    filename = filename.split(',')[0]
    filename = filename.split('.mp3')[0]
    filename = re.sub(r'[-+_.]', ' ', filename)
    filename = re.sub(r' +',' ',filename)
    return filename;

def parseTextToFileFormat(str):
    output='\n'.join(str.split('\\r\\n'))
    output = re.sub(r'(\s\s)','~',output)
    output='\n'.join(output.split('\\n\\n'))
    output = re.sub(r'(~)+\n','\n',output)
    output = '\n'.join(output.split('~'))
    output='\n'.join(output.split('\\n'))
    output='\''.join(output.split('\\\''))
    return output.strip()

def createFile(newfilename, content):
    file = open(destDir+newfilename+'.txt', 'w')
    file.write(parseTextToFileFormat(content))
    file.close()

def searchEnglishLyrics(filename):
    query=getQuery(filename)
    requestString = 'http://search.azlyrics.com/search.php?q=' + query
    req = urllib2.Request(requestString, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen( req )
    soup = BeautifulSoup(response.read())
    songList = soup.find_all(text="Song results:")
    try:
        if len(songList) > 0 :
            albumList = soup.find_all(text="Album results:")
            if(len(albumList)>0):
                albumNum = int(soup.find_all(class_="hlfound")[0].get_text().split('[1-')[1].split(' ')[0])
            else:
                albumNum=0
                alist=soup.find(id="inn").find_all('a')
                anum=len(alist) - albumNum
                if anum>0 :
                    req2 = urllib2.Request(alist[albumNum].get('href'), headers={"User-Agent" : "Magic Browser"})
                    response2 = urllib2.urlopen( req2 )
                    soup2 = BeautifulSoup(str(response2.read()).split('<!-- start of lyrics -->')[1].split('<!-- end of lyrics -->')[0])
                    newfilename=parseFilename(filename)
                    createFile(newfilename,soup2.get_text("\n"))
                    response2.close()
                    return True
    except Exception as e:
        log_error(e, "searchEnglishLyrics")
    response.close()
    lyricsnotfound.append(filename)
    log_info("Lyrics in english songs not found for : " + filename)
    return False

def searchTeluguLyrics(filename):
    query=getQuery(filename)
    requestString = 'http://www.google.co.in/cse?cx=partner-pub-8569787277823547:9213590181&q=' + query + '&sa=Search#gsc.tab=0&gsc.q=' + query + '&gsc.page=1'
    req = urllib2.Request(requestString, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read())
    div=soup.find(id="res")
    try:
        reqtel = urllib2.Request(div.find_all('a')[1].get('href'), headers={"User-Agent" : "Magic Browser"})
        responsetel = urllib2.urlopen( reqtel )
        souptel = BeautifulSoup(responsetel.read())
        soupdiv=BeautifulSoup(str(souptel.find_all(class_="post-body entry-content")[0]))
        newfilename=parseFilename(filename)
        createFile(newfilename,soupdiv.get_text("\n"))
        responsetel.close()
        return True
    except Exception as e:
        log_error(e, "searchTeluguLyrics")
    response.close()
    lyricsnotfound.append(filename)
    log_info("Lyrics in telugu songs not found for : " + filename)
    return False

def searchHindiLyrics(filename):
    query=getQuery(filename)
    log_debug("Searching lyrics in hindi songs for : " + filename)
    requestString = 'http://www.google.com/cse?cx=002906559931738959499%3Avsqae11ldg8&q=' + query + '&sa=Search#gsc.tab=0&gsc.q=' + query + '&gsc.page=1'
    req = urllib2.Request(requestString, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read())
    div=soup.find(id="res")
    try:
        if "Search instead for" in div.get_text():
            reqtel = urllib2.Request(div.find_all('a')[3].get('href'), headers={"User-Agent" : "Magic Browser"})
        else:
            reqtel = urllib2.Request(div.find_all('a')[1].get('href'), headers={"User-Agent" : "Magic Browser"})        
        responsetel = urllib2.urlopen( reqtel )
        souptel = BeautifulSoup(responsetel.read())
        soupdiv=BeautifulSoup(str(souptel.find(id="lcontent1")))
        newfilename=parseFilename(filename)
        createFile(newfilename,soupdiv.get_text("\n"))
        responsetel.close()
        return True
    except Exception as e:
        log_error(e, "searchHindiLyrics")
    response.close()
    log_info("Lyrics in hindi songs not found for : " + filename)
    lyricsnotfound.append(filename)
    return False

def searchTamilLyrics(filename):
    query=getQuery(filename)
    log_debug("Searching lyrics in tamil songs for : " + filename)
    requestString = 'http://www.google.co.in/cse?cx=015820681720464487820%3Agpjgf3255ve&q=' + query + '&sa=Search#gsc.tab=0&gsc.q=' + query + '&gsc.page=1'
    req = urllib2.Request(requestString, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read())
    div=soup.find(id="res")
    try:
        reqtamil = urllib2.Request(div.find_all('a')[1].get('href'), headers={"User-Agent" : "Magic Browser"})
        responsetamil = urllib2.urlopen( reqtamil )
        souptamil = BeautifulSoup(responsetamil.read())
        soupdiv = BeautifulSoup(str(souptamil.find(id="lyricscontent")))
        newfilename=parseFilename(filename)
        createFile(newfilename,BeautifulSoup(str(soupdiv).split("<h2")[0]).get_text("\n"))
        responsetamil.close()
        return True
    except Exception as e:
        log_error(e, "searchTamilLyrics")
    response.close()
    lyricsnotfound.append(filename)
    log_info("Lyrics in tamil songs not found for : " + filename)
    return False

def initWordLists():
    for language in languageList:
        wordList[language]=[]
        for filename in os.listdir(songsDir[language]):
            if(filename.endswith('.mp3')):
                filename=parseFilename(filename)
                wordList[language]=wordList[language]+filename.split(' ')
        wordList[language]=list(set(wordList[language]))
                
def getSongLanguage(wl):
    for word in wl:
        for lang in wordList:
            if word in wordList[lang]:
                return lang
    return None

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
        
#initWordLists()
total=len(os.listdir(sourceDir))
i=1
#for filename in os.listdir(sourceDir):
filename = "Ye safar bahut hain.mp3"
print(str(round(i*100/total, 1)) + "% done")
i=i+1
if(filename.endswith('.mp3')):
    newfilename=parseFilename(filename)
    if os.path.isfile(destDir + newfilename + '.txt'):
        log_info('Lyrics ' + destDir + newfilename + '.txt' + ' already present for : ' + newfilename + '. Skipping..')
    elif os.path.isfile(lyricRepo + newfilename + '.txt'):
        shutil.copyfile(lyricRepo + newfilename + '.txt', destDir + newfilename + '.txt')
    else:
        wl=newfilename.split(' ')
        language = getSongLanguage(wl)
        if(language == "tamil"):
            searchTamilLyrics(newfilename)
        elif(language == "telugu"):
            searchTeluguLyrics(newfilename)
        elif(language == "hindi"):
            searchHindiLyrics(newfilename)
        elif(language == "english"):
            searchEnglishLyrics(newfilename)
        else:
            log_info("Unable to detect language for : " + newfilename)
            lyricsnotfound.append(newfilename)
            print("Do you want to enter the language for " + newfilename + "?")
            inp=input("1 for tamil, 2 for telugu, 3 for hindi, 4 for english, 5 to exit\n")
            if(inp=="1"):
                wordList["tamil"]=wordList["tamil"]+newfilename.split(' ')
                wordList["tamil"]=list(set(wordList["tamil"]))
                searchTamilLyrics(newfilename)
            if(inp=="2"):
                wordList["telugu"]=wordList["telugu"]+newfilename.split(' ')
                wordList["telugu"]=list(set(wordList["telugu"]))
                searchTeluguLyrics(newfilename)
            if(inp=="3"):
                wordList["hindi"]=wordList["hindi"]+newfilename.split(' ')
                wordList["hindi"]=list(set(wordList["hindi"]))
                searchHindiLyrics(newfilename)
            if(inp=="4"):
                wordList["english"]=wordList["english"]+newfilename.split(' ')
                wordList["english"]=list(set(wordList["english"]))
                searchEnglishLyrics(newfilename)
            if(inp=="5"):
                log_info("Lyrics not found for " + newfilename)
                lyricsnotfound.append(newfilename)
        time.sleep(5)
        
print("Lyrics not found for : ")
print(lyricsnotfound)
