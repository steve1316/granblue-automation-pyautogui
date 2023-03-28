from typing import List
from utils.settings import Settings
from utils.message_log import MessageLog as Log


class Parser:
    """
    Provides the utility functions for parsing user written combat script for \
    GenericV2
    """

    @staticmethod
    def pre_parse(text: List[str]):
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
    def _parse_summon(line: str):
        if not line.startswith("supportsummon:"): 
            raise RuntimeError(
                f"[Pareser] Invalid summon: {line}")
        return line.split(':')[1]
    
    @staticmethod
    def _parse_url(line: str):
        if not line.startswith("http"): 
            raise RuntimeError(
                f"[Pareser] Invalid Url: {line}")
        return line
    
    @staticmethod
    def _parse_repeat(line: str):
        if not line.startswith("repeat:"): 
            raise RuntimeError(
                f"[Pareser] Invalid Url: {line}")
        Settings.item_amount_to_farm
        value = line.split(':')[1]
        if value == "default":
            return Settings.item_amount_to_farm
        return int(value)



    @staticmethod
    def parse_battles(text: List[str]):
        """ Parse list of text into list of tuple of 
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
    def _parse_combact(text: List[str]):
        ret = []
        for line in text:
            if line.startswith('character'):
                # character1
                char_idx = int(line.split('.')[0][-1])
                if char_idx not in (1,2,3,4):
                    raise RuntimeError(
                        f"[Parser] Invalid chracter number: {char_idx}")
                ret.append( 
                    ( "selectchar", {"idx":char_idx} ) 
                )

                for cmd in line.split('.')[1:]:
                    # useSkill(1)
                    skill_idx = int(cmd[-2])
                    if skill_idx not in (1,2,3,4):
                        raise RuntimeError(
                            f"[Parser] Invalid skill number: {skill_idx}")
                    ret.append( 
                        ( "useskill", {"idx":skill_idx} ) 
                    )

            else:
                ret.append( (line, {}) )
        return ret
