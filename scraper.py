from details import *

import requests
import json
from datetime import datetime, timedelta
import re

bearer_token = BEARER_TOKEN

search_url = "https://api.twitter.com/2/tweets/search/recent"
historic_search_url = "https://api.twitter.com/2/tweets/search/all"



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"   #### or "v2FullArchiveSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def gettweets(timefrom):

    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query = '(#BorisJohnson OR "boris Johnson" OR "bojo") -is:retweet lang:en' ## add start time: timefrom.strftime("%Y-%m-%dT%H:%M:%SZ")
    tweet_fields = 'author_id,created_at,geo,lang' ## lang is a requirement so not necessary. 
    user_fields = 'location'
    query_params = {'query': query,'tweet.fields': tweet_fields, 'user.fields': user_fields}

    json_response = connect_to_endpoint(search_url, query_params)
    time = ""
    for tweet in json_response["data"]:
        # print(tweet.get("created_at"))
        time = tweet.get("created_at")
        break
    filename = str(re.sub("[:.]", "-", time))+".json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_response, f, ensure_ascii=False, indent=4, sort_keys=True)
    filenames = open("filenames.txt", "a") ###CAN PROBABLY NOT OPEN THE FILE EACH TIME
    filenames.write(str(filename) + "\n")


def main():

    time_str = "2020-01-01 22:00:00"
    format_str = "%Y-%m-%d %H:%M:%S"
    datetime_cur = datetime.strptime(time_str, format_str)
    gettweets(timefrom=datetime_cur)
    # while datetime_cur < datetime.now():
    #     gettweets(timefrom=datetime_cur)
    #     datetime_cur = datetime_cur + timedelta(hours=3)




if __name__ == "__main__":
    main()


##### OTHER USEFUL FUNCTIONS. 
