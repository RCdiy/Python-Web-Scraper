from  modules.web_scrapers import equity
scraper = equity.market_watch(random_headers=True)
stock = scraper.get_stock('aapl')

print('\n'+ __file__)

for key in stock:
	print(key.ljust(20),' : ',stock[key])
del scraper
del stock

import modules.web_scrapers as scrapers
scraper = scrapers.equity.market_watch(random_headers=True)
stock = scraper.get_stock('avst', 'uk')
print()
for key in stock:
	print(key.ljust(20),' : ',stock[key])