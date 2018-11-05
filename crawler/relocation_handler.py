# Handle the manually downloaded webpage.html
#

from bs4 import BeautifulSoup
import os
import db

def save_transcript(html, url):
	try:
		soup = BeautifulSoup(html, "lxml")
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
				body += str(strong) + "\n"
			else:
				body += p.text.replace("\\'","'") + "\n"

		if db.save_transcript(url, title, pub_time, company, body):
			return db.set_crawled(url)
	except Exception as e:
		print(e)
		return False
	

def main():
	for filename in os.listdir("./html"):
		with open("./html/" + filename, "r") as f:
			save_transcript(f.read(), filename[:-5])

if __name__ == "__main__":
    main()