import re

import tweepy
from tweepy import Stream

from utils.message_log import MessageLog
from utils.settings import Settings


class RoomStreamListener(tweepy.StreamListener):
    """
    A listener class using the Twitter Stream API to grab all incoming tweets that match the search query.
    """

    def __init__(self):
        super().__init__()
        self.tweets = []

    def on_status(self, status):
        if Settings.debug_mode:
            print(f"[DEBUG] Stream found: {status.text}")

        self.tweets.append(status)

    def on_error(self, status_code):
        print(f"[ERROR] Stream API encountered Error Code {status_code}. Closing the stream...")
        return False


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
        "Lvl 200 Lindwurm": "Lv200 リンドヴルム",

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
        "Lvl 250 Beelzebub": "Lv250 ベルゼバブ",

        # Xeno Clash Raids
        "Lvl 100 Xeno Ifrit": "Lv100 ゼノ・イフリート",
        "Lvl 100 Xeno Cocytus": "Lv100 ゼノ・コキュートス",
        "Lvl 100 Xeno Vohu Manah": "Lv100 ゼノ・ウォフマナフ",
        "Lvl 100 Xeno Sagittarius": "Lv100 ゼノ・サジタリウス",
        "Lvl 100 Xeno Corow": "Lv100 ゼノ・コロゥ",
        "Lvl 100 Xeno Diablo": "Lv100 ゼノ・ディアボロス"
    }

    _listener = RoomStreamListener()
    _stream: Stream = None

    @staticmethod
    def connect():
        if Settings.farming_mode == "Raid":
            MessageLog.print_message(f"\n[TWITTER] Authenticating provided consumer keys and tokens with the Twitter API...")
            _auth = tweepy.OAuthHandler(Settings.twitter_keys_tokens[0], Settings.twitter_keys_tokens[1])
            _auth.set_access_token(Settings.twitter_keys_tokens[2], Settings.twitter_keys_tokens[3])
            _api = tweepy.API(_auth)

            # Check to see if connection to Twitter's API was successful.
            if not _api.verify_credentials():
                raise (ConnectionError(f"[ERROR] Failed to connect to the Twitter API. Check your keys and tokens."))

            MessageLog.print_message(f"[TWITTER] Successfully connected to the Twitter API.")

            # Create the listener and stream objects. for the Twitter Stream API.
            TwitterRoomFinder._stream = tweepy.Stream(auth = _api.auth, listener = TwitterRoomFinder._listener)

            # Start asynchronous process of listening to tweets for the specified raid.
            MessageLog.print_message(f"\n[TWITTER] Now listening onto the Stream API for the newest tweets for {Settings.mission_name}.")
            TwitterRoomFinder._stream.filter(track = [Settings.mission_name, TwitterRoomFinder._list_of_raids[Settings.mission_name]], is_async = True, filter_level = "none")

    @staticmethod
    def test_connection() -> bool:
        _auth = tweepy.OAuthHandler(Settings.twitter_keys_tokens[0], Settings.twitter_keys_tokens[1])
        _auth.set_access_token(Settings.twitter_keys_tokens[2], Settings.twitter_keys_tokens[3])
        _api = tweepy.API(_auth)
        return _api.verify_credentials()

    @staticmethod
    def get_room_code():
        """Clean the tweets from the listener and parse out a valid room code from them.

        Returns:
            (str): A single room code that has not been visited.
        """
        if len(TwitterRoomFinder._listener.tweets) == 0:
            MessageLog.print_message(f"[TWITTER] There are no recent or detected tweets available for the given raid.")
            return ""

        MessageLog.print_message(f"[TWITTER] Now cleaning up the tweets and parsing for room codes...")

        while len(TwitterRoomFinder._listener.tweets) > 0:
            tweet = TwitterRoomFinder._listener.tweets.pop()

            if re.search(rf"\b{Settings.mission_name}\b", tweet.text) or re.search(rf"\b{TwitterRoomFinder._list_of_raids[Settings.mission_name]}\b", tweet.text):
                # Split up the tweet's text by whitespaces.
                split_text = tweet.text.split(" ")

                # Parse the room code and if it has not been visited yet, append it to the list.
                for i, identifier in enumerate(split_text):
                    if (":Battle" in identifier) or (":参戦ID" in identifier):
                        parsed_code = split_text[i - 1]
                        if parsed_code not in TwitterRoomFinder._already_visited_codes:
                            MessageLog.print_message(f"[TWITTER] Found {parsed_code} created at {tweet.created_at}")
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
        if TwitterRoomFinder._stream is not None:
            TwitterRoomFinder._stream.disconnect()
        return None
