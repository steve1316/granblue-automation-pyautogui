import json
import re
from typing import Union

import tweepy
import tweepy.asynchronous
from tweepy import Response, API

from utils.message_log import MessageLog
from utils.settings import Settings


class RoomStreamListenerV2(tweepy.StreamingClient):
    """
    A listener class using the Twitter Stream API V2 to grab all incoming tweets that match the search query.
    """

    tweets = []

    def on_errors(self, status_code):
        MessageLog.print_message(f"[ERROR] Stream API encountered Error Code {status_code}. Closing the stream...")
        return False

    def on_data(self, raw_data):
        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Raw Data found: {raw_data}")
        self.tweets.append(raw_data)


class TwitterRoomFinder:
    """
    Provides the functions needed to perform Twitter API-related tasks such as searching tweets for room codes for raid farming.
    """

    _already_visited_codes = []

    _list_of_raids = {
        # Omega Raids
        "Lvl 50 Tiamat Omega": "Lv50 ティアマト・マグナ",
        "Lvl 100 Tiamat Omega Ayr": "Lv100 ティアマト・マグナ＝エア",
        "Lvl 70 Colossus Omega": "Lv70 コロッサス・マグナ",
        "Lvl 100 Colossus Omega": "Lv100 コロッサス・マグナ",
        "Lvl 60 Leviathan Omega": "Lv60 リヴァイアサン・マグナ",
        "Lvl 100 Leviathan Omega": "Lv100 リヴァイアサン・マグナ",
        "Lvl 60 Yggdrasil Omega": "Lv60 ユグドラシル・マグナ",
        "Lvl 100 Yggdrasil Omega": "Lv100 ユグドラシル・マグナ",
        "Lvl 75 Luminiera Omega": "Lv75 シュヴァリエ・マグナ",
        "Lvl 100 Luminiera Omega": "Lv100 シュヴァリエ・マグナ",
        "Lvl 75 Celeste Omega": "Lv75 セレスト・マグナ",
        "Lvl 100 Celeste Omega": "Lv100 セレスト・マグナ",

        # Tier 1 Summon Raids
        "Lvl 100 Twin Elements": "Lv100 フラム＝グラス",
        "Lvl 120 Twin Elements": "Lv120 フラム＝グラス",
        "Lvl 100 Macula Marius": "Lv100 マキュラ・マリウス",
        "Lvl 120 Macula Marius": "Lv120 マキュラ・マリウス",
        "Lvl 100 Medusa": "Lv100 メドゥーサ",
        "Lvl 120 Medusa": "Lv120 メドゥーサ",
        "Lvl 100 Nezha": "Lv100 ナタク",
        "Lvl 120 Nezha": "Lv120 ナタク",
        "Lvl 100 Apollo": "Lv100 アポロン",
        "Lvl 120 Apollo": "Lv120 アポロン",
        "Lvl 100 Dark Angel Olivia": "Lv100 Dエンジェル・オリヴィエ",
        "Lvl 120 Dark Angel Olivia": "Lv120 Dエンジェル・オリヴィエ",

        # Tier 2 Summon Raids
        "Lvl 100 Athena": "Lv100 アテナ",
        "Lvl 100 Grani": "Lv100 グラニ",
        "Lvl 100 Baal": "Lv100 バアル",
        "Lvl 100 Garuda": "Lv100 ガルーダ",
        "Lvl 100 Odin": "Lv100 オーディン",
        "Lvl 100 Lich": "Lv100 リッチ",

        # Primarch Raids
        "Lvl 100 Michael": "Lv100 ミカエル",
        "Lvl 100 Gabriel": "Lv100 ガブリエル",
        "Lvl 100 Uriel": "Lv100 ウリエル",
        "Lvl 100 Raphael": "Lv100 ラファエル",
        "The Four Primarchs": "四大天司ＨＬ",

        # Nightmare Raids
        "Lvl 100 Proto Bahamut": "Lv100 プロトバハムート",
        "Lvl 100 Grand Order": "Lv100 ジ・オーダー・グランデ",

        # Rise of the Beasts Raids
        "Lvl 60 Zhuque": "Lv60 朱雀",
        "Lvl 90 Agni": "Lv90 アグニス",
        "Lvl 60 Xuanwu": "Lv60 玄武",
        "Lvl 90 Neptune": "Lv90 ネプチューン",
        "Lvl 60 Baihu": "Lv60 白虎",
        "Lvl 90 Titan": "Lv90 ティターン",
        "Lvl 60 Qinglong": "Lv60 青竜",
        "Lvl 90 Zephyrus": "Lv90 ゼピュロス",
        "Lvl 100 Huanglong": "Lv100 黄龍",
        "Lvl 100 Qilin": "Lv100 黒麒麟",
        "Huanglong & Qilin (Impossible)": "黄龍・黒麒麟HL",
        "Lvl 100 Shenxian": "Lv100 四象瑞神",

        # Impossible Raids
        "Lvl 110 Rose Queen": "Lv110 ローズクイーン",
        "Lvl 120 Shiva": "Lv120 シヴァ",
        "Lvl 120 Europa": "Lv120 エウロペ",
        "Lvl 120 Godsworn Alexiel": "Lv120 ゴッドガード・ブローディア",
        "Lvl 120 Grimnir": "Lv120 グリームニル",
        "Lvl 120 Metatron": "Lv120 メタトロン",
        "Lvl 120 Avatar": "Lv120 アバター",
        "Lvl 120 Prometheus": "Lv120 プロメテウス",
        "Lvl 120 Ca Ong": "Lv120 カー・オン",
        "Lvl 120 Gilgamesh": "Lv120 ギルガメッシュ",
        "Lvl 120 Morrigna": "Lv120 バイヴカハ",
        "Lvl 120 Hector": "Lv120 ヘクトル",
        "Lvl 120 Anubis": "Lv120 アヌビス",
        "Lvl 150 Proto Bahamut": "Lv150 プロトバハムート",
        "Lvl 150 Ultimate Bahamut": "Lv150 アルティメットバハムート",
        "Lvl 200 Ultimate Bahamut": "Lv200 アルティメットバハムート",
        "Lvl 200 Grand Order": "Lv200 ジ・オーダー・グランデ",
        "Lvl 200 Akasha": "Lv200 アーカーシャ",
        "Lvl 150 Lucilius": "Lv150 ルシファー",
        "Lvl 250 Lucilius": "Lv250 ルシファー",
        "Lvl 250 Beelzebub": "Lv250 ベルゼバブ",
        "Lvl 250 Belial": "Lv250 ベリアル",
        "Lvl 300 Super Ultimate Bahamut": "Lv300 スーパーアルティメットバハムート",
        "Lvl 200 Lindwurm": "Lv200 リンドヴルム",
        "Lvl 275 Diaspora": "Lv275 ディアスポラ",
        "Lvl 275 Mugen": "Lv275 ムゲン",

        # Malice Raids
        "Lvl 150 Tiamat Malice": "Lv150 ティアマト・マリス",
        "Lvl 150 Leviathan Malice": "Lv150 リヴァイアサン・マリス",
        "Lvl 150 Phronesis": "Lv150 フロネシス",
        "Lvl 150 Luminiera Malice": "Lv150 シュヴァリエ・マリス",
        "Lvl 150 Anima-Animus Core": "Lv150 アニマ・アニムス・コア",

        # Six Dragon Raids
        "Lvl 200 Wilnas": "Lv200 ウィルナス",
        "Lvl 200 Wamdus": "Lv200 ワムデュス",
        "Lvl 200 Galleon": "Lv200 ガレヲン",
        "Lvl 200 Ewiyar": "Lv200 イーウィヤ",
        "Lvl 200 Lu Woh": "Lv200 ル・オー",
        "Lvl 200 Fediel": "Lv200 フェディエル",

        # Xeno Clash Raids
        "Lvl 100 Xeno Ifrit": "Lv100 ゼノ・イフリート",
        "Lvl 100 Xeno Cocytus": "Lv100 ゼノ・コキュートス",
        "Lvl 100 Xeno Vohu Manah": "Lv100 ゼノ・ウォフマナフ",
        "Lvl 100 Xeno Sagittarius": "Lv100 ゼノ・サジタリウス",
        "Lvl 100 Xeno Corow": "Lv100 ゼノ・コロゥ",
        "Lvl 100 Xeno Diablo": "Lv100 ゼノ・ディアボロス",

        # Ennead Raids
        "Lvl 120 Osiris": "Lv120 オシリス",
        "Lvl 120 Horus": "Lv120 ホルス",
        "Lvl 120 Bennu": "Lv120 ベンヌ",
        "Lvl 120 Atum": "Lv120 アトゥム",
        "Lvl 120 Tefnut": "Lv120 テフヌト",
        "Lvl 120 Ra": "Lv120 ラー",
    }

    _listener_old: API = None
    _listener_old_tweets = []
    _list_of_id = []
    _listener: RoomStreamListenerV2 = None

    @staticmethod
    def connect():
        """Connect to either Twitter API V1.1 or V2.

        Returns:
            None
        """
        # There are two methods of connection: keys/access tokens for V1.1 and bearer token for V2.
        if Settings.twitter_use_version2:
            MessageLog.print_message(f"\n[TWITTER] Authenticating provided bearer token with the Twitter API V2...")
            TwitterRoomFinder.test_connection()
            MessageLog.print_message(f"[TWITTER] Successfully connected to the Twitter API V2.")

            # Create the listener and stream objects for the Twitter Stream API.
            TwitterRoomFinder._listener = RoomStreamListenerV2(Settings.twitter_bearer_token)

            # Start asynchronous process of listening to tweets for the specified raid.
            MessageLog.print_message(f"\n[TWITTER] Now listening onto the Stream API for the newest tweets for {Settings.mission_name}.")

            # Make sure to remove any existing rules from the filter.
            TwitterRoomFinder._remove_rules()

            MessageLog.print_message(f"[TWITTER] Successfully connected to the Twitter API V2.")

            # Add the search terms as new rules.
            search_terms = [Settings.mission_name, TwitterRoomFinder._list_of_raids[Settings.mission_name]]
            for term in search_terms:
                TwitterRoomFinder._listener.add_rules(tweepy.StreamRule(term))

            MessageLog.print_message(f"\n[TWITTER] Current rules to filter by: {TwitterRoomFinder._listener.get_rules()}.")

            # Now listen to the stream in a separate thread (the async components has an issue where the data was not being received and could not be seen from the main thread).
            TwitterRoomFinder._listener.filter(threaded = True)
        else:
            MessageLog.print_message(f"\n[TWITTER] Authenticating provided consumer keys and access tokens with the Twitter API V1.1...")
            TwitterRoomFinder.test_connection()
            MessageLog.print_message(f"[TWITTER] Successfully connected to the Twitter API V1.1.")

            # Create the listener and stream objects for the Twitter Stream API V1.1.
            _auth = tweepy.OAuth1UserHandler(Settings.twitter_keys_tokens[0], Settings.twitter_keys_tokens[1], Settings.twitter_keys_tokens[2], Settings.twitter_keys_tokens[3])
            TwitterRoomFinder._listener_old = tweepy.API(_auth)

            MessageLog.print_message(f"\n[TWITTER] Now ready for manual searching of tweets for {Settings.mission_name}.")

    @staticmethod
    def _remove_rules():
        """Remove any existing rules for the filter for use in the Twitter API V2.

        Returns:
            None
        """
        rules: Union[dict, Response, Response] = TwitterRoomFinder._listener.get_rules()
        if rules[0] is not None:
            TwitterRoomFinder._listener.delete_rules(rules[0])

    @staticmethod
    def test_connection() -> bool:
        """Test connection to the API using either the bearer token for V2 or the consumer keys/tokens for V1.1.

        Returns:
            True if connection was established to the API.
        """
        if Settings.twitter_use_version2:
            _auth = tweepy.Client(bearer_token = Settings.twitter_bearer_token)

            # Check to see if connection to Twitter's API was successful.
            try:
                if len(_auth.get_recent_tweets_count('twitter')) == 0:
                    raise (ConnectionError(f"[ERROR] Failed to connect to the Twitter API V2 with both the keys/tokens as well as the bearer token."))
            except Exception:
                raise (ConnectionError(f"[ERROR] Failed to connect to the Twitter API V2 with both the keys/tokens as well as the bearer token."))
        else:
            _auth = tweepy.OAuth1UserHandler(Settings.twitter_keys_tokens[0], Settings.twitter_keys_tokens[1], Settings.twitter_keys_tokens[2], Settings.twitter_keys_tokens[3])
            _api = tweepy.API(_auth)

            # Check to see if connection to Twitter's API was successful.
            if not _api.verify_credentials():
                raise (ConnectionError(f"[ERROR] Failed to connect to the Twitter API V1.1 with both the keys/tokens as well as the bearer token."))

        return True

    @staticmethod
    def _find_most_recent(count: int = 10):
        """Manually search the most recent tweets with the queries for Twitter API V1.1.

        Returns:
            None
        """
        MessageLog.print_message(f"\n[TWITTER] Now finding the {count} most recent tweets for {Settings.mission_name}.")

        query_en = f"+(:Battle ID) AND +({Settings.mission_name})"
        query_jp = f"+(:参戦ID) AND +({TwitterRoomFinder._list_of_raids[Settings.mission_name]})"

        # Search JP tweets first and filter for tweets that the bot has not processed yet.
        tweet_jp = TwitterRoomFinder._listener_old.search_tweets(q = query_jp, count = count)
        for tweet in tweet_jp:
            if tweet.id not in TwitterRoomFinder._list_of_id and len(TwitterRoomFinder._listener_old_tweets) < count:
                TwitterRoomFinder._listener_old_tweets.append(tweet)
                TwitterRoomFinder._list_of_id.append(tweet.id)

        # Search EN tweets only if the filtered JP tweets was less than the desired amount.
        if len(TwitterRoomFinder._listener_old_tweets) < count:
            tweet_en = TwitterRoomFinder._listener_old.search_tweets(q = query_en, count = count)
            for tweet in tweet_en:
                if tweet.id not in TwitterRoomFinder._list_of_id and len(TwitterRoomFinder._listener_old_tweets) < count:
                    TwitterRoomFinder._listener_old_tweets.append(tweet)
                    TwitterRoomFinder._list_of_id.append(tweet.id)

    @staticmethod
    def get_room_code() -> str:
        """Clean the tweets from the listener and parse out a valid room code from them.

        Returns:
            (str): A single room code that has not been visited.
        """
        if not Settings.twitter_use_version2:
            TwitterRoomFinder._find_most_recent()

        if (not Settings.twitter_use_version2 and len(TwitterRoomFinder._listener_old_tweets) == 0) or (
                Settings.twitter_use_version2 and len(TwitterRoomFinder._listener.tweets) == 0):
            MessageLog.print_message(f"[TWITTER] There are no recent or detected tweets available for the given raid.")
            return ""

        MessageLog.print_message(f"[TWITTER] Now cleaning up the tweets and parsing for room codes...")

        while (not Settings.twitter_use_version2 and len(TwitterRoomFinder._listener_old_tweets) > 0) or (
                Settings.twitter_use_version2 and len(TwitterRoomFinder._listener.tweets) > 0):
            if Settings.twitter_use_version2:
                tweet_text = json.loads(TwitterRoomFinder._listener.tweets.pop().decode('utf-8'))['data']["text"]
            else:
                tweet_text = TwitterRoomFinder._listener_old_tweets.pop().text

            if Settings.twitter_use_version2 and (re.search(rf"\b{Settings.mission_name}\b", tweet_text) or re.search(rf"\b{TwitterRoomFinder._list_of_raids[Settings.mission_name]}\b", tweet_text)):
                # Split up the tweet's text by whitespaces.
                split_text = tweet_text.split(" ")

                # Parse the room code and if it has not been visited yet, append it to the list.
                for i, identifier in enumerate(split_text):
                    if (":Battle" in identifier) or (":参戦ID" in identifier):
                        parsed_code = split_text[i - 1]
                        if parsed_code not in TwitterRoomFinder._already_visited_codes:
                            MessageLog.print_message(f"[TWITTER] Found {parsed_code}")
                            TwitterRoomFinder._already_visited_codes.append(parsed_code)
                            return parsed_code
                        else:
                            MessageLog.print_message(f"[TWITTER] Already visited {parsed_code} before in this session. Skipping this code...")

            else:
                MessageLog.print_message(f"[TWITTER] Skipping tweet as it is for a different raid.")

        return ""

    @staticmethod
    def disconnect():
        """Disconnect from the Stream API.

        Returns:
            None
        """
        if not Settings.twitter_use_version2 and TwitterRoomFinder._listener_old is not None:
            TwitterRoomFinder._listener_old.session.close()
        elif Settings.twitter_use_version2 and TwitterRoomFinder._listener is not None:
            TwitterRoomFinder._listener.disconnect()
        return None
