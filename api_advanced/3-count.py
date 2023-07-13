#!/usr/bin/python3
"""parses the title of all hot articles"""
import json
import sys
import urllib.request
from collections import Counter


def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = Counter()

    if after is None:
        url = "https://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    else:
        url = "https://www.reddit.com/r/{}/hot.json?limit=100&after={}".format(subreddit, after)

    headers = {"User-Agent": "Mozilla/5.0"}

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            posts = data["data"]["children"]

            for post in posts:
                title = post["data"]["title"]
                title_words = title.lower().split()
                counts.update(title_words)

            after = data["data"]["after"]

            if after is not None:
                return count_words(subreddit, word_list, after=after, counts=counts)
            else:
                sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
                for word in word_list:
                    count = next((count for keyword, count in sorted_counts if keyword ==
		    word.lower()), 0)
                    if count > 0:
                    	print("{}: {}".format(word.lower(),count))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        else:
            raise


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2:]
        count_words(subreddit, word_list)
