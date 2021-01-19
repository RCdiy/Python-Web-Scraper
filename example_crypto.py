from  modules.web_scrapers import crypto
scraper = crypto.business_insider(random_headers=True)
crypto = scraper.get_crypto('btc-usd')

print('\n'+ __file__)

for key in crypto:
	print(key.ljust(15),' : ',crypto[key])
del scraper
del crypto

import modules.web_scrapers as scrapers
scraper = scrapers.crypto.business_insider()
crypto = scraper.get_crypto('eth-usd')
print()
for key in crypto:
	print(key.ljust(15),' : ',crypto[key])