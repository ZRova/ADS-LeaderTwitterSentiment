from datetime import datetime
from html import entities
import json
import csv
import dateutil
from matplotlib.transforms import Bbox

##input these
filenames = "academic_filenames2.txt"
savefilename = "test.csv"

#for testing
jsonname = "2021-10-28T00-00-00Z.json"
# Create file
csvFile = open(savefilename, "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)

#Create headers for the data you want to save
column_names = ["tweet_id", "created_at", "text", "author_id", "like_count", "quote_count", "reply_count", "retweet_count", 
    "geo", "country", "place_full_name", "place_name", "bbox", "place_type", 
    "hashtags", "annotations", "urls", "context"]
csvWriter.writerow(column_names)
csvFile.close()

def append_to_csv(json_filename, csvFileName):
    f = open(json_filename)
    json_data = json.load(f)
    
    # counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(csvFileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet_no in range(json_data['meta']["result_count"]):

        tweet = json_data["data"][tweet_no]
        #tweet_geo = json_data["includes"]["places"][tweet_no]
        # print(tweet_geo)
        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']
        # print(author_id)

        # 2. Time created
        format_str = "%Y-%m-%dT%H:%M:%S.000Z"
        created_at = datetime.strptime(tweet["created_at"], format_str)

        # 3. Tweet text
        text = tweet['text']

        # 4. Geolocation 
        # this is complicated because it removes doubled up locations 
        # and i was trying to minimise the number of comparisons it would have to make. 
        if ('geo' in tweet): 
            print("geo in tweet")  
            tweet_geo = ""
            locations_tot = len(json_data["includes"]["places"])
            for location in range(tweet_no+1):
                # location = min(locations_tot-1, tweet_no) - location
                # print(tweet["geo"]["place_id"])
                # print(json_data["includes"]["places"][location]["id"])
                if tweet["geo"]["place_id"] == json_data["includes"]["places"][location]["id"]:
                    tweet_geo = json_data["includes"]["places"][location]
                    print("found match")
                    break

            geo = tweet['geo']['place_id']
            country = tweet_geo["country_code"]
            place_full_name = tweet_geo["full_name"]
            place_name = tweet_geo["name"]
            bbox = tweet_geo["geo"]["bbox"]
            place_type = tweet_geo["place_type"]
        else:
            geo = " "
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
            if "hashtags" in tweet:
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
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print("# of Tweets added from this response: ", counter) 


append_to_csv(jsonname, savefilename)