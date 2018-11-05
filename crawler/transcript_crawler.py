import time
import os
import io
import re
import random
from bs4 import BeautifulSoup
import grequests

import db
import myProxy
from settings import ROOT_2 as root

def crawl_transcripts(max_page=1000, batch_size=20):

	def save_transcript(html):
		try:
			soup = BeautifulSoup(html.text, "lxml")
			title = soup.find("div", {"id": "a-hd"}).find("h1").text
			pub_time = soup.find("div", {"class": "a-info"}).find("time").text

			company_ele = soup.find("span", {"id": "about_primary_stocks"}) \
				or soup.find("span", {"id": "about_stocks"}) \
				or soup.find("div", {"id": "a-body"}).find("p").find("a")
			if company_ele:
				company = company_ele.text
			else:
				company = "<None>"
			
			ps = soup.find("div", {"id": "a-body"}).find_all("p")
			body = ""
			for p in ps:
				strong = p.find("strong")
				if strong:
					p = str(p)
					body += p[p.find("<strong>"):-4] + "\n"
				else:
					body += p.text + "\n"

			url = html.url[33:]
			if db.save_transcript(url, title, pub_time, company, body):
				return db.set_crawled(url)
		except Exception as e:
			print(e)
			print(html.url)
			return False


	def exception_handler(request, exception):
		print("Request failed: ")
		print(exception)

	def batch_scrawl(number=batch_size):
		urls = db.get_uncrawled_transcript_urls(number)
		gs = (myProxy.g_get(root + url) for url in urls)
		rs = grequests.map(gs, exception_handler=exception_handler)
		return rs

	total = 0
	while max_page > 0:
		max_page -= batch_size
		count = 0
		rs = batch_scrawl()
		for html in rs:
			if html and html.status_code == 200:
				count += 1
				if save_transcript(html):
					total += 1
		# if count < batch_size/2:
		# time.sleep(5)
		print(rs)
	print(total)


if __name__ == "__main__":
   start = time.time()
	crawl_transcripts(50000, 20)
	end = time.time()
	print('Time consuming: %.3f seconds.' % (end - start))

	