import os
import shutil
import re
import fnmatch

sourceDir = 'H:\\Sort\\'

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

def parseFilename(filename):
    match = re.search("\d{4}", filename)
    date = None
    extension = None
    if match:
        date = match.group(0)
        filename = re.sub(r'(' + date + ')', '', filename)
    filename = re.sub(r'\[[^\]]*\]', '', filename)
    filename = re.sub(r'\([^)]*\)', '', filename)
    filename = re.sub(r'(Xvid-Anarchy)', '', filename)
    filename = re.sub(r'( - Copy)', '', filename)
    filename = re.sub(r'[-+_~]', ' ', filename)
    for crap in ['\[1080p\]', '\[720p\]', '\[YTS\.AG\]', '720p', 'BRip', 'x264', 'COD', 'BRrip', 'DVDScr', 'XVID', 'AC3', 'HQ', 'Hive', 'CM8', 'BluRay', 'DvDRip', 'Xvid-Anarchy', 'BRRip', 'RARBG', 'AAC', 'H264', 'ESubs', 'Downloadhub', '5.1', '7.7', 'MSubs', 'Xvid', 'YIFY', 'Hindi', 'CharmeLeon', 'RG', '1080p', 'BrRip', 'BOKUTOX', 'DVDRip', 'Want3d', 'panTHEr', 'KING', 'Hon3y', 'PLAYNOW']:
        filename = re.sub(r'(' + crap + ')', '', filename)
    # filename, extension = os.path.splitext(filename)
    for ext in ['mp4', 'mkv', 'avi', 'sub', 'srt']:
        if filename[-4:] == "." + ext:
            extension = "." + ext
            filename = filename[:-4]
            break
    filename = re.sub(r'[.]', ' ', filename)
    filename = filename.split(',')[0]
    if date:
        filename = filename + " [" + date + "]"
    if extension:
        filename = filename + extension
    filename = re.sub(r' +',' ',filename)
    return filename

#for name in os.listdir(sourceDir):
for root, dir, files in os.walk(sourceDir):
    print("folder : " + root)
    if len(os.listdir(root)) == 0:
        os.rmdir(root)
    for file in fnmatch.filter(files, "*"):
        if (os.path.getsize(root + "\\" + file)) > 1000000:
            if root != sourceDir:
                log_debug("Moving : " + file)
            else:
                log_debug("Renaming : " + file)
            os.rename(root + "\\" + file, sourceDir + parseFilename(file))
        else:
            log_debug("Removing : " + file)
            os.remove(root + "\\" + file)
            if len(os.listdir(root)) == 0:
                os.rmdir(root)
        #os.rename(sourceDir + file, sourceDir + parseFilename(file))
