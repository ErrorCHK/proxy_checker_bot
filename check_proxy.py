import requests
from requests.exceptions import ProxyError,ConnectionError
from geopy.geocoders import Nominatim
from functools import partial

url = 'http://pppoker.club/poker/api/getip.php?need_gps=1' # API return IP and coordinates lat:lon



def get_check_proxy(type,proxy):
    try:
            proxies={'http':None}
        
            if 'HTTP' in type:
                proxies['http'] = 'http://'+proxy
            else:
                proxies['http'] = 'socks5h://'+proxy

        
            response = requests.get(url=url,proxies=proxies,timeout=5)
            if response.status_code == 200:
                r_json = response.json()
                clientip,lat,lon = r_json['clientip'], r_json['lat'],r_json['lon']
                geo =[i/1000000 for i in (lat,lon)] #formatting for geo
                geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)')
                country = partial(geolocator.reverse, language="es")
                result = str(country(geo)).split()[-1]
                return f'IP proxy: {clientip}🟢\nlatitude: {geo[0]}\nlongitude: {geo[1]}\nCountry: {result}',(geo[0],geo[1])
      
    except (ProxyError, ConnectionError) as var:
        return 'Proxy is dead 🆘'




