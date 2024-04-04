import os
import random
import shutil
import requests
import time

from db_util import MongoDBActor


class TwitterFeeds:
    def __init__(self, search_param=None, twitter_cred=1):
        self.twitter_cred = twitter_cred
        self.search_param = search_param
        self.search_url = "https://api.twitter.com/1.1/users/search.json"
        self.query_params = self.create_query_params()
        self.graceful_wait = 1

    def sleep_in_too_many_requests(self, msg):
        if 'Too Many Requests' in msg:
            print("Found too many requests exception.. sleeping for a minute ..")
            time.sleep(60)

    def get_random_bearer_token(self):
        # other tokens are not active, placeholder for 1 only
        tokens = [
            os.environ['TWITTER_BEARER_TOKEN_dazlingstarz']
            # os.environ['TWITTER_BEARER_TOKEN_harold_tuc11811'],
            # os.environ['TWITTER_BEARER_TOKEN_TomasHarry87231'],
            # os.environ['TWITTER_BEARER_TOKEN_victor_gar49736'],
            # os.environ['TWITTER_BEARER_TOKEN_AlexisS15667'], # resets on Jan
            # os.environ['TWITTER_BEARER_TOKEN_sandra_kas26624']
        ]
        return random.choice(tokens)

    def create_query_for_exact_match_user_name(self):
        fields = "created_at,description"
        params = {"usernames": self.search_param, "user.fields": fields}
        return params

    def create_query_params(self):
        return {
            'q': self.search_param,
            'page': 40,
            'count': 20
        }

    def bearer_oauth(self, r):
        r.headers[
            "Authorization"] = f"Bearer {'{}'}".format(self.get_random_bearer_token())
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def make_get_request(self, url, params):
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def get_user_fields(self):
        return {
            "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,edit_controls,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
            "count": 199,
            "skip_status": True,
            "include_user_entities": False,
            "screen_name": self.search_param
        }

    def get_followers(self):
        _all_followers = set()
        _all_json = []
        try:
            url = "https://api.twitter.com/1.1/followers/list.json"
            params = self.get_user_fields()
            json_response = self.make_get_request(url, params)
            print(json_response)
            _all_json = [json_response]
            while True:
                if "next_cursor" in json_response:
                    next_token = json_response["next_cursor"]
                    params['next_cursor'] = next_token
                    json_response = self.make_get_request(url, params)
                    print(json_response)
                    _all_json = _all_json + [json_response]

                    time.sleep(self.graceful_wait)
                    # ensure this applies to twitter rules of number of requests it can make
                else:
                    break
        except Exception as ex:
            print(str(ex))
            self.sleep_in_too_many_requests(str(ex))

        for _json in _all_json:
            if 'users' in _json:
                _users = _json['users']
                for user in _users:
                    if 'screen_name' in user:
                        _all_followers.add(user['screen_name'])

        return list(_all_followers)

    def fetch_user_detail_by_screen_name(self):
        try:
            search_url = "https://api.twitter.com/2/users/by"
            fields = "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url," \
                     "protected,public_metrics,url,username,verified,withheld"
            query_param = {"usernames": self.search_param,
                           "user.fields": fields
                           }

            json_response = self.make_get_request(search_url, query_param)
            return json_response
        except Exception as ex:
            print("Exception occurred in fetching Twitter account data {}".format(ex))
            _id = MongoDBActor("user_detail_anamoly").find_and_modify(
                key={'screen_name': self.search_param},
                data={
                    'screen_name': self.search_param,
                    'detail': "{}".format(ex),

                })
            print("Inserted with exception {}, upsert_id:{}".format(self.search_param, _id))

            self.sleep_in_too_many_requests(str(ex))

    def download_image(self, request_url, save_path):
        try:
            response = requests.get(request_url,
                                    auth=self.bearer_oauth,
                                    stream=True)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)

            if response.status_code == 200:
                with open('{}'.format(save_path), 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
        except Exception as ex:
            print("Exception occurred in twitter request to image {}".format(ex))
            self.sleep_in_too_many_requests(str(ex))

    """
        Input:
            numeric_user_id
            additional_query_param: list of key, pair 
                The additional query param can be formatted based on supported query param: https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets

        output: The output will be either errors or list of tweets data found
            list of errors  
                OR
            list of data 

    """

    def get_user_tweets(self, numeric_user_id='1532420332497342466', _additional_query_param=None):
        # sample suspended id: 2881117795
        _tweets_data = []
        _url = "https://api.twitter.com/2/users/{}/tweets/".format(numeric_user_id)
        _param = {
            'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,'
                            'id,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,reply_settings,'
                            'source,text,withheld',
            'expansions': 'attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,'
                          'referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id',
            'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
            'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld',
            'media.fields': 'duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,alt_text,variants',
            'max_results': '100'
        }

        if _additional_query_param:
            if type(_additional_query_param) is dict:
                for k, v in _additional_query_param.items():
                    _param[k] = v

        try:
            json_response = self.make_get_request(_url, _param)

            if 'errors' in json_response:
                # this is list
                _errors = json_response['errors']
                return _errors

            if 'data' not in json_response:
                return []

            _data = json_response['data']
            for _tweet in _data:
                _tweets_data.append(_tweet)

            # error case where user_id is suspended
            """
                {
                    "errors": [
                        {
                            "detail": "User has been suspended: [2881117795].",
                            "parameter": "id",
                            "resource_id": "2881117795",
                            "resource_type": "user",
                            "title": "Forbidden",
                            "type": "https://api.twitter.com/2/problems/resource-not-found",
                            "value": "2881117795"
                        }
                    ]
                }

            """

            # returning the data
            """
                {
                    "data": [

                        { .... },
                        { .... }
                        ....                    
                    ],
                    "meta": {
                        "newest_id": "1592974543773396993",
                        "next_token": "7140dibdnow9c7btw424c28rstvlbelekdc8wj65ji4vs",
                        "oldest_id": "1592600829760094208",
                        "result_count": 100
                    }
                }

            """
            counter = 1
            while True:
                if "meta" in json_response:
                    if "next_token" in json_response['meta']:
                        next_token = json_response["meta"]["next_token"]
                        _param['pagination_token'] = next_token
                        json_response = self.make_get_request(_url, _param)

                        if 'data' not in json_response:
                            continue
                        _data = json_response['data']
                        for _tweet in _data:
                            _tweets_data.append(_tweet)
                        time.sleep(self.graceful_wait)
                        print("user_id:{}, Tweet pagination request count:{}".format(numeric_user_id, counter))
                        counter = counter + 1
                    else:
                        break
                else:
                    break
        except Exception as ex:
            print("Exception occurred: {}, numeric_id:{}".format(ex, numeric_user_id))
            self.sleep_in_too_many_requests(str(ex))
        return _tweets_data
