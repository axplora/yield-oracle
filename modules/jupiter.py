from selenium import webdriver
from bs4 import BeautifulSoup 
from selenium.webdriver.firefox.options import Options
from lxml import etree 
import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def jupiter():
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
    cursor = conn.cursor()

    driver = webdriver.Firefox(options=options)
    driver.get('https://jup.ag/perps-earn')

    time.sleep(10)

    vegetables = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()

    soup = BeautifulSoup(vegetables,'html.parser')
    blended_soup = etree.HTML(str(soup)) 
    rate = blended_soup.xpath('//*[@id="__next"]/div[2]/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/p')[0].text
    float_rate = float(rate.strip("%"))
    rounded_rate = round(float_rate,2)

    cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (53, rounded_rate))
    conn.commit()

if __name__ == "__main__":
    jupiter()