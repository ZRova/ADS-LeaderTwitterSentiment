from details import *

import requests
import json
from datetime import datetime, timedelta
import re
import time

# bearer_token = BEARER_TOKEN
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
        print(response.status_code, response.text)
        time.sleep(15*60) #Wait until you can again!
        response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def gettweets(timefrom):
    print(timefrom)
    format_str = "%Y-%m-%dT%H:%M:%SZ"
    string_time = datetime.strftime(timefrom, format_str)
    string_endtime = datetime.strftime((timefrom + timedelta(hours=2, minutes=59, seconds=59)), format_str)
    #SHOULD WE INCLUDE has:geo OR place_country:GB. Would severely limit responses.
    query_params = {'query': "(#BorisJohnson OR Boris Johnson OR bojo OR boris -yeltsin) -is:retweet lang:en -has:media", 
                    'start_time': string_time, 
                    'end_time':string_endtime, 
                    'max_results':20, 
                    'tweet.fields': 'author_id,created_at,geo',  #,public_metrics,context_annotations' ## lang is a requirement so not necessary. #Should entities be included?
                    'user.fields': 'username,location',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type'}

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
    test_stop_time ="2021-01-15 00:00:00"
    format_str = "%Y-%m-%d %H:%M:%S"
    datetime_cur = datetime.strptime(time_str, format_str)
    datetime_stop = datetime.strptime(test_stop_time, format_str) 
    # gettweets(timefrom=datetime_cur)
    while datetime_cur < datetime_stop: #### datetime.now():   ####TESTING ONLY FOR FIRST 15 DAYS TO SEE HOW IT HANDLES API CALLS
        gettweets(timefrom=datetime_cur)
        datetime_cur = datetime_cur + timedelta(hours=3)
        print(datetime_cur)
    print("stopped at" + str(datetime.strptime(time_str, format_str)))


if __name__ == "__main__":
    main()


##### OTHER USEFUL FUNCTIONS. 
