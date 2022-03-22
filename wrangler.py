import pandas as pd


df = pd.read_csv("borisjohnsonscrape_20220321.csv", usecols=["id", "date", "time", "user_id", "username", "tweet", "language", "replies_count", "retweets_count", "likes_count", "geo", "reply_to", "place.type", "place.coordinates"])
df = df.loc[df.language == "en"]
print(df["tweet"].head(10))
df.to_csv("cleanbojo_20220321")


##### use for concatting all files. 
# with open(“out.csv”, “w”) as f:
#     for file in list_of_files:
#         df = pd.read_json(file)
#         f.write(df.to_csv())
