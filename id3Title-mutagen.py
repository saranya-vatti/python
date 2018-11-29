from mutagen.id3 import ID3
import os

sourceDir = 'E:\\Music\\English\\'
#sourceDir = 'I:\\Music\\'

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
        
def parseFilename(filename):
    #check out id3 for recently downloaded files
    origfilename = filename
    audio = ID3(sourceDir+filename)
    print(audio)
    filename = audio["TIT2"].text[0]
    log_info("Filename:: " + origfilename + "; Parsed to:: " + filename)


songslist=[]
for name in os.listdir(sourceDir):
    if(name.endswith('.mp3')):
        songslist.append(name)
total=len(songslist)
i=0
success=0
print("Extracting id3 tags", end="")
for filename in songslist:
    i=i+1
    #print(str(round(i*100/total, 1)) + "% done", end="")
    print(".", end="")
    try:
        newfilename=parseFilename(filename)
        success=success+1
    except Exception as e:
        pass
    
print()
print("Successfully extracted id3 titles from : " + str(success) + " files out of " + str(total))
