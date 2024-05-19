from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup 
import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def mango_markets():
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

        {'name':'JUP', 'id':'54'},
        {'name':'RAY', 'id':'55'},
        {'name':'MNDE', 'id':'57'},
        {'name':'SOL', 'id':'58'},
        {'name':'STEP', 'id':'59'},
        {'name':'MNGO', 'id':'61'},
        {'name':'MSOL', 'id':'63'},
        {'name':'USDH', 'id':'64'},
        {'name':'ZEUS', 'id':'66'},
        {'name':'W', 'id':'67'},
        {'name':'wBTC (Portal)', 'id':'68'},
        {'name':'JLP', 'id':'69'},
        {'name':'JTO', 'id':'70'},
        {'name':'BLZE', 'id':'71'},
        {'name':'GOFX', 'id':'72'},
        {'name':'DUAL', 'id':'73'},
        {'name':'TNSR', 'id':'75'},
        {'name':'META', 'id':'76'},
        {'name':'ORCA', 'id':'78'},
        {'name':'JitoSOL', 'id':'79'},
        {'name':'GUAC', 'id':'80'},
        {'name':'USDT', 'id':'81'},
        {'name':'BONK', 'id':'82'},
        {'name':'ETH (Portal)', 'id':'83'},
        {'name':'SAMO', 'id':'86'},
        {'name':'PYTH', 'id':'87'},
        {'name':'NOS', 'id':'89'},
        {'name':'RENDER', 'id':'92'},
        {'name':'WIF', 'id':'93'},
        {'name':'HNT', 'id':'94'},
        {'name':'TBTC', 'id':'95'},
        {'name':'bSOL', 'id':'96'},
        {'name':'WEN', 'id':'99'},
        {'name':'GECKO', 'id':'100'},
        {'name':'DAI', 'id':'101'},
        {'name':'USDC', 'id':'103'},
        {'name':'KMNO', 'id':'144'},
        {'name':'POPCAT', 'id':'145'},
        {'name':'JSOL', 'id':'145'},

    ]

    # Get Lending Pools APY
    driver = webdriver.Firefox(options=options)
    driver.get('https://app.mango.markets/')
    time.sleep(15)
    vegetables = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()
    soup = BeautifulSoup(vegetables,'html.parser')
    lending = soup.find_all(class_="border-y border-th-bkg-3 default-transition border-t-0 md:hover:cursor-pointer md:hover:bg-th-bkg-2")
    for pools in lending:
        token = pools.find(class_="font-body leading-none text-th-fgd-2")
        rate = pools.find(class_="cursor-help text-th-up")
        token_name = token.text.strip()
        for pool_token in lending_pools:
            if token_name == pool_token['name']:
                if rate:
                    float_rate = float(rate.text.strip("%"))
                    rounded_rate = round(float_rate,2)
                    cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'], rounded_rate))
                    conn.commit()
                else:
                    cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'], "0.0"))
                    conn.commit()

if __name__ == "__main__":
    mango_markets()