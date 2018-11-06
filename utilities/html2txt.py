import os
from bs4 import BeautifulSoup

def get_content(html):
	try:
		soup = BeautifulSoup(html, "lxml")
		title = soup.find("div", {"id": "a-hd"}).find("h1").text
		
		ps = soup.find("div", {"id": "a-body"}).find_all("p")
		body = ""
		for p in ps:
			strong = p.find("strong")
			if strong:
				p = str(p)
				body += p[p.find("<strong>"):-4] + "\r\n"
			else:
				body += p.text + "\r\n"

		return title + "\r\n" + body
	except Exception as e:
		print(e)
		return None

def main():
	FROM = os.path.expanduser("~/Downloads/transcripts/html/")
	TO = os.path.expanduser("~/Downloads/transcripts/")

	for filename in [f for f in os.listdir(FROM) if f.endswith(".html")]:
		with open(FROM + filename, 'r') as html:
			content = get_content(html.read())
			with open(TO + filename[:-4] + "txt", 'w', encoding="utf8") as f:
				f.write(content)
				f.close()
			html.close()

if __name__ == "__main__":
	main()