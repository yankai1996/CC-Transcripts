import os
import shutil
from processbar import processbar

FROM = os.path.expanduser("~/Local/SeekingAlpha/transcripts/clean/")
TO = os.path.expanduser("~/Local/SeekingAlpha/transcripts/QA/")

def cp_files():
	filenames = [f for f in os.listdir(temp) if f.endswith(".txt")]
	for filename in processbar(filenames):
		shutil.copy(FROM + filename, DIR_PATH)

def mv_files():
	filenames = [f for f in os.listdir(FROM) if f.endswith(".txt")]
	for filename in processbar(filenames):
		os.rename(FROM + filename, TO + filename)


if __name__ == "__main__":
	mv_files()
	# cp_files()
