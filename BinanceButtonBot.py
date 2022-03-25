from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import time, sleep

driver = webdriver.Chrome("C:/dev/chromedriver_win32/chromedriver.exe")
driver.get("https://www.binance.com/en/activity/bitcoin-button-game")

start = time()
counter = []
while True:
    sleep(1.0 - time() % 60)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    
    matches =  soup.findAll('div', attrs={'class':'css-w39bvu'})
    counter.append(float(matches[0].text+matches[1].text+'.'+matches[2].text+matches[3].text))

    if (time() >= start+60.0):
        start = time()
        matches =  soup.findAll('div', attrs={'class':'css-th68ec'})
        totalParticipants = int(matches[1].text.replace(",",""))
    
    
