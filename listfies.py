import os

path = '\\\\L-ANILKUMAR-ILB'
path = bytes(path, "utf-8").decode("unicode_escape")
print (os.listdir(path))
