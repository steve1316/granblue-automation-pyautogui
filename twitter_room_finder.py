import datetime
from typing import Iterable

import tweepy


class TwitterRoomFinder():
    """
    Provides the functions needed to perform Twitter API-related tasks such as searching tweets for room codes for raid farming.

    Attributes
    ----------
    game (game.Game): The Game object.
    
    consumer_key (str): Consumer API key from the user's personal Twitter Developer app.
    
    consumer_secret (str): Consumer Secret API key from the user's personal Twitter Developer app.
    
    access_token (str): Access token from the user's personal Twitter Developer app.
    
    access_token_secret (str): Secret Access token from the user's personal Twitter Developer app.
    
    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """
    def __init__(self, game, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str, debug_mode: bool = False):
        super().__init__()
        
        self.game = game
        
        # Save consumer keys and access tokens.
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
        self.request_limit = 900
        self.rate_limit = 900 # A maximum of 900 requests per 15 minutes or 900 seconds before getting rate-limited.
        
        self.already_visited = []
        self.list_of_id = []
        self.list_of_raids_jp = {
            "Lvl 100 Odin": "Lv100 オーディン",
            "Lvl 100 Medusa": "Lv100 メドゥーサ",
            "Lvl 120 Grimnir": "Lv120 グリームニル",
        }
        
        self.debug_mode = debug_mode
        
        # Connect to Twitter's API.
        self.game.print_and_save(f"\n{self.game.printtime()} [TWITTER] Authenticating...")
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)
        self.game.print_and_save(f"{self.game.printtime()} [TWITTER] Successfully connected to the Twitter API.")
    
    def find_most_recent(self, raid_name: str, count: int = 10, tweets_only: bool = False):
        """Start listening to tweets containing room codes starting with JP and then listens for EN tweets if there was not enough collected tweets.

        Args:
            raid_name (str): Name and level of the raid that appears in tweets containing the room code to it.
            count (int): Number of most recent tweets to grab. Defaults to 10.
            tweets_only (bool): Either return tweets or 

        Returns:
            tweets (Iterable[str]): List of 10 most recent tweets that match the query.
        """
        self.game.print_and_save(f"\n{self.game.printtime()} [TWITTER] Now finding the {count} most recent tweets for {raid_name}.")
        today = datetime.datetime.today()
        query_en = f"+(:Battle ID) AND +({raid_name})"
        query_jp = f"+(:参戦ID) AND +({self.list_of_raids_jp[raid_name]})"
        
        # Example of expected tweet:
        #   CUSTOM_USER_MESSAGE XXXXXXXX :Battle ID
        #   I need backup!
        #   LEVEL and NAME OF RAID
        
        tweets = []
        list_of_id = []

        if(len(self.list_of_id) > 50):
            self.list_of_id = []
            
        tweet_jp = self.api.search(q=query_jp, since=today.strftime('%Y-%m-%d'), count=count)
        for tweet in tweet_jp:
            if(tweet.id not in self.list_of_id and len(tweets) < count):
                self.game.print_and_save(f"{self.game.printtime()} [TWITTER] Found JP tweet.")
                tweets.append(tweet)
                self.list_of_id.append(tweet.id)

        if(len(tweets) < count):
            tweet_en = self.api.search(q=query_en, since=today.strftime('%Y-%m-%d'), count=count)
            for tweet in tweet_en:
                if(tweet.id not in self.list_of_id and len(tweets) < count):
                    self.game.print_and_save(f"{self.game.printtime()} [TWITTER] Found EN tweet.")
                    tweets.append(tweet)
                    self.list_of_id.append(tweet.id)
                    
        return tweets
        
    def clean_tweets(self, tweets: Iterable[str]):
        """Clean the tweets passed to this function and parse out the room codes from them.

        Args:
            tweets (Iterable[str]): List of tweets with its text unchanged.

        Returns:
            room_codes (Iterable[str]): List of room codes cleaned of all other text.
        """
        self.game.print_and_save(f"\n{self.game.printtime()} [TWITTER] Now cleaning up the tweets and parsing for room codes...\n")
        room_codes = []
        
        # Split the text up by whitespaces and find the element in the list that has the room code.
        for tweet in tweets:
            if(len(self.already_visited) > 50):
                self.already_visited = []
            
            split_text = tweet.text.split(" ")
            for i, identifier in enumerate(split_text):
                if((":Battle" in identifier) or (":参戦ID" in identifier)):
                    parsed_code = split_text[i - 1]
                    if(parsed_code not in self.already_visited):
                        self.game.print_and_save(f"{self.game.printtime()} [TWITTER] Found {parsed_code} created at {tweet.created_at}")
                        room_codes.append(parsed_code)
                        self.already_visited.append(parsed_code)
                        break
                    else:
                        self.game.print_and_save(f"{self.game.printtime()} [TWITTER] Already visited {parsed_code} before in this session. Skipping this code...")

        return room_codes
