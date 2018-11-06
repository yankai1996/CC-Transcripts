# CC-Transcripts Cleaner

These programs clean the raw transcripts and preprocess them to build the input dataset.

As required by Dr. Gu, the data is organized using file system. You might need to define your own file paths in each program. You need to change the regex to cover all the cases. You may also need to manually handel some transcripts.

## Basic Usage

### Step 1

1. There are a few advertisements mixed in the transcripts. Manually detect them and use `remove_ads.py` to remove them.

2. Use `extract_ticker.py` to create `info` files and save the extractred tickers in them.

3. Use `extract_time.py` to get the call date and time and append them in `info` files.

4. Use `divide.py` to divide the transcripts to Presentation and QA.

5. Use `remove_prologue.py` to remove the name lists at the beginning of Presentation.

6. Use `remove_operator.py` to remove the subtitles.

### Step 2

7. Use `count_words.py` to extract textual infomation from the transcritps and save to `info` files.

8. Use `integrate.py` to integrate all the `info` files and build the final table.
