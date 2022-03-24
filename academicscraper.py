from details import *

import requests
import json
from datetime import datetime, timedelta
import re
import time

########## NOTES
# this code will retrieve 10 tweets every 3 hours from the start date(2020/01/01) to the end date(2022/03/20). 
# change the query!!!!! 
# if you aren't getting enough country tagged data, you may have to remove that tag/live with less data 
# getting less data at 3am is normal. look at daytime values and see whether they are larger. since it is sampling 8x per day they add up.  
# you can also set it to retrieve less often, up to 1300 seconds it should get the same amount of data but print less often? Do check that

#change this to however you access the token
academic_bearer_token = ACADEMIC_BEARER_TOKEN

academic_search_url = "https://api.twitter.com/2/tweets/search/all"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {academic_bearer_token}" #KEEP THE f
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    while response.status_code == 429:          ### In case of too many requests error
        print(response.status_code, response.text.title)
        time.sleep(10)                          ### Wait until you can again! 
        response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def gettweets(timefrom):
    format_str = "%Y-%m-%dT%H:%M:%SZ"
    string_time = datetime.strftime(timefrom, format_str)
    string_endtime = datetime.strftime((timefrom + timedelta(hours=3)), format_str)
    
    query_params = {'query': "(#BorisJohnson OR Boris Johnson OR bojo OR (boris -yeltsin -becker -karloff)) -is:retweet lang:en -has:media place_country:GB", #SHOULD WE INCLUDE has:geo OR place_country:GB. Would severely limit responses.
                    'start_time': string_time, 
                    'end_time':string_endtime, 
                    'max_results':10, 
                    'expansions': "geo.place_id",                                               #'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'author_id,created_at,geo,lang,in_reply_to_user_id,public_metrics,context_annotations,entities',  #'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',#,public_metrics,context_annotations' ## lang is a requirement so not necessary. #Should entities be included?
                    'user.fields': 'name,username,location,verified',                                         #'id,name,username,created_at,description,public_metrics,verified'
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type'}

    json_response = connect_to_endpoint(academic_search_url, query_params)
    filename = re.sub("[:.]", "-", string_endtime)+".json"
    folder = "academicJsons3\\"
    with open(folder + filename, 'w', encoding='utf-8') as f:
        json.dump(json_response, f, ensure_ascii=False, indent=4, sort_keys=True)
    filenames = open("academic_filenames3.txt", "a") ###CAN PROBABLY NOT OPEN THE FILE EACH TIME
    filenames.write(str(filename) + "\n")
    resultcount = json_response["meta"]["result_count"]
    return(resultcount)


def main():
    tweet_count = 0
    time_str = "2021-08-02 21:00:00" #MAKE SURE TO RESET THIS EACH TIME YOU STOP START THE CODE. First start on 2020-01-01 00:00:00
    test_stop_time ="2022-03-20 00:00:00"
    format_str = "%Y-%m-%d %H:%M:%S"
    datetime_cur = datetime.strptime(time_str, format_str)
    datetime_stop = datetime.strptime(test_stop_time, format_str) 
    while datetime_cur < datetime_stop: 
        newtweets = gettweets(timefrom=datetime_cur)
        datetime_cur = datetime_cur + timedelta(hours=3)
        tweet_count += newtweets
        print("total collected=",tweet_count,"new=",newtweets, "date=", datetime_cur, " retrieved at", datetime.strftime(datetime.now(), format_str))
    print("stopped at" + str(datetime.strptime(time_str, format_str)))


if __name__ == "__main__":
    main()


##### OTHER USEFUL FUNCTIONS. 
