##code to copy all the songs in the playlist to the directory specified

import os
import shutil

basePath = 'D:\\TrafficSplitter\\trafficSplitter-git\\trafficSplitter.js\\js\\modules\\trafficsplitter\\'
os.chdir(basePath)
entryFile = 'TrafficSplitter.js'

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

def convertRelToAbs(rel, base):
    try:
        log_debug ("base : " + base)
        arr = base.split("\\");
        arr.pop()
        log_debug ("rel : " + rel)
        rel = rel.replace("\";", "")
        if(rel.startswith("./")):
            return "//".join(arr)
        for _ in range(rel.count("../")):
            arr.pop()
        rel = rel.replace("/", "//")
        log_debug("converted to : " + "//".join(arr) + "//" + rel.replace("..//", ""))
        return "//".join(arr) + "//" + rel.replace("..//", "")
    except Exception as e:
        log_error(e, "error with path: " + rel)

printedFiles = []
def printDepTree(f, depLevel):
    global printedFiles
    base = os.path.abspath(f.name)
    printFileName = os.path.basename(f.name)
    if (printFileName not in printedFiles):
        for _ in range(depLevel):
            print("-", end="")
        print (printFileName)
        printedFiles.append(printFileName)
        for line in f:
            try:
                while ("import" in line):
                    folder = convertRelToAbs(line.split("from \"")[1], base).strip().replace("./", "")
                    os.chdir(folder)
                    fileNameArr = line.split("{")[1].split("}")[0].split(",")
                    for fileName in fileNameArr:
                        fileName = fileName + ".js"
                        fileName = fileName.strip()
                        log_debug("Opening file : " + folder.replace("//", "/") + "/" + fileName)
                        if (os.path.isfile(folder + "//" + fileName)):
                            file = open(folder + "//" + fileName)
                        elif (fileName == "UserAgentParser.js"):
                            file = open(folder + "//UAParser.js")
                        printDepTree(file, depLevel + 1)
                    break
            except Exception as e:
                log_error(e, "error in line: " + line)
    else:
        log_debug("Skipping " + printFileName)

file = open(os.getcwd() + "\\" + entryFile, "r", encoding="utf8")
printDepTree(file, 0)
