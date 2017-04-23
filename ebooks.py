##code to extract all the ebooks from http://inzania.com/temp/kindle/books/ and save it to a directory
try:
    import urllib.request as urllib2
except:
    import urllib2
import bs4
from bs4 import BeautifulSoup

destDir = 'E:\\Books\\New folder\\tmp\\'

LOG_LEVELS = {
    "DEBUG" : 100,
    "INFO" : 200,
    "ERROR" : 300,
    "NONE" : 400
}
LOGLVL=LOG_LEVELS["DEBUG"]

def log_error(exception, string):
    if(LOGLVL <= LOG_LEVELS["ERROR"]):
        print("Exception encountered : " + str(type(exception)))
        print("Exception : " + str(exception))
        print(string)

def log_info(string):
    if(LOGLVL <= LOG_LEVELS["INFO"]):
        print(string)

def log_debug(string):
    if(LOGLVL <= LOG_LEVELS["DEBUG"]):
        print(string)
        
requestString='http://inzania.com/temp/kindle/books/'
req = urllib2.Request(requestString, headers={"User-Agent" : "Magic Browser"})
response = urllib2.urlopen(req)
soup = BeautifulSoup(response.read())
for a in soup.find_all('a'):
    try:
        url='http://inzania.com/temp/kindle/books/'+a.get('href')
        filename=destDir+a.get_text().strip()
        urllib2.urlretrieve(url, filename)
    except Exception as e:
        log_error(e, "Error with url:" + url)
response.close()
    

