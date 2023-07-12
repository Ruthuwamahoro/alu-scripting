#!/usr/bin/python3
"""return number of subscribes"""
import json
import sys
import urllib.request

def number_of_subscribers (subreddit):
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            subscribers = json.loads(data).get("data", 
                                               {}).get("subscribers", 0)
            return subscribers
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 0
        else:
            print("Error: ", e.code)
    except urllib.error.URLError as e:
        print("Error: ", e.reason)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subreddit = sys.argv[1]
        result = number_of_subscribers(subreddit)
        print(result)
