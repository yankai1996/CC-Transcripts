# Proxies that send request and return the webpage
#

import grequests
import requests
import random
from settings import mogu_config, abuyun_config, luminati_config


USER_AGENTS = [
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

REFERER = [
	'http://www.google.com/',
	'http://www.google.com/',
	'http://www.google.com/',
	'http://www.baidu.com/',
	"http://seekingalpha.com"
]

HEADERS = {
	'Accept': '*/*',
	'Accept-Language': 'en-US,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
	'Connection': 'keep-alive',
	'Referer': 'http://www.google.com/'
}

class FailResponse(object):
	def __init__(self, status_code=502):
		self.status_code = status_code


def random_header():
	return {
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.8',
		'Cache-Control': 'max-age=0',
		'User-Agent': random.choice(USER_AGENTS),
		'Connection': 'keep-alive',
		'Referer': random.choice(REFERER)
	}



def get(url):
	return get_by_mogu(url)
	# return get_by_abuyun(url)
	# return get_by_luminati(url)


def g_get(url):
	return get_by_mogu(url, g=True)
	# return get_by_abuyun(url, g=True)
	# return get_by_luminati(url, g=True)


def g_get_by_proxy(url, proxies, headers=random_header()):
	return grequests.get(url,
		headers=headers,
		proxies=proxies,
		verify=False,
		allow_redirects=False, 
		timeout=15)


def get_by_proxy(url, proxies, headers=HEADERS):
	try_count = 5
	r = FailResponse()
	while r.status_code != 200 and try_count > 0:
		try:
			r = requests.get(url, headers=headers, proxies=proxies, verify=False, allow_redirects=False, timeout=15)
			if r.status_code == 302 or r.status_code == 301:
			    url_f = url + r.headers['Location']
			    r = requests.get(url_f, headers=headers, proxies=proxies, verify=False, allow_redirects=False, timeout=15)	
		except Exception as e:
			r = FailResponse()
			print(str(e))
		try_count -= 1

	return r

def get_by_mogu(url, g=False):
	proxies = {"http": "http://" + mogu_config.ip_port, "https": "https://" + mogu_config.ip_port}
	headers = random_header()
	headers["Proxy-Authorization"] = 'Basic '+ mogu_config.appKey

	if g:
		return g_get_by_proxy(url, proxies, headers=headers)
	return get_by_proxy(url, proxies, headers=headers)


def _get_by_auth_proxy(url, config, g=False):
	proxyHttp = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : config.host,
      "port" : config.port,
      "user" : config.username,
      "pass" : config.password,
    }
	proxyHttps = "https://%(user)s:%(pass)s@%(host)s:%(port)s" % {
	  "host" : config.host,
	  "port" : config.port,
	  "user" : config.username,
	  "pass" : config.password
	}
	proxies = {
	    "http"  : proxyHttp,
	    "https" : proxyHttps
	}
	if g:
		return g_get_by_proxy(url, proxies)
	return get_by_proxy(url, proxies)

def get_by_abuyun(url, g=False):
	return _get_by_auth_proxy(url, abuyun_config, g=g)


def get_by_luminati(url, g=False):
	return _get_by_auth_proxy(url, luminati_config, g)




