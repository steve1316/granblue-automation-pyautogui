import random

import pyautogui
import pyclick
import re
import pyperclip
from typing import List
from utils.settings import Settings
from utils.message_log import MessageLog as Log


class Parser:
    """
    Provides the utility functions for parsing user written combat script.
    Only for combate_mode_lite
    """

    @staticmethod
    def pre_parse(text: List[str]):
        """ Not implement
        
        return:
        """
        return

    @staticmethod
    def parse_raid_sequence(text: List[str]):
        """ Parse list of text into list of tuple of 
        (url, summon_name, [action])
        
        return:
            list of (url, summon_name, [action])
        """

        URL = None
        summon = None
        actions = []
        ret = []
        for line in [line.strip().lower() for line in text]:

            if line == "" or line[0] == "#" or line[0] == "/":
                continue

            if line.startswith("http"):
                # first url
                if URL is None:
                    URL = line
                # non first url, action of previous url should not be empty
                elif len(actions) == 0:
                    raise RuntimeError(f"[Pareser] Invalid generic_lite script format: {line}")
                # conclude the previous url
                else:
                    ret.append( (URL, summon, actions) )
                    URL = line
                    summon = None
                    actions = []
            elif line.startswith("friendsummon:"):
                if URL is None or len(actions) != 0 or summon != None:
                    raise RuntimeError(f"[Pareser] Invalid generic_lite script format: {line}")
                else:
                    summon = line.split(':')[1]
            elif URL is None or summon is None:
                raise RuntimeError(f"[Pareser] Invalid generic_lite script format: {line}")
            else:
                actions.append(line)
        # check last
        if URL is not None:
            if len(actions) == 0:
                raise RuntimeError(f"[Pareser] Invalid generic_lite script format: {text[-1]}")
            else:
                ret.append( (URL, summon, actions) )
        if len(ret) == 0:
            raise RuntimeError(f"[Pareser] Script is empty!")
        return ret