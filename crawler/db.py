import pymysql
from datetime import datetime
from settings import db_config

db = pymysql.connect(
	host=db_config.host, 
	port=db_config.port,
	user=db_config.user, 
	passwd=db_config.passwd, 
	db=db_config.db, 
	charset=db_config.charset
)

cursor = db.cursor()


def add_failed_page(page_number):
	try:
		sql = "INSERT INTO FAILED_PAGE (PAGE_NUMBER) VALUES (%s)" % page_number
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		print(str(e))
		db.rollback()

def delete_failed_page(page_number):
	try:
		sql = "DELETE FROM FAILED_PAGE WHERE PAGE_NUMBER = '%s'" % page_number
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		print(str(e))
		db.rollback()

def get_failed_pages():
	try:
		sql = "SELECT page_number FROM failed_page"
		cursor.execute(sql)
		result = cursor.fetchall()
		return [str(row[0]) for row in result]
	except Exception as e:
		print(str(e))
		return []

def save_transcript_url(url, crawled=0):
	try:
		sql = "INSERT INTO transcript_url (url, crawled) VALUES ('%s', %s)" % (url, crawled)
		cursor.execute(sql)
		db.commit()
		return True
	except Exception as e:
		print(str(e))
		return False

def get_uncrawled_transcript_urls(limit=1):
	try:
		sql = "SELECT url FROM transcript_url WHERE crawled = '0' ORDER BY RAND() LIMIT %s" % limit
		cursor.execute(sql)
		result = cursor.fetchall()
		return [str(row[0]) for row in result]
	except Exception as e:
		print(str(e))
		return []

def save_transcript(url, title, pub_time, company, body):
	try:
		title = title.replace("'","''")
		pub_time = pub_time.replace("'","''")
		company = company.replace("'", "''")
		body = body.replace("'", "''")
		sql = (
			"INSERT INTO transcript "
			"(url, title, pub_time, company, body) "
			"VALUES ('%s', '%s', '%s', '%s', '%s')"
		) % (url, title, pub_time, company, body)
		cursor.execute(sql)
		db.commit()

		update = "UPDATE transcript_url SET crawled = 1 WHERE url = '%s'" % url
		cursor.execute(update)
		db.commit()
		return True
	except Exception as e:
		print(str(e))
		return False

def set_crawled(url):
	try:
		sql = "UPDATE transcript_url SET crawled = 1 WHERE url = '%s'" % url
		cursor.execute(sql)
		db.commit()
		return True
	except Exception as e:
		print(str(e))
		return False

def summary():
	try:
		sql = "SELECT COUNT(url) FROM transcript_url"
		cursor.execute(sql)
		total = cursor.fetchall()[0][0]

		sql = "SELECT COUNT(url) FROM transcript_url WHERE crawled = 1"
		cursor.execute(sql)
		crawled = cursor.fetchall()[0][0]

		print(str(crawled) + " / " + str(total) + " Crawled")

		sql = "SELECT COUNT(url) FROM transcript"
		cursor.execute(sql)
		transcripts = cursor.fetchall()[0][0]

		sql = (
			"SELECT "
    		"table_name AS `Table`, "
    		"round(((data_length + index_length) / 1024 / 1024), 3) `Size in MB` "
			"FROM information_schema.TABLES "
			"WHERE table_schema = 'seekingalpha' "
    		"AND table_name = 'transcript';"
    	)
		cursor.execute(sql)
		size = cursor.fetchall()[0][1]

		print(str(transcripts) + " records, " + str(size)+ " MB.")
		print(datetime.now())

	except Exception as e:
		raise e

if __name__ == "__main__":
	summary()
	db.close()
