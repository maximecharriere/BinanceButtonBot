from selenium import webdriver
from bs4 import BeautifulSoup
from time import time, sleep
import csv

driver = webdriver.Chrome("C:/dev/chromedriver_win32/chromedriver.exe")
driver.get("https://www.binance.com/en/activity/bitcoin-button-game")

countdown = []
start_m = 0
with open('BinanceButtonStats.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    while True:
        start_s = time()
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        
        matches =  soup.findAll('div', attrs={'class':'css-w39bvu'})
        countdown.append(float(matches[0].text+matches[1].text+'.'+matches[2].text+matches[3].text))
        if (start_s >= start_m+60.0):
            start_m = start_s

            countdown_min = min(countdown)
            countdown.clear()
            matches =  soup.findAll('div', attrs={'class':'css-th68ec'})
            totalParticipants = int(matches[1].text.replace(",",""))
            csvwriter.writerow([start_m,countdown_min,totalParticipants])
            print(f"Row writed: {start_m},{countdown_min},{totalParticipants}")

        to_sleep = 1.0+start_s-time()
        sleep(to_sleep) if to_sleep>=0 else print("PROCESS TIME > 1s !!")
        
        
