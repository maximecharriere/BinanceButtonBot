from typing import final
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
from time import time, sleep
import mysql.connector
import json 
import requests

CHROMEDRIVER_PATH = "C:/dev/chromedriver_win32/chromedriver.exe"
URL = "https://www.binance.com/en/activity/bitcoin-button-game"

MYSQL_QUERY = """
INSERT INTO `binance_btn_stats` (`timestamp_unix`, `participants_tot`, `countdown_min`) 
VALUES 
(%s, %s, %s);
"""

def main ():
    try:

        ### CONFIG ###
        try:
            r =requests.get(URL)
            if (r.status_code != 200):
                raise ReferenceError(f"URL '{URL}' isn't accessible")
        except ReferenceError as e:
            print(f"{type(e).__name__} : {e}")
            return 1

        try:
            with open('db_login.json') as json_file:
                login = json.load(json_file)
        except FileNotFoundError as e:
            print(f"{type(e).__name__} : {e}")
            return 1

        try:
            mydb = mysql.connector.connect(
                host     = login["host"],
                user     = login["user"],
                password = login["password"],
                database = login["database"])
            mycursor = mydb.cursor()
        except mysql.connector.Error as e:
            print(f"{type(e).__name__} : {e}")
            return 1

        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--disable-gpu')
            s=Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(
                service=s,
                options=chrome_options)
            # driver = webdriver.Remote("http://localhost:4444/wd/hub", options=chrome_options)
        except WebDriverException as e:
            print(f"{type(e).__name__} : {e}")
            return 1

        ### MAIN ###
        driver.get(URL)
        countdown = []
        start_m = time()

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
                try:
                    mycursor.execute(MYSQL_QUERY, (start_m,participants,countdown_min))
                    mydb.commit()
                except mysql.connector.Error as e:
                    print(f"{type(e).__name__} : {e}")
                    return 2
                else:
                    print(f"Row writed: {start_m}, {participants}, {countdown_min}")

            to_sleep = 1.0+start_s-time()
            sleep(to_sleep) if to_sleep>=0 else print("PROCESS TIME > 1s !!")

    finally:
        if mydb is not None:
            mydb.close()
        if mycursor is not None:
            mycursor.close()
        if driver is not None:
            driver.quit()



if __name__ == "__main__":
    exit(main())


