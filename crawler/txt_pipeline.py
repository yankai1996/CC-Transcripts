# Export transcripts from database to file system
#

import os
import io
import db

DIR_PATH = os.path.expanduser("~/Downloads/transcripts/")


def main():
	for t in db.get_transcripts(160000):
		path = DIR_PATH + t[0] + ".txt"
		with io.open(path, "w", encoding="utf-8") as f:
			f.write((t[1] + "\n" + t[-1]).replace("\n", "\r\n"))
			f.close()


if __name__ == "__main__":
	main()