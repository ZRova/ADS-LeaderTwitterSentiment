from details import *

import requests
import json
from datetime import datetime, timedelta
import re
import time

bearer_token = BEARER_TOKEN
academic_bearer_token = ACADEMIC_BEARER_TOKEN

# search_url = "https://api.twitter.com/2/tweets/search/recent"
academic_search_url = "https://api.twitter.com/2/tweets/search/all"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {academic_bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code == 429: ###TRYING TO GET TOO MANY WITHIN 15 MINS
        print("Pause, too many needed")
        time.sleep(15*60) #Wait until you can again!
        response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def gettweets(timefrom):
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    # adding OR entity:"Boris Johnson" to query fills it with news articles rather than opinions
    query = '(#BorisJohnson OR Boris Johnson OR bojo OR boris -yeltsin) -is:retweet lang:en -has:media start_time: ' + str(timefrom.strftime("%Y-%m-%dT%H:%M:%SZ")) ## add max_results:50 start time: timefrom.strftime("%Y-%m-%dT%H:%M:%SZ") 
    print(query)
    #SHOULD WE INCLUDE has:geo OR place_country:GB. Would severely limit responses.
    tweet_fields = 'author_id,created_at,geo,public_metrics,context_annotations' ## lang is a requirement so not necessary. #Should entities be included?
    user_fields = 'username,location'
    query_params = {'query': query,'tweet.fields': tweet_fields, 'user.fields': user_fields}

    json_response = connect_to_endpoint(academic_search_url, query_params)
    time = ""
    for tweet in json_response["data"]:
        # print(tweet.get("created_at"))
        time = tweet.get("created_at") #TIME OF MOST RECENT TWEET
        break
    filename = str(re.sub("[:.]", "-", str(time)))+".json"
    folder = "academicJsons\\"
    with open(folder + filename, 'w', encoding='utf-8') as f:
        json.dump(json_response, f, ensure_ascii=False, indent=4, sort_keys=True)
    filenames = open("filenames.txt", "a") ###CAN PROBABLY NOT OPEN THE FILE EACH TIME
    filenames.write(str(filename) + "\n")


def main():

    time_str = "2020-01-01 00:00:00"
    test_stop_time ="2020-01-15 00:00:00"
    format_str = "%Y-%m-%d %H:%M:%S"
    datetime_cur = datetime.strptime(time_str, format_str)
    datetime_stop = datetime.strptime(test_stop_time, format_str)
    # gettweets(timefrom=datetime_cur)
    while datetime_cur < datetime_stop: #### datetime.now():
        gettweets(timefrom=datetime_cur)
        datetime_cur = datetime_cur + timedelta(hours=3)
        print(datetime_cur)
    print("stopped at" + str(datetime.strptime(time_str, format_str)))


if __name__ == "__main__":
    main()


##### OTHER USEFUL FUNCTIONS. 
