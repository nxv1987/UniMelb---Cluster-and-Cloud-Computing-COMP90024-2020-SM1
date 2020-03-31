import os
import sys
from pathlib import Path
from collections import Counter

from twitter import Tweet


def read_lines(filename, start=0, end=-1):
    """
    Read (lazy) specific chunk of filename line by line
    filename: json file containing tweet data (big file)
    start: byte position to read from (defaults to start of file)
    end: byte position to read to (defaults to end of file)
    """

    if end < 0:
        end = os.path.getsize(filename)

    with open(filename, encoding="utf8") as f:
        f.seek(start)
        while f.tell() < end:
            yield f.readline()


def count_hashtags_langs(filename, start=0, end=-1):
    """
    Count hashtags and languages in specific chunk of filename
    filename: json file containing tweet data (big file)
    start: byte position to read from (defaults to start of file)
    end: byte position to read to (defaults to end of file)
    """

    hashcounts = Counter()  # hashtag counts
    langcounts = Counter()  # language counts
    for text in read_lines(filename, start, end):
        tweet = Tweet(text)
        if not tweet.data:  # badly formatted line
            continue

        hashcounts.update(tweet.hashtags)
        langcounts[tweet.lang] += 1

    return hashcounts, langcounts


def process_chunk(filename, chunks=1, number=0):
    """
    Pick and process equal-size chunk of filename according to its number
    filename: json file containing tweet data (big file)
    chunks: total number of chunks, defaults to processing entire file
    number (starting 0): current chunk number, defaults to first chunk number
    """

    size = os.path.getsize(datafile)
    start = int(number / chunks * size)  # start byte position
    end = int((number + 1) / chunks * size)  # end byte position
    hashcounts, langcounts = count_hashtags_langs(filename, start, end)

    return hashcounts, langcounts


if __name__ == "__main__":
    root = Path(sys.argv[1])  # project directory

    # Test read_lines(...)
    datafile = root / "test" / "data.txt"
    with open(datafile, 'w') as f:
        f.write("Hello World!\nHow are you today?\nThank you!")
    print(*read_lines(datafile, end=15), sep="\n")
    print(*read_lines(datafile, start=15, end=20), sep="\n")
    print(*read_lines(datafile, start=20), sep="\n")

    # Test read_lines(...) real data
    datafile = root / "data" / "tinyTwitter.json"
    lines = read_lines(datafile)
    print(next(lines))  # 1st line
    print(next(lines))  # 2nd line
    print(next(lines))  # 3rd line

    # Test count_hashtags_langs(...) w/o splitting
    hashcounts, langcounts = count_hashtags_langs(datafile)
    print(hashcounts)
    print(langcounts)

    # Test count_hashtags_langs(...) with splitting
    hashcounts1, langcounts1 = count_hashtags_langs(datafile, end=1567912)
    hashcounts2, langcounts2 = count_hashtags_langs(datafile, start=1567912, end=3135824)
    hashcounts3, langcounts3 = count_hashtags_langs(datafile, start=3135824)
    hashcounts_split = hashcounts1 + hashcounts2 + hashcounts3
    langcounts_split = langcounts1 + langcounts2 + langcounts3
    print(hashcounts_split)
    print(langcounts_split)

    # Test process_chunk(...)
    hashcounts1, langcounts1 = process_chunk(datafile, 3, 0)  # 1st chunk
    hashcounts2, langcounts2 = process_chunk(datafile, 3, 1)  # 2nd chunk
    hashcounts3, langcounts3 = process_chunk(datafile, 3, 2)  # 3rd chunk
    hashcounts_split = hashcounts1 + hashcounts2 + hashcounts3  # merge hashtag counts
    langcounts_split = langcounts1 + langcounts2 + langcounts3  # merge language counts
    print(hashcounts_split)
    print(langcounts_split)
