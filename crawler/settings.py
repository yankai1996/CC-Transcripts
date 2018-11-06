# Global settings
# Please custom the following variables according to your own use
#

# database configuration
class DBConfig(object):
	def __init__(self):
		self.host = 'localhost', 
		self.port = 3306,
		self.user = 'root', 
		self.passwd = 'admin@0225', 
		self.db = 'seekingalpha', 
		self.charset = 'utf8'
		
db_config = DBConfig()


# Mogu proxy configuration
# http://www.moguproxy.com/
class MoguConfig(object):
	def __init__(self):
		self.appKey = "U1BpNGxpMVZjbDcxNjJPeDpIaDhFYkdoem9HR2tvdW5n"
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
	username = "HY939725721Z1ZYD",
	password = "83A19E7CB307DE92")


# Luminati proxy configuration 
# https://luminati-china.io/
luminati_config = ProxyConfig(
	host = "zproxy.lum-superproxy.io",
	port = 22225,
	# username = "lum-customer-hl_68fc3a66-zone-zone1",
	# password = "kty7qy02zrrn")
	username = "lum-customer-hl_68fc3a66-zone-zone2",
	password = "3ljrgdqhlp73")

# SeekingAlpha address
ROOT_1 = "https://seekingalpha.com/earnings/earnings-call-transcripts/"
ROOT_2 = "https://seekingalpha.com/article/"
