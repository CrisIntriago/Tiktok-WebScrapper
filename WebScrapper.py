#Selenium for web scrapping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Counter to count dozens of videos
counter=0 
#Importing beautifulSoup
import bs4

#Time to avoid problems while charging page
import time


from Functions import *

s= Service('C:\Program Files (x86)\chromedriver.exe')

browser_options = Options()
browser_options.add_argument("start-maximized")
browser_options.add_argument('--no-sanbox')
browser_options.add_argument('disable-notificatioon')
browser_options.add_argument('--disable-infobars')
browser_options.add_argument("--disable-extensions")
browser_options.add_argument("--mute-audio")




driver= webdriver.Chrome(service=s,options=browser_options)
time.sleep(5)
driver.get("https://www.tiktok.com")
#When i open i got to check if theres a login, sometimes there isn't but to avoid crashing

##I can't click the quit button of the login, have to do it manually still.

try:
    btnPopUp = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-modal"]/div[2]')))
    driver.execute_script("arguments[0].click();", btnPopUp)
    print("Closed the Popup succesfully")
except:
    print("Did not show the Popup")

#I get the bar to enter the hashtags that I'm going to search

barraTEXTO= driver.find_element(By.NAME,"q")

hashtags= input("Enter the hashtags for search, ideally at least 2: ")
#hashtags= "#Tareas #humor #matematicas #universidad"


driver.implicitly_wait(5)

barraTEXTO.send_keys(hashtags)
barraTEXTO.send_keys(Keys.RETURN)
time.sleep(7)


#Download 12 videos, apparently sometimes is only 11..., to avoid that we should put at least 2 hashtags parameters

videosURL=getTheHtml(driver)
download12(videosURL,counter)
counter+=1



confirmation= input("Do you want to download 12 videos more?: Type YES/NO \n")

time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



if confirmation.lower().strip()=="yes": 
    try:
        print("Intentando clickear")
        try:
            moreBtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main-content-general_search"]/div[2]/div[2]/button')))
            driver.implicitly_wait(10)
        except:
            print("Ni se pudo obtener el botón :( para tener 12 más")

        print("Se obtuvo el botón")

        try:
            driver.execute_script("arguments[0].click();", moreBtn)
            print("Se clickeó")
        except Exception as excp:
            print(excp)
        time.sleep(10)
        videosURL=getTheHtml(driver)
        download12(videosURL,counter)
        counter+=1


    except:
        print("Hubo un error al intentar cargar 12 vídeos más")
else:
    print("Thanks for using this software :)")  
     









