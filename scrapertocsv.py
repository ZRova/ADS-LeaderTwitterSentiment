from details import *

import requests
from datetime import datetime, timedelta
import time
import csv

########## NOTES
# this code will retrieve 10 tweets every 3 hours from the start date(2020/01/01) to the end date(2022/03/20). 
# it then puts them in a csv     !!!!!!DO NOT OPEN THE CSV OR IT WILL CRASH!!!!
# change the query!!!!! 
# if you aren't getting enough country tagged data, you may have to remove that tag/live with less data 
# getting less data at 3am is normal. look at daytime values and see whether they are larger. since it is sampling 8x per day they add up.  
# you can also set it to retrieve less often, up to 1300 seconds it should get the same amount of data but print less often? Do check that
# if you're saving the jsons, set up a folder for storage and change the folder name variable. 
# also name your filename storage something sensible if you're doing that
# Change the start date each time you start the program
# and hash out the part that adds the headers, you only want those once. 

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
        print(response.status_code, response.text)
        time.sleep(5)                          ### Wait until you can again! 
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
                    'max_results':100, 
                    'expansions': "geo.place_id",                                               #'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'author_id,created_at,geo,lang,in_reply_to_user_id,public_metrics,context_annotations,entities',  #'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',#,public_metrics,context_annotations' ## lang is a requirement so not necessary. #Should entities be included?
                    'user.fields': 'name,username,location,verified',                                         #'id,name,username,created_at,description,public_metrics,verified'
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type'}

    json_response = connect_to_endpoint(academic_search_url, query_params)

    ### UNHASH THIS PART IF YOU WOULD LIKE TO KEEP THE json FILES AS WELL AS THE CSV. 
    # filename = re.sub("[:.]", "-", string_endtime)+".json"
    # folder = "academicJsons3\\"
    # with open(folder + filename, 'w', encoding='utf-8') as f:
    #     json.dump(json_response, f, ensure_ascii=False, indent=4, sort_keys=True)
    # filenames = open("academic_filenames3.txt", "a") ###CAN PROBABLY NOT OPEN THE FILE EACH TIME
    # filenames.write(str(filename) + "\n")
    return(json_response) 

def append_to_csv(json_data, csvFileName):

    #Open OR create the target CSV file
    csvFile = open(csvFileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet_no in range(json_data['meta']["result_count"]):
        tweet = json_data["data"][tweet_no]
        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        format_str = "%Y-%m-%dT%H:%M:%S.000Z"
        created_at = datetime.strptime(tweet["created_at"], format_str)

        # 3. Tweet text
        text = tweet['text']

        # 4. Geolocation 
        # complicated as it removes doubled up locations, so you need to matche them back up using id's 
        # should be in all tweets
        if ('geo' in tweet): 
            tweet_geo = ""
            locations_tot = len(json_data["includes"]["places"])
            for location in range(tweet_no+1):
                location = min(locations_tot-1, tweet_no) - location
                if tweet["geo"]["place_id"] == json_data["includes"]["places"][location]["id"]:
                    tweet_geo = json_data["includes"]["places"][location]
                    break

            geo = tweet['geo']['place_id']
            country = tweet_geo["country_code"]
            place_full_name = tweet_geo["full_name"]
            place_name = tweet_geo["name"]
            bbox = tweet_geo["geo"]["bbox"]
            place_type = tweet_geo["place_type"]
        else:
            geo = ""
            country = ""
            place_full_name = ""
            place_name = ""
            bbox = ""
            place_type = ""
        
        # 5. Tweet ID
        tweet_id = tweet['id'] 

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        # 7. Context annotations
        if "context_annotations" in tweet:
            context = tweet["context_annotations"]
        else:
            context = ""

        # 8 Entities
        if "entities" in tweet:
            if "annotations" in tweet["entities"]:
                annotations = tweet["entities"]["annotations"]
            else:
                annotations = ""
            if "hashtags" in tweet["entities"]:
                hashtags = tweet["entities"]["hashtags"]
            else:
                hashtags = ""
            if "urls" in tweet["entities"]:
                urls = tweet["entities"]["urls"]
            else:
                urls = ""
        else:
            annotations = ""
            hashtags = ""
            urls = ""

        # Assemble all data in a list
        res = [tweet_id, created_at, text, author_id, like_count, quote_count, reply_count, retweet_count, 
                geo, country, place_full_name, place_name, bbox, place_type, 
                hashtags, annotations, urls, context]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)

    # When done, close the CSV file
    csvFile.close()

def main():

    ###set up write file
    savefilename = "dataUK4.csv"
    csvFile = open(savefilename, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Create headers for the data you want to save
    column_names = ["tweet_id", "created_at", "text", "author_id", "like_count", "quote_count", "reply_count", "retweet_count", 
        "geo", "country", "place_full_name", "place_name", "bbox", "place_type", 
        "hashtags", "annotations", "urls", "context"]
    # csvWriter.writerow(column_names)
    csvFile.close()

    #setting up times
    time_str = "2020-01-01 00:00:00" #MAKE SURE TO RESET THIS EACH TIME YOU STOP START THE CODE. First start on 2020-01-01 00:00:00
    test_stop_time ="2020-05-04 00:06:00"
    format_str = "%Y-%m-%d %H:%M:%S"
    datetime_cur = datetime.strptime(time_str, format_str)
    datetime_stop = datetime.strptime(test_stop_time, format_str)

    request_count = 0
    tweet_count = 0
    while datetime_cur < datetime_stop: 
        json_response = gettweets(timefrom=datetime_cur)
        newtweets = json_response["meta"]["result_count"]
        datetime_cur = datetime_cur + timedelta(hours=3)
        tweet_count += newtweets
        request_count += 1
        print("requests=", request_count,"total collected=",tweet_count,"new=",newtweets, "date=", datetime_cur, "retrieved=", datetime.strftime(datetime.now(), format_str))
        append_to_csv(json_response,savefilename)
    print("stopped at" + str(datetime.strptime(time_str, format_str)))


if __name__ == "__main__":
    main()


##### OTHER USEFUL FUNCTIONS. 
