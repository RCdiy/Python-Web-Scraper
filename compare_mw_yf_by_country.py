from  modules.web_scrapers import equity
mw = equity.market_watch
from  modules.web_scrapers import equity
yf = equity.yahoo_finance

countries = {
    'US':{'mw':'abc', 'yf':'abc'},
    'CA':{'mw':'abx', 'yf':'abx.to'},
    'UK':{'mw':'abc', 'yf':'abc.l'},
    'DE':{'mw':'aba', 'yf':'aba.f'},
    'ES':{'mw':'ams', 'yf':'ams.mc'},
    'FR':{'mw':'air', 'yf':'air.pa'},
    'IT':{'mw':'atl', 'yf':'atl.mi'},
    'NL':{'mw':'abn', 'yf':'abn.as'},
    'NO':{'mw':'ade', 'yf':'ade.ol'},
    'SE':{'mw':'abb', 'yf':'abb.st'},
    'CH':{'mw':'ams', 'yf':'ams.sw'},
    'ZA':{'mw':'abg', 'yf':'abg.jo'},
    'HK':{'mw':'1234', 'yf':'1234.hk'},
    'JP':{'mw':'4321', 'yf':'4321.t'},
    'AU':{'mw':'anz', 'yf':'anz.ax'},
    'NZ':{'mw':'anz', 'yf':'anz.nz'}
    }

print('\n'+ __file__)

for c in countries:
    if True:
        s_mw = countries[c]['mw']
        s_yf = countries[c]['yf']
        stock_mw = mw(random_headers=True).get_stock(s_mw,c)
        stock_yf = yf(random_headers=True).get_stock(s_yf)

        p_mw = stock_mw['price']
        cu_mw = stock_mw['currency']
        time_mw = stock_mw['price_time_iso']  
        t_mw = time_mw[:-6] + ' ' + time_mw[-6:] 
        e_mw = stock_mw['exchange']
        n_mw = stock_mw['name']

        p_yf = stock_yf['price']
        cu_yf = stock_yf['currency']
        time_yf = stock_yf['price_time_iso']
        t_yf = time_yf[:-6] + ' ' + time_yf[-6:]
        e_yf = stock_yf['exchange']
        n_yf = stock_yf['name']

        print(c + ' : ' + s_mw.ljust(7) + p_mw.rjust(10) + cu_mw.center(5) + t_mw + '  ' + e_mw.ljust(32) + ' ' + n_mw )
        print(c + ' : ' + s_yf.ljust(7) + p_yf.rjust(10) + cu_yf.center(5) + t_yf + '  ' + e_yf.ljust(32) + ' ' + n_yf )
        print('')


print('')