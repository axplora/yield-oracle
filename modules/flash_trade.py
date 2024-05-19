from selenium import webdriver
from bs4 import BeautifulSoup 
from selenium.webdriver.firefox.options import Options
from lxml import etree 
import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def flash_trade():
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

    driver = webdriver.Firefox(options=options)
    driver.get('https://beast.flash.trade/earn')

    time.sleep(10)

    vegetables = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()
    soup = BeautifulSoup(vegetables,'html.parser')
    blended_soup = etree.HTML(str(soup)) 

    # Flash trade pool 1
    rate_pool_1 = blended_soup.xpath('//*[@id="__next"]/div[2]/div[3]/main/div[1]/div/div[2]/div/span[1]/div/span')[0].text
    float_rate_1 = float(rate_pool_1.strip("%"))
    rounded_rate_1 = round(float_rate_1,2)
    cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (105, rounded_rate_1))
    conn.commit()

    # Flash trade pool 2
    rate_pool_2 = blended_soup.xpath('//*[@id="__next"]/div[2]/div[3]/main/div[1]/div/div[2]/div/span[2]/div/span')[0].text
    float_rate_2 = float(rate_pool_2.strip("%"))
    rounded_rate_2 = round(float_rate_2,2)
    cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (106, rounded_rate_2))
    conn.commit()

    # Flash trade pool 3
    rate_pool_3 = blended_soup.xpath('//*[@id="__next"]/div[2]/div[3]/main/div[1]/div/div[2]/div/span[3]/div/span')[0].text
    float_rate_3 = float(rate_pool_3.strip("%"))
    rounded_rate_3 = round(float_rate_3,2)
    cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (107, rounded_rate_3))
    conn.commit()

    driver.quit()

if __name__ == "__main__":
    flash_trade()