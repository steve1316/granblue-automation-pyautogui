from typing import List, Tuple, Dict, Optional
from utils.settings import Settings
from utils.message_log import MessageLog as Log
from utils.debugger import Debugger as Debug


class Parser:
    """
    Provides the utility functions for parsing user written combat script for \
    GenericV2
    """

    @staticmethod
    def pre_parse(text: List[str]) -> List[str]:
        """ Remove all comment and empty line and lowercased result
        """
        result = []
        for line in [line.strip().lower() for line in text]:
            if line == "" or line.startswith("#") or line.startswith("/"):
                continue
            else:
                result.append(line)
        return result

    @staticmethod
    def _parse_summon(line: str) -> str:
        if not line.startswith("supportsummon:"):
            raise RuntimeError(
                f"[Pareser] Invalid summon: {line}")
        return line.split(':')[1]

    @staticmethod
    def _parse_url(line: str) -> str:
        if not line.startswith("http"):
            raise RuntimeError(
                f"[Pareser] Invalid Url: {line}")
        return line

    @staticmethod
    def _parse_repeat(line: str) -> int:
        if not line.startswith("repeat:"):
            raise RuntimeError(
                f"[Pareser] Invalid Url: {line}")
        Settings.item_amount_to_farm
        value = line.split(':')[1]
        if value == "default":
            return Settings.item_amount_to_farm
        return int(value)

    @staticmethod
    def _parse_character(line: str, is_char_selected: bool) -> List[Tuple[str, Dict[str, int]]]:
        """ Parse a line of character action

        Returns:
            Same type as _parse_combact
        """
        ret = []
        is_skill_selected = False
        chains = line.split('.')
        char_idx = int(chains.pop(0)[-1])
        if char_idx not in (1, 2, 3, 4):
            raise ValueError(
                f"[Parser] Invalid chracter number: {char_idx}")
        if is_char_selected:
            ret += [("changechar", {"idx": char_idx-1})]
        else:
            ret += [("selectchar", {"idx": char_idx-1})]

        for cmd in chains:
            if cmd.startswith('useskill'):
                skill_idx = int(cmd[-2])
                if skill_idx not in (1, 2, 3, 4):
                    raise ValueError(
                        f"[Parser] Invalid skill number: {skill_idx}")
                ret += [("useskill", {"idx": skill_idx-1})]
                is_skill_selected = True
            elif cmd.startswith('target'):
                target_idx = int(cmd[-2])
                if target_idx not in (1, 2, 3, 4, 5, 6):
                    raise ValueError(
                        f"[Parser] Invalid skill target number: {target_idx}")
                if not is_skill_selected:
                    raise RuntimeError(
                        f"[Parser] Select a skill before picking a target")
                ret += [('target', {"idx": target_idx-1})]
                is_skill_selected = False
        return ret

    @staticmethod
    def parse_battles(text: List[str]) -> List[Tuple[Tuple[str, str, int], ...]]:
        """ Parse list of battles into list

        Returns:
            list of battle informations (url, summon, repeats) and combact action
        """
        text = Parser.pre_parse(text)

        url: str = Parser._parse_url(text.pop(0))
        summon: str = Parser._parse_summon(text.pop(0))
        repeat: int = Parser._parse_repeat(text.pop(0))
        combact = []
        ret = []

        while len(text) > 0:
            line = text.pop(0)
            if not line.startswith("http"):
                combact.append(line)
            else:
                ret.append(
                    ((url, summon, repeat), Parser._parse_combact(combact)))
                url = line
                summon = Parser._parse_summon(text.pop(0))
                repeat: int = Parser._parse_repeat(text.pop(0))
                combact = []
        # end
        ret.append(
            ((url, summon, repeat), Parser._parse_combact(combact)))

        if Settings.debug_mode:
            Debug.parser(ret)
        return ret

    @staticmethod
    def _parse_combact(text: List[str]) -> List[Tuple[str, Dict[str, int]]]:
        """Parse the combact action

        Returns:
            list of function names and function param in combact mode
        """
        is_char_selected: bool = False
        ret = []
        for line in text:
            if line.startswith('character'):
                ret += Parser._parse_character(line, is_char_selected)
                is_char_selected = True
            elif line.startswith("wait"):
                ret += [("wait", {"time": int(line[5:-1])})]
            elif line.startswith("summon"):
                idx = int(line[-2])
                if idx not in (1,2,3,4,5,6):
                    raise ValueError
                if is_char_selected:
                    ret += [("deselectchar", {})]
                    is_char_selected = False
                ret += [('usesummon', {'idx': idx-1})]
            elif line == "attack":
                is_char_selected = False
                ret += [(line, {})]
            elif line == "enablefullauto":
                if is_char_selected:
                    ret += [("deselectchar", {})]
                    is_char_selected = False
                ret += [(line, {})]

            else:
                ret.append((line, {}))

        # finish
        if len(ret) == 0:
            ret += [("enablefullauto", {})]
        return ret
