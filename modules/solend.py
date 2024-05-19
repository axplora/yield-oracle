from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup 
import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def solend():
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

    main_pools = [

        {'name':'sol', 'id':'147'},
        {'name':'usdc', 'id':'148'},
        {'name':'usdt', 'id':'149'},
        {'name':'eth (portal)', 'id':'150'},
        {'name':'slnd', 'id':'151'},
        {'name':'jup', 'id':'152'},
        {'name':'pyth', 'id':'153'},
        {'name':'w', 'id':'154'},
        {'name':'jto', 'id':'155'},
        {'name':'ray', 'id':'156'},
        {'name':'mnde', 'id':'157'},
        {'name':'blze', 'id':'158'},
        {'name':'tbtc', 'id':'159'},
        {'name':'msol', 'id':'160'},
        {'name':'bsol', 'id':'161'},
        {'name':'jitosol', 'id':'162'},
        {'name':'wsteth', 'id':'163'},

    ]

    turbo_sol_pool = [

        {'name':'sol', 'id':'164'},
        {'name':'usdc', 'id':'165'},

    ]

    driver = webdriver.Firefox(options=options)
    driver.get('https://solend.fi/dashboard')
    time.sleep(15)
    vegetables = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()
    soup = BeautifulSoup(vegetables,'html.parser')

    main_pool_data = soup.find_all(class_="ant-table-row ant-table-row-level-0")
    for data_token in main_pool_data:
        token = data_token.find(class_="Typography_primary__ljjY8 Typography_body__iCB0t").text.lower()
        rate = data_token.find(class_="Typography_primary__ljjY8 Typography_body__iCB0t Market_percent__T85bk").text.strip("%")
        rounded_rate = rounded_rate = round(float(rate),2)
        for pool_token in main_pools:
            if token == pool_token['name']:
                cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'],rounded_rate))
                conn.commit()


    # ----------------------------------------------------------------------------- #

    driver = webdriver.Firefox(options=options)
    driver.get('https://solend.fi/dashboard?pool=7RCz8wb6WXxUhAigok9ttgrVgDFFFbibcirECzWSBauM')
    time.sleep(15)
    vegetables = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()
    soup = BeautifulSoup(vegetables,'html.parser')

    turbo_sol_data = soup.find_all(class_="ant-table-row ant-table-row-level-0")
    for data_token in turbo_sol_data:
        token = data_token.find(class_="Typography_primary__ljjY8 Typography_body__iCB0t").text.lower()
        rate = data_token.find(class_="Typography_primary__ljjY8 Typography_body__iCB0t Market_percent__T85bk").text.strip("%")
        rounded_rate = rounded_rate = round(float(rate),2)
        for pool_token in turbo_sol_pool:
            if token == pool_token['name']:
                cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'],rounded_rate))
                conn.commit()

if __name__ == "__main__":
    solend()