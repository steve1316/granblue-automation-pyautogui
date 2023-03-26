from utils.settings import Settings
from utils.parser import Parser

case = [    "// This script starts Semi-Auto mode on Turn 1.",
            "// It will go uninterrupted until either the party wipes or the quest/raid ends.",
            "",
            "https://game.granbluefantasy.jp/#quest/supporter/800021/22",
            "friendSummon:Kaguya",
            "",
            "quickSummon",
            "subBack",
            "https://game.granbluefantasy.jp/#quest/supporter/800021/22",
            "friendSummon:Kaguya",
            "",
            "quickSummon",
            "subBack"]

print(Parser.parse_raid_sequence(case))