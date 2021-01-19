from  modules.web_scrapers import equity
scraper = equity.yahoo_finance(random_headers=True)
stock = scraper.get_stock('aapl')

print('\n'+ __file__)

for key in stock:
	print(key.ljust(30),' : ',stock[key])
del scraper
del stock

import modules.web_scrapers as scrapers
scraper = scrapers.equity.yahoo_finance(random_headers=True)
stock = scraper.get_stock('avst.l')
print()
for key in stock:
	print(key.ljust(30),' : ',stock[key])