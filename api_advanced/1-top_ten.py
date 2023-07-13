#!/usr/bin/python3
"""print the titles of the first 10 host posts"""
import argparse
import json
import urllib.request


def top_ten(subreddit):
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    requesting = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(requesting) as response:
            data = json.loads(response.read().decode('utf-8'))
            posts = data["data"]["children"]

            for post in posts:
                title = post["data"]["title"]
                print(title.encode('unicode_escape').decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("None")
        else:
            raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get top 10 hot posts from a subreddit")
    parser.add_argument("subreddit", type=str, help="Name of the subreddit")
    args = parser.parse_args()

    top_ten(args.subreddit)
