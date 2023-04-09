from typing import List, Tuple, Dict, Optional
from utils.settings import Settings
from utils.message_log import MessageLog as Log


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
    def parse_battles(text: List[str]) -> List[Tuple[Tuple[str, str, int], ...]]:
        """ Parse list of text into list of tuple of 

        Returns:
            list of battle informations (url, summon, repeats) and combact action
        """
        text = Parser.pre_parse(text)

        url: str = Parser._parse_url(text.pop(0))
        summon: str = Parser._parse_summon(text.pop(0))
        repeat: int = Parser._parse_repeat(text.pop(0))
        combact = []
        ret = []

        while len(text)>0:
            line = text.pop(0)
            if not line.startswith("http"):
                combact.append(line)
            else:
                ret.append(
                    ( (url, summon, repeat), Parser._parse_combact(combact)) )
                url = line
                summon = Parser._parse_summon(text.pop(0))
                repeat: int = Parser._parse_repeat(text.pop(0))
                combact = []
        # end
        ret.append(
            ( (url, summon, repeat), Parser._parse_combact(combact)) )
        
        return ret
        
    @staticmethod
    def _parse_combact(text: List[str]) -> List[Tuple[str, Dict[str, int]]]:
        """Parse the combact action

        Returns:
            list of function names and function param in combact mode
        """
        char_selected: Optional[int] = None
        ret = []
        for line in text:
            if line.startswith('character'):
                chains = line.split('.')
                char_idx = int(chains[0][-1])
                if char_idx not in (1,2,3,4):
                    raise RuntimeError(
                        f"[Parser] Invalid chracter number: {char_idx}")
                if char_selected == None:
                    ret += [("selectchar", {"idx":char_idx-1} )] 
                elif char_selected != char_idx:
                    ret += [("changechar", {"idx":char_idx-1})] 
                char_selected = char_idx

                for cmd in chains[1:]:

                    skill_idx = int(cmd[-2])
                    if skill_idx not in (1,2,3,4):
                        raise RuntimeError(
                            f"[Parser] Invalid skill number: {skill_idx}")
                    ret.append( 
                        ( "useskill", {"idx":skill_idx-1} ) 
                    )
            elif line == "attack":
                char_selected = None
                ret.append( (line, {}) )
            elif line == "enablefullauto":
                if char_selected is not None:
                    ret += [("deselectchar", {})]
                ret += [(line, {})]
            else:
                ret.append( (line, {}) )
        return ret