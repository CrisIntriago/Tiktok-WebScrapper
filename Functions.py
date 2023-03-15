import requests
#Importing beautifulSoup
import bs4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen

#Function that loads the driver from selenium

def loadDriver():
    PATH= 'C:\Program Files (x86)\chromedriver.exe'
    driver= webdriver.Chrome(PATH)
    return driver

def openWebsite(driver1,link):
    driver1.get(link)
    return driver1

#We get the html with divided by the class which has the video links
def getTheHtml(driver):
    soup= bs4.BeautifulSoup(driver.page_source,"html.parser")
    videosURL=soup.find_all("div",{"class": "tiktok-yz6ijl-DivWrapper e1cg0wnj1"})
    return videosURL



#I download videos by dozen with a counter so when I load 12 videos more I start indexing in 12 and its multiples

def downloadDozen(videosURL,counter):
    for i in range(counter*12,(counter+1)*12):
        try:
            print("Reading the link: "+ videosURL[i].a["href"]+" video number: "+i)
            try:
                downloadVideo(videosURL[i].a["href"],i)
            except:
                print("Renew the code from CurlConverter") # Go to https://curlconverter.com/ manually get the network from SSStik.io which is the website where we delete the watermark
        except IndexError:
            print("Problem with indexes, probably just entered 1 hashtag but still should work, we may lose videos")
        #Because the server would get overloaded and think we are a bot (which we are LOL)
        #We are gonna set 12 seconds delay so it goes smoothly
        time.sleep(12) 



#This calls the SSTIK.IO server and gives me the link immediatly
def downloadVideo(url,id):
    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/es',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/es',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': url,
        'locale': 'es',
        'tt': 'NmJ3YWY0sss', ##IT CHANGES OVERTIME, GO TO CURLCONVERTER.COM AND GET A NEW ONE, its just that change
    }

    response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
    downloadSoup= bs4.BeautifulSoup(response.text,"html.parser")

    downloadURL= downloadSoup.a["href"]
    print(downloadURL)
    try:
        videoMP4= urlopen(downloadURL)
    except:
        print("Could not load the MP4 file,probably internet problems, excedeed the timing.")

    with open(f"videos/{id}"+'.mp4',"wb") as output:
        while True:
            data= videoMP4.read(4096)
            if data:
                output.write(data)
            else:
                break


