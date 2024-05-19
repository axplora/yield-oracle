from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup 
import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def drift():
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

        {'name':'USDC', 'id':'28'},
        {'name':'SOL', 'id':'29'},
        {'name':'mSOL', 'id':'30'},
        {'name':'wBTC', 'id':'31'},
        {'name':'wETH', 'id':'32'},
        {'name':'USDT', 'id':'33'},
        {'name':'jitoSOL', 'id':'34'},
        {'name':'PYTH', 'id':'35'},
        {'name':'bSOL', 'id':'36'},
        {'name':'JTO', 'id':'37'},
        {'name':'WIF', 'id':'38'},
        {'name':'JUP', 'id':'39'},
        {'name':'RNDR', 'id':'40'},
        {'name':'W', 'id':'139'},
        {'name':'TNSR', 'id':'140'}
    ]

    insurance_pools = [

        {'name':'USDC', 'id':'41'},
        {'name':'SOL', 'id':'42'},
        {'name':'jitoSOL', 'id':'43'},
        {'name':'mSOL', 'id':'44'},
        {'name':'USDT', 'id':'45'},
        {'name':'bSOL', 'id':'46'},
        {'name':'PYTH', 'id':'47'},
        {'name':'JUP', 'id':'48'},
        {'name':'WIF', 'id':'49'},
        {'name':'JTO', 'id':'50'},
        {'name':'wETH', 'id':'51'},
        {'name':'wBTC', 'id':'52'},
        {'name':'RNDR', 'id':'136'},
        {'name':'W', 'id':'138'},
        {'name':'TNSR', 'id':'137'}

    ]

    # Get Lending Pools APY
    driver = webdriver.Firefox(options=options)
    driver.get('https://app.drift.trade/earn/lend-borrow/deposits')
    time.sleep(15)
    vegetables = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()
    soup = BeautifulSoup(vegetables,'html.parser')

    lending = soup.find_all(class_="bg-container-bg hover:bg-container-bg-hover py-2 css-yv7tq1 ej8o9vq1")

    for pools in lending:
        token = pools.find(class_="font-[300] text-[13px] leading-[16px] mt-0.5 text-text-emphasis")
        pre_rate = pools.find(class_="w-full flex flex-row py-2 px-1 items-center font-numeral text-text-default")
        rate = pre_rate.find(class_="whitespace-nowrap")
        pre_float_rate = rate.text.strip("%")
        float_rate = float(pre_float_rate)
        rounded_rate = round(float_rate,2)
        token_name = token.text.strip()
        for pool_token in lending_pools:
            if token_name == pool_token['name']:
                cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'],rounded_rate))
                conn.commit()

    # RNDR for some reason doesnt have the same class name...

    rndr_lending = soup.find(class_="bg-container-bg hover:bg-container-bg-hover py-2 css-1irn7ra ej8o9vq1")
    token = rndr_lending.find(class_="font-[300] text-[13px] leading-[16px] mt-0.5 text-text-emphasis")
    pre_rate = rndr_lending.find(class_="w-full flex flex-row py-2 px-1 items-center font-numeral text-text-default")
    rate = pre_rate.find(class_="whitespace-nowrap")
    pre_float_rate = rate.text.strip("%")
    float_rate = float(pre_float_rate)
    rounded_rate = round(float_rate,2)
    token_name = token.text.strip()
    for pool_token in lending_pools:
        if token_name == pool_token['name']:
            cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'], rounded_rate))
            conn.commit()
    
    # --------------------------


    # Get Insurance Funds APR
    driver = webdriver.Chrome(options=options)
    driver.get('https://app.drift.trade/earn/stake')
    time.sleep(15)
    vegetables = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()
    soup = BeautifulSoup(vegetables,'html.parser')

    insurance = soup.find_all(class_="bg-container-bg hover:bg-container-bg-hover py-2 css-1e30a66 ej8o9vq1")

    for pools in insurance:
        token = pools.find(class_="font-[300] text-[13px] leading-[16px] mt-0.5 text-text-emphasis")
        rate = pools.find(class_="font-[300] text-[13px] leading-[16px]")
        pre_float_rate = rate.text.strip()
        if pre_float_rate == "<0.01%":
            rounded_rate == "0.00"
        else:
            float_rate = float(pre_float_rate.strip("%"))
            rounded_rate = round(float_rate,2)
        token_name = token.text.strip()
        for pool_token in insurance_pools:
            if token_name == pool_token['name']:
                cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'], rounded_rate))
                conn.commit()

    # RNDR for some reason doesnt have the same class name...

    #rndr_insurance = soup.find(class_="bg-container-bg hover:bg-container-bg-hover py-2 css-1aab9ph ej8o9vq1")
    #token = rndr_insurance.find(class_="font-[300] text-[13px] leading-[16px] mt-0.5 text-text-emphasis")
    #rate = rndr_insurance.find(class_="font-[300] text-[13px] leading-[16px]")
    #pre_float_rate = rate.text.strip()
    #if pre_float_rate == "<0.01%":
    #    rounded_rate == "0.00"
    #else:
    #    float_rate = float(pre_float_rate.strip("%"))
    #    rounded_rate = round(float_rate,2)
    #token_name = token.text.strip()
    #for pool_token in insurance_pools:
    #    if token_name == pool_token['name']:
    #        cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (pool_token['id'], rounded_rate))
    #        conn.commit()

if __name__ == "__main__":
    drift()