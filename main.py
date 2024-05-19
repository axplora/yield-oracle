import time 
from logbook import Logger, FileHandler
from modules import sanctum, parcl, drift, ondo_finance, mango_markets, kamino_finance, jupiter, flash_trade, solend, marginfi

log = Logger('WebScraper Logging')
FileHandler('main.log').push_application()

protocols = [
    (sanctum),
    (parcl),
    (drift),
    (jupiter),
    (ondo_finance),
    (mango_markets),
    (kamino_finance),
    (flash_trade),
    (solend),
    (marginfi),

]

while True:
  print("Starting...")

  time.sleep(5)

  for protocol in protocols:
    count = 0
    while True:
      try:
        protocol()
        log.info(f"{protocol}: SUCCESSFUL!")
        break
      except Exception as e:
        count += 1
        log.error(f"{protocol}: {e}")
        if count < 3:
          log.error(f"{protocol}: RETRYING! ({count})")
        else:
          log.error(f"{protocol}: MAX RETRIES!")
          break

  print("Shutting Down...")

  time.sleep(1800)
