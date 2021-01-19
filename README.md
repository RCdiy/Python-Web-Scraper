# Python Web Scrapers

* This module scrapes websites for data.
* A delay between scrapping the same URL is used to reduce server load.
* Random headers are used to reduce the likelihood of being blocked.

# Equity (Stocks)
## Market Watch
https://www.marketwatch.com
```python
from  modules.web_scrapers import equity
scraper = equity.market_watch(random_headers=True)
stock = scraper.get_stock('aapl')
for key in stock:
	print(key.ljust(20),' : ',stock[key])

import modules.web_scrapers as scrapers
scraper = scrapers.equity.market_watch(random_headers=True)
```
## Yahoo Finance
https://ca.finance.yahoo.com
```python
from  modules.web_scrapers import equity
scraper = equity.yahoo_finance(random_headers=True)
stock = scraper.get_stock('aapl')
for key in stock:
	print(key.ljust(20),' : ',stock[key])

import modules.web_scrapers as scrapers
scraper = scrapers.equity.yahoo_finance(random_headers=True)
```

---
**Not being maintained**
* This code is unlikely to be maintained.
* If you send in a pull request it is unlikely I will look at it.
* If you create an issue it is unlikely I will look at it.

**Using & Forking**
* You may use this code or fork it without crediting me.
