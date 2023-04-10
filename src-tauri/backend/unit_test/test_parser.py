from utils.settings import Settings
from utils.parser import Parser

case = [    "// This script starts Semi-Auto mode on Turn 1.",
            "// It will go uninterrupted until either the party wipes or the quest/raid ends.",
            "",
            "",
            "https://game.granbluefantasy.jp/#quest/supporter/800021/22",
            "supportSummon:Kaguya",
            "",
            "quickSummon",
            "subBack",
            "https://game.granbluefantasy.jp/#quest/supporter/800021/22",
            "supportSummon:Kaguya",
            "",
            "quickSummon",
            "character1.useSkill(2).useSkill(4)",
            "subBack"]

print(Parser.parse_battles(case))