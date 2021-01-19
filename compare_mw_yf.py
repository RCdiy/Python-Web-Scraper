"""
Prints values from keys common to Market Watch and Yahoo Finance using a stock
not traded on the US stock exchange.
Market Watch
    symbol = 'avst'
    country = 'uk'
Yahoo Finance
    symbol = 'avst.l'
"""
import modules.web_scrapers as scrapers
scraper_mw = scrapers.equity.market_watch(random_headers=True)
scraper_yf = scrapers.equity.yahoo_finance(random_headers=True)

symbol_mw = 'ams'
country = 'es'
symbol_yf = 'ams.mc' 

stock_mw = scraper_mw.get_stock(symbol_mw,country)
stock_yf = scraper_yf.get_stock(symbol_yf)

comparison = {}

print('\n'+ __file__)

for key in stock_yf :
    try:
        yf = stock_yf[key]
        mw = stock_mw[key]
        key = key.ljust(20)
        print(key," mw : ", mw)
        key = " ".ljust(20)
        print(key," yf : ", yf)
    except:
        pass
print('')