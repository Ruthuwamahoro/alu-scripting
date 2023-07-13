#!/usr/bin/python3
""" a list containing the titles of all hot articles for a given subreddit"""
import json
import sys
import urllib.request


def recurse(subreddit, hot_list=[], after=None):
    if hot_list is None:
        hot_list = []
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
                hot_list.append(title)

            after = data["data"]["after"]

            if after is not None:
                return recurse(subreddit, hot_list=hot_list, after=after)
            else:
                return hot_list
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        else:
            raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subreddit = sys.argv[1]
        result = recurse(subreddit)
        if result is not None:
            print(len(result))
        else:
            print("None")
