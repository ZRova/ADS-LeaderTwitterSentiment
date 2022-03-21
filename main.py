import requests
import os
import json

bearer_token = os.environ.get("BEARER_TOKEN")
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

search_url = "https://api.twitter.com/2/spaces/search"

search_term = 'bojo' # Replace this value with your search term

#######
# QUERYING FOR boris OR boris johnson OR bojo
# place_country:GB 
# -is:retweet
# lang:en

# date:                     ##HOW DO I DO THAT
# has:geo                   ##IS THIS NECESSARY GIVEN PLACE SEARCH


# Optional params: host_ids,conversation_controls,created_at,creator_id,id,invited_user_ids,is_ticketed,lang,media_key,participants,scheduled_start,speaker_ids,started_at,state,title,updated_at
query_params = {'query': search_term, 'space.fields': 'title,created_at', 'expansions': 'creator_id'}


def create_headers(bearer_token):
    headers = {
        "Authorization": "Bearer {}".format(bearer_token),
        "User-Agent": "v2SpacesSearchPython"
    }
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(search_url, headers, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()

