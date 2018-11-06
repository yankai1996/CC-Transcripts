# Global settings
# Please custom the following variables according to your own use
#

# database configuration
class DBConfig(object):
	def __init__(self):
		self.host = 'localhost', 
		self.port = 3306,
		self.user = 'root', 
		self.passwd = '', 
		self.db = 'seekingalpha', 
		self.charset = 'utf8'
		
db_config = DBConfig()


# Mogu proxy configuration
# http://www.moguproxy.com/
class MoguConfig(object):
	def __init__(self):
		self.appKey = ""
		self.ip_port = 'transfer.mogumiao.com:9001'

mogu_config = MoguConfig()


class ProxyConfig(object):
	def __init__(self, host, port, username, password):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		

# Abuyun proxy configuration
# https://www.abuyun.com/
abuyun_config = ProxyConfig(
	host = "http-dyn.abuyun.com",
	port = 9020,
	username = "",
	password = "")


# Luminati proxy configuration 
# https://luminati-china.io/
luminati_config = ProxyConfig(
	host = "zproxy.lum-superproxy.io",
	port = 22225,
	username = "",
	password = "")

# SeekingAlpha address
ROOT_1 = "https://seekingalpha.com/earnings/earnings-call-transcripts/"
ROOT_2 = "https://seekingalpha.com/article/"
