from selenium import webdriver
from bs4 import BeautifulSoup 
from selenium.webdriver.firefox.options import Options
from lxml import etree 
import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def kamino_finance():
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

    # Links to all lending pools on kamino
    lending_pools = [

        {'name':'jlp_usdc', 'id':'1', 'link':'https://app.kamino.finance/lending/reserve/DxXdAyU3kCjnyggvHmY5nAwg5cRbbmdyX3npfDMjjMek/Ga4rZytCpq1unD4DbEJ5bkHeUz9g3oh9AAFEi6vSauXp'},
        {'name':'jlp_jlp', 'id':'2', 'link':'https://app.kamino.finance/lending/reserve/DxXdAyU3kCjnyggvHmY5nAwg5cRbbmdyX3npfDMjjMek/DdTmCCjv7zHRD1hJv3E8bpnSEQBzdKkzB1j9ApXX5QoP'},
        {'name':'main_sol', 'id':'3', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/d4A2prbA2whesmvHaL88BH6Ewn5N4bTSU2Ze8P6Bc4Q'},
        {'name':'main_usdc', 'id':'4', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/D6q6wuQSrifJKZYpR1M8R4YawnLDtDsMmWM1NbBmgJ59'},
        {'name':'main_jitosol', 'id':'5', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/EVbyPKrHG6WBfm4dLxLMJpUDY43cCAcHSpV3KYjKsktW'},
        {'name':'main_bsol', 'id':'6', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/H9vmCVd77N1HZa36eBn3UnftYmg4vQzPfm1RxabHAMER'},
        {'name':'main_msol', 'id':'7', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/FBSyPnxtHKLBZ4UeeUyAnbtFuAmTHLtso9YtsqRDRWpM'},
        {'name':'main_usdt', 'id':'8', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/H3t6qZ1JkguCNTi9uzVKqQ7dvt2cum4XiXWom6Gn5e5S'},
        {'name':'main_jlp', 'id':'9', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/EAA3VVsxUuQB1Tm5x7TJkq9ATtiX5Qwq8ok7gXwim7oo'},
        {'name':'main_jup', 'id':'10', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/4AFAGAm5G8fkcKy7QerL88E7BiSE22ZRbvJzvaKjayor'},
        {'name':'main_jto', 'id':'11', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/9Ukd2MSw5RvVFaN8jLhWxjHLEGiF1F6Hf7v3Zq5hZsKB'},
        {'name':'main_eth', 'id':'12', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/febGYTnFX4GbSGoFHFeJXUHgNaK53fB23uDins9Jp1E'},
        {'name':'main_tbtc', 'id':'13', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/Hcz1o77tF9TpdEHcvrx29tz7SBKoQEwJA1wuJqGZYnTw'},
        {'name':'main_uxd', 'id':'14', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/GhGPbkWmPjSkbkgZbhNGBTxzwQKjqDpZwNfaf2gQKgdG'},
        {'name':'main_usdh', 'id':'15', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/DaGyAQJrdkLCzYZiUWg49NV8vabDnhR7ETwLu5eQgL56'},
        {'name':'main_kbsolsol', 'id':'16', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/57U9pEC8NsWvHgWywd2xHTRkGQzWWYsWivxYRhtxZrLB'},
        {'name':'main_kjitosolsol', 'id':'17', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/75WrtSz7rLCdBvAQhtHi8M2jC8HnpT8iUxcYkdeawr37'},
        {'name':'main_kmsolsol', 'id':'18', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/FPAwg5jadDs8AvUtvtAbit2RCZdkZES6yY5X6nCSuEw9'},
        {'name':'main_kuxdusdc', 'id':'19', 'link':'https://app.kamino.finance/lending/reserve/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/AxuWrPrJfwrUTvCWRxpkSQct6q8k1YSJzxhyYw2AAmv2'},
        {'name':'alt_usdc', 'id':'20', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/9TD2TSv4pENb8VwfbVYg25jvym7HN6iuAR6pFNSrKjqQ'},
        {'name':'alt_wif', 'id':'21', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/GvPEtF7MsZceLbrrjprfcKN9quJ7EW221c4H9TVuWQUo'},
        {'name':'alt_bonk', 'id':'22', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/CoFdsnQeCUyJefhKK6GQaAPT9PEx8Xcs2jejtp9jgn38'},
        {'name':'alt_wen', 'id':'23', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/G6wtWpanuKmtqqjkpHpLsp21d7DKJpWQydKojGs2kuHQ'},
        {'name':'alt_pyth', 'id':'24', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/HXSE82voKcf8x2rdeLr73yASNhzWWGcTz3Shq6UFaEHA'},
        {'name':'alt_jup', 'id':'25', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/3AKyRviT87dt9jP3RHpfFjxmSVNbR68Wx7UejnUyaSFH'},
        {'name':'alt_usdh', 'id':'26', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/G9T3ajJ5NL4m5v3bbu5KuSmVojWgaMGufDorLAHgJuYE'},
        {'name':'alt_jto', 'id':'27', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/8PYYKF4ZvteefFBmtb9SMHmhZKnDWQH86z59mPZBfhHu'},
        {'name':'alt_inf', 'id':'141', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/Hy2S5arXGFgsvze47PCgSjF92ZQCiAfUJnFkqZQMXu4T'},
        {'name':'alt_w', 'id':'142', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/Dd7KhG2zJbrEDCq1rJJWg9mcDSfrdt3ExtzcA12zy1f9'},
        {'name':'alt_tnsr', 'id':'143', 'link':'https://app.kamino.finance/lending/reserve/ByYiZxp8QrdN9qbdtaAiePN8AAr3qvTPppNJDpf5DVJ5/E9Y7wNfjcHVhukm7tmqSke5DUhea5Rkq5oXhXFmcJ9GB'},

    ]

    for elemnts in lending_pools:
        retries = 0
        while True:
            try:
                driver = webdriver.Firefox(options=options)
                driver.get(elemnts['link'])
                time.sleep(15)
                vegetables = driver.execute_script('return document.documentElement.outerHTML')
                driver.quit()
                soup = BeautifulSoup(vegetables,'html.parser')
                blended_soup = etree.HTML(str(soup)) 
                rate = blended_soup.xpath('//*[@id="BACKGROUND_OVERRIDE"]/div/div[1]/div[3]/div[3]/p[2]')[0].text
                float_rate = float(rate.strip("%"))
                rounded_rate = round(float_rate,2)
                cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (elemnts['id'], rounded_rate))
                conn.commit()
                break
            except:
                retries = retries + 1
                if retries == 3:
                    print(f"{elemnts['name']} max retries, going next!") 
                else:
                    print(f"{elemnts['name']} failed, retrying!")

if __name__ == "__main__":
    kamino_finance()