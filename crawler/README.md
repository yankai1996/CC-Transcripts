# CC-Transcripts Crawler

## Introduction

This web crawler collects the conference call transcripts

## Usage

Before running the crawler, please customize `settings.py`

Then, 

1. Run `python3 url_crawler.py` first;
2. After some urls have been crawled, you can run `python3 transcript_crawler.py`.

There may be a few transcripts cannot be simply crawled. You may need to download them manually and use `relocation_handler.py` to parse them.
