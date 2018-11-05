import time
import random
from bs4 import BeautifulSoup
import db
import myProxy
import requests
from settings import ROOT_1 as root

def random_sleep():
	time.sleep(random.randint(5,11))


def scrawl_urls(max_page=5000):

	def save_urls(html, check_dup=False):
		soup = BeautifulSoup(html.text, "lxml")
		count = 0
		if not check_dup:
			for li in soup.find_all("li", class_="list-group-item article"):
				url = li.find("a")['href'][9:]
				db.save_transcript_url(url)
		else:
			for li in soup.find_all("li", class_="list-group-item article"):
				url = li.find("a")['href'][9:]
				saved = db.save_transcript_url(url)
				if saved:
					count += 1
				else:
					return count
		return count

	
	last_failed_pages = db.get_failed_pages()

	count = 0
	for i in range(1, max_page):
		url = root + str(i)
		page_html = myProxy.get(url)
		code = page_html.status_code
		if code == 200:
			number = save_urls(page_html, True)
			count += number
			if number < 30:
				break
		print(code)


	for i in last_failed_pages:
		j = str(int(i) + count//30)
		url = root + j
		page_html = myProxy.get(url) # config in myProxy
		code = page_html.status_code
		db.delete_failed_page(i)
		if code == 200:
			save_urls(page_html)
		else:
			db.add_failed_page(j)
		print(code)

	if count % 30 != 0:
		for i in last_failed_pages:
			j = str(int(i) + 1 + count//30)
			url = root + j
			page_html = myProxy.get(url) # config in myProxy
			code = page_html.status_code
			if code == 200:
				save_urls(page_html, True)
			else:
				db.add_failed_page(j)
			print(code)


	i = int(last_failed_pages[-1]) + count//30
	while i < max_page:
		i += 1
		url = root + str(i)
		page_html = myProxy.get(url) # config in my Proxy
		code = page_html.status_code
		if code == 200:
			save_urls(page_html)
		else:
			db.add_failed_page(i)
		print(code)

	db.add_failed_page(max_page+1)




def main():
	start = time.time()
	scrawl_urls(5119)
	end = time.time()
	print('Time consuming: %.3f seconds.' % (end - start))


if __name__ == "__main__":
    main()

