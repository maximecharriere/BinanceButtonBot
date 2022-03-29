from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import time, sleep
import csv
import mysql.connector

mysql_insert_query = """
INSERT INTO `binance_btn_stats` (`timestamp`, `participants_tot`, `countdown_min`) 
VALUES 
(FROM_UNIXTIME(%s), %s, %s);
"""

try:
    mydb = mysql.connector.connect(
        host="",
        user="",
        password="",
        database="")
    mycursor = mydb.cursor()

except mysql.connector.Error as e:
    print(f"Failed to connect to database: {e}")
    exit()

CHROMEDRIVER_PATH = "C:/dev/chromedriver_win32/chromedriver.exe"
WINDOW_SIZE = "1920,1080"
URL = "https://www.binance.com/en/activity/bitcoin-button-game"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(
    executable_path=CHROMEDRIVER_PATH,
    options=chrome_options)
# driver = webdriver.Remote("http://localhost:4444/wd/hub", options=chrome_options)

driver.get(URL)

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
            participants = int(matches[1].text.replace(",",""))
            csvwriter.writerow([start_m,countdown_min,participants])
            print(f"Row writed: {start_m},{countdown_min},{participants}")
            try:
                mycursor.execute(mysql_insert_query, (start_m,participants,countdown_min))
                mydb.commit()
            except mysql.connector.Error as e:
                print(f"Failed to insert to database: {e}")
                exit()

        to_sleep = 1.0+start_s-time()
        sleep(to_sleep) if to_sleep>=0 else print("PROCESS TIME > 1s !!")
        
        
