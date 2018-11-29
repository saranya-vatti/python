#rename all files in a directory
import os
sourceDir = "D:\\Acads\\Python\\Music\\"
for name in os.listdir(sourceDir):
    if(name.endswith('.mp3.mp3')):
        os.rename(sourceDir + name, sourceDir + name.replace('.mp3.mp3', '.mp3'))
