##code to copy all the songs in the playlist to the directory specified

import os
import shutil

sourcePL = 'F:\\Music\\Sleep.wpl'
sourceDir = 'F:\\Music\\'
#destDir = 'E:\\Music\\Lyrics\\'
destDir = 'I:\\Music\\'

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
    
f = open(sourcePL, "r", encoding='utf8')
for line in f:
    try:
        log_debug("Trying to split : " + line)
        tmp = (line.split('src="')[1])
        songfilefullpath = sourceDir + tmp.split('"')[0]
        log_debug("split to : " + songfilefullpath)
        tmplist = songfilefullpath.split("\\")
        songfilename = tmplist[len(tmplist) - 1]
        if os.path.isfile(songfilefullpath) and not os.path.isfile(destDir + songfilename):
            shutil.copyfile(songfilefullpath, destDir + songfilename)
    except Exception as e:
        log_error(e, "splitting line : " + line)
