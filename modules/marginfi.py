from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup 
import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def marginfi():
    options = Options()
    options.add_argument("--headless")

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT')
        )

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    lending_pools = [

        {'name':'jitosol', 'id':'166'},
        {'name':'$wif', 'id':'167'},
        {'name':'sol', 'id':'168'},
        {'name':'msol', 'id':'169'},
        {'name':'lst', 'id':'170'},
        {'name':'bsol', 'id':'171'},
        {'name':'bonk', 'id':'172'},
        {'name':'inf', 'id':'173'},
        {'name':'usdt', 'id':'174'},
        {'name':'jto', 'id':'175'},
        {'name':'usdc', 'id':'176'},
        {'name':'wbtc', 'id':'177'},
        {'name':'jup', 'id':'178'},
        {'name':'pyth', 'id':'179'},
        {'name':'eth', 'id':'180'},
        {'name':'hnt', 'id':'181'},
        {'name':'uxd', 'id':'182'},
        {'name':'dust', 'id':'183'},

        ]

    driver = webdriver.Firefox(options=options)
    driver.get('https://app.marginfi.com/')
    time.sleep(15)
    vegetables = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()
    soup = BeautifulSoup(vegetables,'html.parser')
    pre_lending = soup.find(class_="[&_tr:last-child]:border-0") 
    lending = pre_lending.find_all(class_="transition-colors data-[state=selected]:bg-muted")
    for pools in lending:
        token = pools.find(class_="flex gap-4 justify-start items-center").text.lower()
        rate = pools.find(class_="flex justify-end").text.strip("%")
        rounded_rate = rounded_rate = round(float(rate),2)
        for pool_token in lending_pools:
            if token == pool_token['name']:
                cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'],rounded_rate))
                conn.commit()

if __name__ == "__main__":
    marginfi()