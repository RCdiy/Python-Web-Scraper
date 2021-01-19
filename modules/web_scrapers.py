class _print:
	def __init__(self):
		pass

	def _abc(dictionary,indent=''):
			print(indent,type(dictionary), end='')
			for key in dictionary:
				space = indent + ' '
				print('\n',space, key, end='')
				space += ' '
				if type(dictionary[key]) == dict:
					_print._abc(dictionary=dictionary[key],indent=space)
				else:
					print('\n', space, dictionary[key])
	


	def _indented(*args,indent=''):
		print('web_scrapers', end='')
		space = indent + ' '
		for arg in args:
			space = space + ' '
			if type(arg) == dict:
				_print._abc(dictionary=arg,indent=space)
			else:
				print(':\n',space, arg, end='')
		print('\n')
			# if type(message) == dict:
			# 	print()
			# 	self._dictionary(message, indent=space)
			# else:
			# 	print(':\n',indent, message, end='')


class timer:
	"""
	A timer that can be used to determin elapsed time.
		timer(duration_seconds:float)

		Example:
			from modules.web_scrapers import timer
			x = timer(2)
			x.start()
			print('Timer started :', x.started())
			x.wait(1)
			print('Time elapsed: ', x.elapsed())
			print('Time remaining: ', x.remaining())
			print('The timer is done (maybe):', x.done())
			print('Waiting till done.')
			x.wait_till_done()
			print('Timer done:', x.done())

			import modules.web_scrapers as scrapers
			x = scrapers.timer(2)
	"""
	from datetime import datetime
	from datetime import timezone
	from time import sleep
	_utc = timezone.utc
	_timer = datetime
	
	def __init__(self, duration_seconds:float):
		self._timer_start_time = None
		self.duration_seconds = duration_seconds

	def current_time(self) -> datetime:
		"""
		Returns the current time as a datetime object.
		"""
		return self._timer.now(self._utc)

	def current_time_posix(self) -> float:
		"""
		Returns the current POSIX time seconds.
		"""
		return self.current_time().timestamp()

	def current_time_iso(self) -> str:
		"""
		Returns the current time is ISO format.
		2021-00-11-14:30-05:00
		"""
		return self.current_time().replace(microsecond=0).isoformat(' ')

	def start_time(self) -> datetime:
		"""
		Returns the timer start time as a datetime object.
		"""
		return self.timer_start_time

	def start_time_posix(self) -> float:
		"""
		Returns the timer start time in POSIX time seconds.
		"""
		return self.start_time().timestamp()

	def start_time_iso(self) -> str:
		"""
		Returns the timer start time in an ISO format.
		2021-00-11-14:30-05:00
		"""
		return self.start_time().replace(microsecond=0).isoformat(' ')

	def started(self) -> bool:
		"""
		Returns True or False. True is start has been called.
		"""
		if self.start_time() == None:
			return False
		return True

	def start(self, duration_seconds:float=None) -> None:
		"""
		Sets the timer to zero.
		"""
		self.timer_start_time = self.current_time()
		if duration_seconds != None:
			self.duration_seconds = duration_seconds
		if self.duration_seconds == None:
			_print._indented( 'class timer', 'start()','Warning: A count down duration has not been set.')

	def elapsed_seconds(self) -> float:
		"""
		Seconds since last reset.
		"""
		return self.current_time_posix() -  self.start_time_posix()

	def remaining_seconds(self) -> float:
		"""
		Seconds remaining. A negative number is seconds past timer end.
		"""
		return self.duration_seconds - self.elapsed_seconds()

	def wait(self, seconds:float) -> None:
		"""
		Waits the duration provided.
		"""
		self.sleep(seconds)

	def wait_till_done(self) -> None:
		"""
		Waits till the count down reaches zero.
		"""
		self.wait(self.remaining_seconds())

	def check_done(self) -> bool:
		"""
		Checks if the count down has reached zero.
		"""
		if self.remaining_seconds() > 0:
			return False
		else:
			self.started_utc_now = None
			return True


class _web:
	import requests
	def __init__(self, random_headers:bool=True, time_out:tuple=(10,10), url_update_interval:float=60):
		"""
		Time out (x,y):
			x - seconds to wait for a response.
			y - seconds to wait for the content.
		"""
		self.use_random_headers = random_headers
		self.time_out = time_out
		self.url_update_interval = url_update_interval
		self.urltimers = {}

		self.timer = timer(url_update_interval)

		self.previous_user_agent_index = 0
		self.user_agents = [
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
			"Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
			"Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
			"Mozilla/5.0 (X11; CrOS x86_64 13310.93.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.133 Safari/537.36",
			]
		self.header = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Encoding": "gzip, deflate",
			"Accept-Language": "en-ca",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
			}

	def _get_random_user_agent(self) -> str:
		"""
		Returns a random user agent.
		"""
		num = self.timer.current_time_posix()
		num = int( ( num - int(num) ) * 10**6 )

		idx = num % len(self.user_agents)
		if idx == self.previous_user_agent_index :
			idx = (num + 1) % len(self.user_agents)
			self.previous_user_agent_index = idx

		return self.user_agents[idx]

	def _get_header(self) -> dict:
		"""
		Returns a header with a random user agent.
		"""
		if self.use_random_headers:
			self.header["User-Agent"] = self._get_random_user_agent()
		return self.header

	def _get_website(self, url:str, header:dict=None) -> str:
		'''
		Returns the contents website.
		If the url update interval has not been completed 'None' is returned.
		'''
		# Don't access website too often
		if self.urltimers.get(url) == None:
			self.urltimers[url] = timer(self.url_update_interval)
		else:
			if not self.urltimers[url].check_done():
				# _print._indented('class _web', '_get_website('+url+', '+str(type(header))+')', 
				# 	'if not self.urltimers[url].check_done()')
				return None

		# Asign header
		if header == None:
			header =self._get_header()
	
		try:
			website = self.requests.get( url, timeout=self.time_out, headers=header)
		except:
			_print._indented('class _web', '_get_website('+url+', '+type(header)+')', 
				'website = self.requests.get('+url+', '+str(self.time_out)+','+type(header)+')')
			return None

		if not website.ok:
			_print._indented('class _web', '_get_website('+url+', '+ str(type(header))+')','not website.ok',website.text[:200])

		self.urltimers[url].start()

		return str(website.text)


class equity:
	from datetime import datetime
	from datetime import timezone
	import html

	class market_watch:
		"""
		Stock data scrapped from MarketWatch.
			market_watch(random_headers:bool=True, update_delay_seconds:int=60)

			Values:
				name                   :  tesla inc.
				symbol                 :  tsla
				currency               :  usd
				price                  :  702.00
				price_change           :  7.22
				price_change_percent   :  1.04%
				price_time_iso         :  2020-12-31-10:24-05:00
				exchange               :  nasdaq

				parsely-tags           :  pagetype: quotes, us:tsla, stock, us: u.s.: nasdaq, nas, page-overview
				chartingsymbol         :  stock/us/xnas/tsla
				instrumenttype         :  stock
				exchangecountry        :  us
				exchangeiso            :  xnas

			Example:
				from  modules.web_scrapers import equity
				scraper = equity.market_watch(random_headers=True)
				stock = scraper.get_stock('aapl')
				for key in stock:
					print(key.ljust(20),' : ',stock[key])
				del scraper
				del stock

				import modules.web_scrapers as scrapers
				scraper = scrapers.equity.market_watch(random_headers=True)
				stock = scraper.get_stock('avst', 'uk')
				for key in stock:
					print(key.ljust(20),' : ',stock[key])
		"""

		def __init__(self, random_headers:bool=True, update_delay_seconds:int=60):
			"""
			Use Market Watch to get stock information.
				When random_headers is True a header is chosen randomly and used with each website access.

				To reduce load on the website server update_delay_seconds prevents access using the
				same  symbol if the specified number of seconds has not elapsed since the last access.
			"""
			web = _web(random_headers=random_headers,  url_update_interval=update_delay_seconds)
			self.get_website = web._get_website

			self.url = 'https://www.marketwatch.com/investing/stock/'
			self.stock_list = {}

		def get_stock(self, symbol:str, country:str=None, header:dict=None) -> dict:
			"""
			Get the latest information on the stock symbol string.
				The optional country code defaults to US.
					CA, AU, FR, DE, HK, IT, JP, NL, NZ, NO, ZA, ES, SE, CH, UK

				Returns a dictionatry with keys:
					parsely-tags, chartingsymbol, instrumenttype, exchangecountry, exchangeiso,
					quotetime, name, symbol, currency, price, price_change, price_change_percent,
					price_time_iso, exchange

					Optional:
						Uses the supplied browser header.
						If a header is not provided then a random one gets used.

				Example:
					from  modules.web_scrapers import equity
					scraper = equity.market_watch(random_headers=True)
					stock = scraper.get_stock('aapl')
					for key in stock:
						print(key.ljust(20),' : ',stock[key])

					import modules.web_scrapers as scrapers
					scraper = scrapers.equity.market_watch(random_headers=True)
			"""
			symbol = symbol.casefold()
			if country != None:
				country = country.casefold()
			ticker_symbol = symbol

			url = self.url + symbol

			if country != None:
				url= url + '?countrycode=' + country


			# Website text
			html = self.get_website(url, header=header)
			if html == None:
				if self.stock_list[url] != None:
					return self.stock_list[url]
				else:
					_print._indented('class equity', 'market_watch', 'get_stock(' + symbol + ', ' + country + ', ' + str(type(header)+')',
					'html = self.get_website(' + url + ',' + 'header=' + str(type(header)) + ').casefold()',
					'if html == None:') )
				return None
			html = html.casefold()
			# Start parsing
			data_string = html[ html.find('<meta name=\"parsely-tags\"') : ]
			data_string = data_string[ : data_string.find('<meta name=\"description\"') ]

			lines = data_string.split('<meta name=')

			stock = {}
			for line in lines:
				if line != '':
					data = line.split('\"')
					key = data[1]
					value =  data[3].replace('&#x9;', '') # remove the tab
					value = equity.html.unescape(value)
					stock[key] = value

			# Test we have the expected keys
			if stock.get('tickersymbol') == None:
				_print._indented('market_watch', str('get_stock(' + symbol + ', ' + country + ', ' + str(type(header)) + ')'), 
				'stock.get(\'tickersymbol\') == None' )
				return None
			elif stock['tickersymbol'] != symbol:
				_print._indented('market_watch', str('get_stock(' + symbol + ', ' + country + ', ' + str(type(header)) + ')'), 
					'elif stock[\'tickersymbol\'] = ' + stock['tickersymbol'] + '!= '+symbol)
				return None

			# Price
			# Stock price with only digits and a period
			price =stock.pop('price')
			try:
				x = float(price)
			except:
				for c in range(0,len(price)):
					if not price[0].isdigit():
						price = price[1:]
					if not price[-1].isdigit():
						price = price[:-1]
				price = price.replace(',','')
			
			# ISO Date Time Format
			# From:
			# 	jan 12, 2021 4:35 p.m. gmt
			# 	(utc+00:00) dublin, edinburgh, lisbon, london
			# To:
			# 	2021-01-12-16:35-05:00
			tz = stock.pop('exchangetimezone')
			tz = tz.split('(')[1].split(')')[0][-6:]

			qt = stock['quotetime']
			qt = qt[:qt.find('.m.')] + 'm '
			qt = qt + tz

			time_iso = equity.datetime.strptime(qt, '%b %d, %Y %I:%M %p %z')
			time_iso = str(time_iso.replace(microsecond=0).astimezone(equity.timezone.utc).isoformat(' '))

			# Matching keys with data from other sources
			stock['name']=stock.pop('name')
			stock['symbol']=stock.pop('tickersymbol')
			stock['currency']=stock.pop('pricecurrency')
			stock['price'] = price
			stock['price_change']=stock.pop('pricechange')
			stock['price_change_percent']=stock.pop('pricechangepercent')
			stock['exchange'] = stock.pop('exchange')
			stock['price_time_iso'] = time_iso
			stock['quotetime'] = stock.pop('quotetime')
			self.stock_list[url] = stock
			return stock


	class yahoo_finance:
		"""
		Stock data scrapped from Yahoo Finance
			yahoo_finance(random_headers:bool=True, update_delay_seconds:int=60)

			Values:
				name                             :  tesla, inc.
				symbol                           :  tsla
				currency                         :  usd
				price                            :  701.20
				price_change                     :  6.42
				price_change_percent             :  0.92%
				price_time_iso                   :  2020-12-31-10:33-05:00
				exchange                         :  nasdaqgs

				sourceinterval                   :  15
				quotesourcename                  :  nasdaq real time price
				regularmarketopen                :  {'raw': 699.99, 'fmt': '699.99'}
				regularmarkettime                :  {'raw': 1609428782, 'fmt': '10:33am est'}
				fiftytwoweekrange                :  {'raw': '70.102 - 703.7399', 'fmt': '70.10 - 703.74'}
				sharesoutstanding                :  {'raw': 947900992, 'fmt': '947.901m', 'longfmt': '947,900,992'}
				regularmarketdayhigh             :  {'raw': 703.7399, 'fmt': '703.74'}
				longname                         :  tesla, inc.
				exchangetimezonename             :  america\u002fnew_york
				regularmarketpreviousclose       :  {'raw': 694.78, 'fmt': '694.78'}
				fiftytwoweekhighchange           :  {'raw': -2.539917, 'fmt': '-2.54'}
				exchangetimezoneshortname        :  est
				fiftytwoweeklowchange            :  {'raw': 631.098, 'fmt': '631.10'}
				exchangedatadelayedby            :  0
				regularmarketdaylow              :  {'raw': 691.13, 'fmt': '691.13'}
				pricehint                        :  2
				regularmarketvolume              :  {'raw': 11294432, 'fmt': '11.294m', 'longfmt': '11,294,432'}
				isloading                        :  False
				triggerable                      :  True
				firsttradedatemilliseconds       :  1277818200000
				region                           :  ca
				marketstate                      :  regular
				marketcap                        :  {'raw': 664668209152, 'fmt': '664.668b', 'longfmt': '664,668,209,152'}
				quotetype                        :  equity
				invalid                          :  False
				language                         :  en-ca
				fiftytwoweeklowchangepercent     :  {'raw': 9.002568, 'fmt': '900.26%'}
				regularmarketdayrange            :  {'raw': '691.13 - 703.7399', 'fmt': '691.13 - 703.74'}
				messageboardid                   :  finmb_27444752
				fiftytwoweekhigh                 :  {'raw': 703.7399, 'fmt': '703.74'}
				fiftytwoweekhighchangepercent    :  {'raw': -0.00360917, 'fmt': '-0.36%'}
				uuid                             :  ec367bc4-f92c-397c-ac81-bf7b43cffaf7
				market                           :  us_market
				fiftytwoweeklow                  :  {'raw': 70.102, 'fmt': '70.10'}
				tradeable                        :  False

			Example:
				from  modules.web_scrapers import equity
				scraper = equity.yahoo_finance(random_headers=True)
				stock = scraper.get_stock('aapl')
				for key in stock:
					print(key.ljust(20),' : ',stock[key])
				del scraper
				del stock

				import modules.web_scrapers as scrapers
				scraper = scrapers.equity.yahoo_finance(random_headers=True)
		"""

		def __init__(self,random_headers:bool=True, update_delay_seconds:int=60):
			"""
			Use Yahoo Finance to get stock information.
				When random_headers is True a header is chosen randomly and used with each website access.

				To reduce load on the website server update_delay_seconds prevents access using the
				same  symbol if the specified number of seconds has not elapsed since the last access.
			"""
			web = _web(random_headers=random_headers, url_update_interval=update_delay_seconds)
			self.get_website = web._get_website

			self.host = 'ca.finance.yahoo.com'
			self.url1 = 'https://' + self.host + '/quote/'
			self.url2 = '/sustainability?p='

			self.time_out = (2,4)

			from json import loads
			self.loads = loads

			self.stock_list = {}
			
		def get_stock(self, symbol:str, header:dict=None) -> dict :
			"""
			Get the latest information on the stock symbol string.
				Returns a dictionatry with keys:
					name,		symbol, 	currency, exchange,
					price, 	price_change,		price_change_percent, price_time_iso,

					regularmarketpreviousclose : {'raw':, 'fmt':},
					regularmarketopen : {'raw':, 'fmt':},
					regularmarketdaylow : {'raw':, 'fmt':},
					regularmarketdayhigh : {'raw':, 'fmt':},
					regularmarketdayrange : {'raw':, 'fmt':},
					regularmarketvolume : {'raw':, 'fmt':},
					regularmarkettime : {'raw':, 'fmt':},

					fiftytwoweekrange : {'raw':, 'fmt':},
					fiftytwoweeklow : {'raw':, 'fmt':},
					fiftytwoweeklowchange : {'raw':, 'fmt':},
					fiftytwoweeklowchangepercent : {'raw':, 'fmt':},
					fiftytwoweekhigh : {'raw':, 'fmt':},
					fiftytwoweekhighchange : {'raw':, 'fmt':},
					fiftytwoweekhighchangepercent : {'raw':, 'fmt':},

					sharesoutstanding : {'raw':, 'fmt':},
					marketcap : {'raw':, 'fmt':},
					sourceinterval,
					quotesourcename,
					sharesoutstanding,
					longname,
					exchangetimezonename,
					exchangetimezoneshortname,
					exchangedatadelayedby,
					pricehint,
					isloading,
					triggerable,
					firsttradedatemilliseconds,
					region,
					marketstate,
					marketcap,
					quotetype,	invalid,
					language,
					messageboardid,
					uuid,
					market,
					tradeable

				Optional:
					Uses the supplied browser header.
					If a header is not provided then a random one gets used.

					Example:
						import yahoo_finance as yf
						yf.yahoo_finance().get_stock('tsla')
						yf.yahoo_finance().get_stock('avst.l')
			"""
			symbol = symbol.casefold()
			ticker_symbol = symbol

			url = self.url1 + ticker_symbol + self.url2 + ticker_symbol

			# Website html
			html = self.get_website(url, header=header).casefold()
			
			if html == None:
				if self.stock_list[url] != None:
					return self.stock_list[url]
				else:
					_print._indented('class equity', 'yahoo_finance', 'get_stock(' + symbol + ', ' + str(type(header) + ')',
					'html = self.get_website(' + url + ',' + 'header=' + str(type(header)) + ').casefold()',
					'if html == None:') )
				return None

			data_string1 = html[ html.find('\"quotedata\":{'): ]
			data_string2 = data_string1[:data_string1.find(',\"mktmdata\"')]

			dic_str = data_string2[data_string2.find('{'):]

			try:
				stock = self.loads(dic_str)
			except:
				_print._indented('yahoo_finance', 'get_stock(' + symbol + ', ' +str(type(header)) + ')', 
					'try','stock = self.loads(dic_str)', 'data_string1', data_string1, 'data_string2', data_string2, 
					'dic_str', dic_str, 'html[:100]', html[:100])
				return None
			del html
			del dic_str
			# Test we have the expected keys
			if stock.get(symbol) == None:
				_print._indented('yahoo_finance', 'get_stock('+symbol+', '+str(type(header))+')', 
					'stock.get(\''+symbol+'\') == None', stock)
				return None
			elif stock[symbol]['symbol'] != symbol:
				_print._indented('yahoo_finance', 'get_stock('+symbol+', '+str(type(header))+')', 
					'elif stock[symbol][\'symbol\'] != symbol:', stock[symbol]['symbol']+' != '+symbol)
				return None

			stock = stock[symbol]

			# ISO Format
			# 2020-12-30-16:00-05:00
			lt = int( stock['regularmarkettime']['raw'] )
			dt_iso = equity.datetime.fromtimestamp(lt,tz=equity.timezone.utc).isoformat(' ')

			# Matching keys with data from other sources
			stock['name']=stock.pop('shortname')
			stock['symbol']=stock.pop('symbol')
			stock['currency']=stock.pop('currency')
			stock['price']=str(stock.pop('regularmarketprice')['raw'])
			stock['price_change']=stock.pop('regularmarketchange')['fmt']
			stock['price_change_percent']=stock.pop('regularmarketchangepercent')['fmt']
			stock.pop('exchange')
			stock['exchange'] = stock.pop('fullexchangename')
			stock['price_time_iso'] = dt_iso
			stock['regularmarkettime'] = stock.pop('regularmarkettime')
			self.stock_list[url] = stock
			return stock


class crypto:
	class business_insider:
		"""
		Cryptocurrency scraped from Business Insider.
			business_insider(random_headers:bool=True, update_delay_seconds:int=60)

			Dictionary keys:
				name             :  bitcoin
				price            :  38966.5195
				change           :  -412.53
				change_percent   :  -1.05
				market_cap       :  704230000000
				circulating      :  18072712
				volume           :  18880000000
				utc_iso          :  2021-01-08-18:02:20.067122+00:00

			Example:
				from  modules.web_scrapers import crypto
				scraper = crypto.business_insider(random_headers=True)
				crypto = scraper.get_crypto('btc-usd')
				for key in crypto:
					print(key.ljust(15),' : ',crypto[key])

				import modules.web_scrapers as scrapers
				scraper = scrapers.crypto.business_insider()
		"""
		def __init__(self,random_headers:bool=True, update_delay_seconds:int=60):
			"""
			Use Market Watch to get stock information.
			When random_headers is True a header is chosen randomly and used with each website access.

			To reduce load on the website server update_delay_seconds prevents access using the
			same  symbol if the specified number of seconds has not elapsed since the last access.
			"""

			self.web = _web(random_headers=random_headers, url_update_interval=update_delay_seconds)
			self.get_website = self.web._get_website

			# https://markets.businessinsider.com/cryptocurrencies
			# https://markets.businessinsider.com/currencies/btc-usd
			self.url_crypto_list = 'https://markets.businessinsider.com/cryptocurrencies'
			self.time_out = (4,4)
			self.crypto_value_sections_list = []
			self.values_dict = { 'symbol':0, 'name':1 , 'price':4, 'change':7,
													'change_percent':10, 'market_cap':11, 'circulating':12, 
													'volume':13, 'utc_iso':-1 
												}
			self.most_active_cryptos = {}
			self.most_active_cryptos_limit = 100
			self.timer = timer(update_delay_seconds)
			self.update_delay_seconds = update_delay_seconds

		def _parse_value(self,section_index:int) -> str:
			if section_index == -1: # utc_iso key
				return self.timer.start_time_iso()

			value_section = self.crypto_value_sections_list[section_index]
			value_list = value_section.split('<')
			value = value_list[0]
			del value_list

			if section_index == self.values_dict['symbol']:
				symbol_section_list = value.split('\"')
				symbol_link = symbol_section_list[1]
				del symbol_section_list

				symbol_link_sections = symbol_link.split('/')

				return symbol_link_sections[2]


			if section_index > self.values_dict['name']:
				if value[-1] == 'b':
					return str( int(float(value[:-1]) * 10**9) )

				if value[-1] == 'm':
					return str( float(value[:-1]) * 10**6 )

			return value

		def get_most_active_cryptos(self, limit:int, header:dict=None, show_warnings:bool=False) -> dict:
			"""
			Get the latest information on the most active cryptocuttencies.

				Returns a dictionatry with keys:
					'name' : {'symbol': , 'price':, 'change':, 'change_percent':, 'market_cap':,
											'circulating':, 'volume':}

					'bitcoin' : {'symbol':'tbc-usd', price':'34164.5391', 'change':'2105.41',
											'change_percent':'6.57', 'market_cap':'617450000000',
											'circulating':'18072712', 'volume':'18880000000'}

					Optional:
						Uses the supplied browser header.

				Example:
					from  modules.web_scrapers import crypto
					scraper = crypto.business_insider(random_headers=True)
					crypto = scraper.get_crypto('btc-usd')
					for key in crypto:
						print(key.ljust(15),' : ',crypto[key])

					import modules.web_scrapers as scrapers
					scraper = scrapers.crypto.business_insider()
					crypto = scraper.get_crypto('eth-usd')
			"""
			self.most_active_cryptos_limit = limit
			html = self.get_website(self.url_crypto_list, header=header)

			if html == None:
				return self.most_active_cryptos

			self.timer.start()
			html = html.casefold()

			# Get cryptos section
			html_sections_list = html.split('<tbody class="table__tbody">')
			del html
			if show_warnings:
				if len(html_sections_list) != 4:
					_print._indented('crypto', 'business_insider', 'get_most_active_cryptos('+str(limit)+', '+type(header)+', '+ str(show_warnings)+')',
						'HTML sections warning', 'Website data not as expected.',
						'4 sections expected, have ',len(html_sections_list))

			cryptos_section = html_sections_list[1]
			del html_sections_list
			cryptos_section = cryptos_section.replace(',','').replace(' %','')

			# Get crypto sections
			crypto_sections_list = cryptos_section.split('<a')
			del cryptos_section

			number_crypto_sections = len(crypto_sections_list) - 1
			if number_crypto_sections < limit:
				limit = number_crypto_sections
			limit +=1

			# Get crypto sections symbols, values
			for crypto_section in crypto_sections_list[1:limit]:

				self.crypto_value_sections_list = crypto_section.split('">')

				if show_warnings :
					if len(self.crypto_value_sections_list) != 18:
						_print._indented('\nValues sections warning:\n\tWebsite data not as expected.')
						_print._indented('\t18 sections expected, have ',len(self.crypto_value_sections_list))

				for key in self.values_dict:
					if key == 'symbol':
						symbol = self._parse_value(self.values_dict[key] )
						self.most_active_cryptos[symbol] = {}
					else:
						self.most_active_cryptos[symbol][key] = self._parse_value(self.values_dict[key] )

			return self.most_active_cryptos

		def find_symbol_for(self,limit:int, name:str) -> list:
			"""
			Returns a list of symbols from the last most active crypto currency data set
			that match in part or whole the name supplied.
			"""
			self.most_active_cryptos_limit = limit
			self.most_active_cryptos = self.get_most_active_cryptos(self.most_active_cryptos_limit)

			list = []
			for symbol in self.most_active_cryptos :
				crypto_name = self.most_active_cryptos[symbol]['name']
				if crypto_name.find(name) >= 0:
					list.append((symbol, crypto_name))
			return list

		def get_price_for(self,symbol:str) -> str:
			"""
			Returns the price as a string.
			"""
			self.most_active_cryptos = self.get_most_active_cryptos(self.most_active_cryptos_limit)

			return self.most_active_cryptos[symbol]['price']

		def get_crypto(self,symbol:str) -> dict:
			"""
			Returns the dictionary of a crypto symbol.
			"""
			self.most_active_cryptos = self.get_most_active_cryptos(self.most_active_cryptos_limit)

			return self.most_active_cryptos[symbol]


# timer and web
if __name__ == '__main__' :
	print('\ntimer and web')
	print('=============')
	# input('Press enter to continue.')

	w = _web(random_headers=True, url_update_interval=3)
	x = timer(5)
	print('Getting a website:\n',w._get_website('http://httpbin.org/headers') )
	x.start()
	print('Timer started :', x.started())
	x.wait(1)
	print('Time elapsed: ', x.elapsed_seconds())
	print('\nGetting the website again:',w._get_website('http://httpbin.org/headers') )
	print('\nTime remaining: ', x.remaining_seconds())
	print('The timer is done (maybe):', x.check_done())
	print('Waiting till done.')
	x.wait_till_done()
	print('Timer done:', x.check_done())
	print('Lets try getting the website again:\n',w._get_website('http://httpbin.org/headers') )
	print('Timer started at: ', x.start_time_iso())
	print('Current time:     ', x.current_time_iso())
	print('POSIX time:       ', x.current_time_posix())

# market_watch
if __name__ == '__main__' :
	print('\nmarket_watch')
	print('============')
	# input('Press enter to continue.')

	def example(symbol,country=None,random_headers=False):
		"""
		Prints all the available dictionary keys.

		Run from the command line:
				python3 yahoo_finance.py

		"""

		if random_headers:
			site = equity.market_watch(random_headers=True)
		else:
			site = equity.market_watch()
		stock = site.get_stock(symbol,country)
		print()
		for key in stock :
			pad=''
			for x in range(0,20-len(key)):
				pad = pad + ' '
			print(key, pad, ' : ', stock[key])
		print()

	print("\nexample('avst', 'uk', random_headers=False)")
	print('------------------------------------------')
	example('avst', 'uk', random_headers=False)

	print("\nexample('aapl',random_headers=True)")
	print('-----------------------------------')
	example('aapl',random_headers=True)

# yahoo_finance
if __name__ == '__main__' :
	print('\nyahoo_finance')
	print('=============')
	# input('Press enter to continue.')

	def example(symbol,random_headers=False):
		"""
		Prints all the available dictionary keys.

		Run from the command line:
				python3 yahoo_finance.py

		"""
		if random_headers:
			site = equity.yahoo_finance(random_headers=True)
		else:
			site = equity.yahoo_finance()
		stock = site.get_stock(symbol)
		print()
		for key in stock :
			pad=''
			for x in range(0,20-len(key)):
				pad = pad + ' '
			print(key, pad, ' : ', stock[key])
		print()

	print("\nexample('avst.l', random_headers=False)")
	print('--------------------------------------')
	example('avst.l', random_headers=False)

	print("\nexample('aapl',random_headers=True)")
	print('-----------------------------------')
	example('aapl',random_headers=True)

# business_insider
if __name__ == '__main__' :
	print('\nbusiness_insider')
	print('================')
	# input('Press enter to continue.')

	def example(limit:int, random_headers=False, find:str=None):
		"""
		Prints all the available dictionary keys.

		Run from the command line:
				python3 crypto.py

		"""
		print()
		print('Example limit: '+ str(limit))
		if random_headers:
			source = crypto.business_insider(random_headers=True)
		else:
			source = crypto.business_insider()

		cryptos = source.get_most_active_cryptos(limit=limit)

		if find != None:
			found = source.find_symbol_for(limit,find)

		for key in cryptos:
			cryptos[key]['name'] = cryptos[key]['name'].ljust(20)
			cryptos[key]['price'] = cryptos[key]['price'].rjust(10)
			cryptos[key]['change'] = cryptos[key]['change'].rjust(8)
			cryptos[key]['change_percent'] = cryptos[key]['change_percent'].rjust(8)
			cryptos[key]['market_cap'] = cryptos[key]['market_cap'].rjust(12)
			cryptos[key]['circulating'] = cryptos[key]['circulating'].rjust(12)
			cryptos[key]['volume'] = cryptos[key]['volume'].rjust(12)

			print(key.rjust(10)+' :',cryptos[key])

		if find != None:
				first_symbol = found[0][0].strip()
				print('\nSearched for: '+find+'\nFound: ',found)
				print('First symbol found is ' + first_symbol + ' for ' + found[0][1].strip() +'.')
				print('The price is $',source.get_price_for(first_symbol))
		print()
		print('Note: In this example the fields have been padded with spaces.')
		print('      The actual data does not have padding.')
		print()

	print("\nexample(4,random_headers=True)")
	print('------------------------------')
	example(4,random_headers=True)

	print("\nexample(limit=4,find='it',random_headers=True))")
	print('-----------------------------------------------')
	example(limit=4,find='it',random_headers=True)