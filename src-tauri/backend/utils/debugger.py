from utils.message_log import MessageLog as Log
from typing import List, Tuple, Dict, Optional

class Debugger:

    @staticmethod
    def parser(battles:List[Tuple[Tuple[str, str, int], ...]]):
        for battle in battles:
            config, actions = battle
            url, summon, repeat, = config
            Log.print_message("\nDebugging Parser...")
            Log.print_message(f"url: {url}")
            Log.print_message(f"summon: {summon}")
            Log.print_message(f"repeat: {repeat}")
            for act in actions:
                func, param = act
                Log.print_message(f"action: {func}, parameter: {param}")
