

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
from tinytag import TinyTag
from selenium import webdriver
from selenium.webdriver.common.by import By

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

driver = webdriver.Chrome('C:\\Users\\saran\\Acads\\Python\\chromedriver')
driver.get('https://www.instagram.com/accounts/login/?hl=en')
username = driver.find_elements_by_class_name("zyHYP")[0]
password = driver.find_elements_by_class_name("zyHYP")[1]
username.send_keys("saranyavatti")
password.send_keys("labyrinthsole")
driver.find_element(By.XPATH, '//button[text()="Log in"]').click()
time.sleep(3)
driver.find_elements_by_class_name("HoLwm")[0].click()
driver.find_elements_by_class_name("x3qfX")[0].send_keys("#humansoftuck")
time.sleep(1)
driver.find_elements_by_class_name("Ap253")[0].click()
time.sleep(2)

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(6)

post_links = set()
user_likes = {}
last_visited = 0

total = len(driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a"))
print(total)
while last_visited<54:
    a_elem = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a")[last_visited]
    link = a_elem.get_attribute("href")
    a_elem.click()
    time.sleep(3)
    username = driver.find_element_by_class_name("nJAzx").get_attribute("title")
    likes = int(driver.find_element_by_xpath("//div[@class='Nm9Fw']/button/span").get_attribute("innerHTML"))
    post_links.add(link)
    if username not in user_likes:
        user_likes[username]=0
    user_likes[username]=user_likes.get(username)+likes
    driver.find_element_by_class_name("ckWGn").click()
    last_visited = last_visited+1
    print(user_likes)

##for elem in driver.find_elements_by_class_name("_bz0w"):
##    #driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG _bz0w']/a"):
##    try:
##        for elem2 in elem.find_elements_by_xpath(".//a"):
##            try:
##                link = elem2.get_attribute("href")
##                if link not in post_links :
##                    elem.click()
##                    time.sleep(2)
##                    username = driver.find_element_by_class_name("nJAzx").get_attribute("title")
##                    likes = int(driver.find_element_by_xpath("//div[@class='Nm9Fw']/button/span").get_attribute("innerHTML"))
##                    post_links.add(link)
##                    if username not in user_likes:
##                        user_likes[username]=0
##                    user_likes[username]=user_likes.get(username)+likes
##                driver.find_element_by_class_name("ckWGn").click()
##                time.sleep(1)
##                print(user_likes)
##                   
##            except Exception as e:
##                log_error(e, "trying to get linnks from the posts page : ")
##        except Exception as e:
##            log_error(e, "trying to find the post in the link
            

print(user_likes)
