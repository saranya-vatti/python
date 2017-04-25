##code to extract all the courses from:
## https://ufl.instructure.com/courses/335491/pages/travel-preparations?module_item_id=6386108
## https://ufl.instructure.com/courses/335491/pages/life-at-uf?module_item_id=6386109
from selenium import webdriver
import time
try:
    import urllib.request as urllib2
except:
    import urllib2
import re

destDir = 'D:\\Acads\\Python\\Voyages\\'

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

#options = webdriver.ChromeOptions()
#options.add_argument("download.default_directory=D:\\Acads\\Python\\Voyages\\")
#driver = webdriver.Chrome('D:\\Softwares\\Python\\chromedriver', chrome_options=options)
driver = webdriver.Chrome('D:\\Softwares\\Python\\chromedriver')
driver.get('https://ufl.instructure.com/courses/335491/pages/travel-preparations?module_item_id=6386108');
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
username.send_keys("saranyavatti")
password.send_keys("Awsedr9102")
driver.find_element_by_id("submit").click()

filename = re.sub(r' +', '', driver.find_element_by_class_name("page-title").text)
iframe = driver.find_elements_by_tag_name("iframe")[1]
driver.switch_to_frame(iframe)
time.sleep(3)
videoUrl = driver.find_element_by_xpath(".//source[@type='video/mp4']").get_attribute("src").split("?")[0]
f = urllib2.urlopen(videoUrl)
data = f.read()
with open(filename + ".mp4", "wb") as code:
    code.write(data)
