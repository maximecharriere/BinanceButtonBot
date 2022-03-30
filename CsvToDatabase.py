import csv
import mysql.connector

mysql_insert_query = """
INSERT INTO `binance_btn_stats` (`timestamp`, `countdown_min`, `participants_tot`) 
VALUES 
(FROM_UNIXTIME(%s), %s, %s);
"""

with open('BinanceButtonStats.csv', 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    data = list(csvreader)

try:
    try:
        mydb = mysql.connector.connect(
            host="maximecharriere.ch",
            user="root",
            password="MC@Solaar7Synology",
            database="crypto")
        mycursor = mydb.cursor()
    except mysql.connector.Error as e:
        print(f"Failed to connect to database: {e}")
        raise e
    try:
        mycursor.executemany(mysql_insert_query, data)
        mydb.commit()
    except mysql.connector.Error as e:
        print(f"Failed to insert to database: {e}")
        raise e
finally:
    mycursor.close()
    mydb.close()