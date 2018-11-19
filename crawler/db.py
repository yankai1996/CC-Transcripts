# Data Layer
#

import pymysql
from datetime import datetime
from settings import db_config as config

db = pymysql.connect(
	host=	config.host, 
	port=	config.port,
	user=	config.user, 
	passwd=	config.passwd, 
	db=		config.db, 
	charset=config.charset
)

cursor = db.cursor()


# create tables if not extist in the database
def init_tables():
	cursor.execute("""
		SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'transcript'
		""")
	if cursor.fetchone()[0] != 1:
		create_table = """
			CREATE TABLE transcript (
				url VARCHAR(256) NOT NULL, 
				title VARCHAR(256) NULL , 
				pub_time VARCHAR(64) NULL , 
				company VARCHAR(128) NULL , 
				body MEDIUMTEXT NULL, 
				PRIMARY KEY (url(256))
				) 
			ENGINE = InnoDB;
		"""
		cursor.execute(create_table)
		db.commit()

	cursor.execute("""
		SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'failed_page'
		""")
	if cursor.fetchone()[0] != 1:
		create_table = """
			CREATE TABLE transcript (
				page_number INT(256) NOT NULL, 
				PRIMARY KEY (page_number(4))
				) 
			ENGINE = InnoDB;
		"""
		cursor.execute(create_table)
		db.commit()

init_tables()



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
		sql = "INSERT INTO transcript (url) VALUES ('%s')" % url
		cursor.execute(sql)
		db.commit()
		return True
	except Exception as e:
		print(str(e))
		return False

def get_uncrawled_transcript_urls(limit=1):
	try:
		sql = "SELECT url FROM transcript WHERE title = NULL ORDER BY RAND() LIMIT %s" % limit
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
		sql = """
			UPDATE transcript
			SET title = '%s', pub_time = '%s', company = '%s', body = '%s') 
			WHERE url = '%s'
		""" % (title, pub_time, company, body, url)
		cursor.execute(sql)
		db.commit()
		return True
	except Exception as e:
		print(str(e))
		return False

def get_transcripts(limit=1):
	try:
		sql = "SELECT * FROM transcript LIMIT %s" % limit
		cursor.execute(sql)
		result = cursor.fetchall()
		return list(result)
	except Exception as e:
		print(e)
		return []

# view how many transcripts have been crawled
def summary():
	try:
		sql = "SELECT COUNT(url) FROM transcript"
		cursor.execute(sql)
		total = cursor.fetchall()[0][0]

		sql = "SELECT COUNT(url) FROM transcript WHERE title <> NULL"
		cursor.execute(sql)
		crawled = cursor.fetchall()[0][0]

		sql = ("""
			SELECT
    		table_name AS `Table`,
    		round(((data_length + index_length) / 1024 / 1024), 3) `Size in MB`
			FROM information_schema.TABLES
			WHERE table_schema = 'seekingalpha'
    		AND table_name = 'transcript';
    	""")
		cursor.execute(sql)
		size = cursor.fetchall()[0][1]

		print("%d / %d Crawled, %f MB" % (crawled, total, size))
		print(datetime.now())

	except Exception as e:
		raise e

if __name__ == "__main__":
	summary()
	db.close()
