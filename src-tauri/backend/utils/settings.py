import json
import os
import multiprocessing
from typing import List, Tuple

from utils.message_log import MessageLog


class Settings:
    bot_status_flag = multiprocessing.Value("i", 0)

    ######################################################
    # ################## settings.json ###################
    # Read from settings.json and populate the class variables.
    _file = open(f"{os.getcwd()}/backend/settings.json")
    _data = json.load(_file)

    combat_script: List[str] = _data["combatScript"]
    farming_mode: str = _data["farmingMode"]
    item_name: str = _data["item"]
    map_name: str = _data["map"]
    mission_name: str = _data["mission"]
    item_amount_to_farm: int = _data["itemAmount"]
    item_amount_farmed: int = 0
    amount_of_runs_finished: int = 0
    summon_element_list: List[str] = _data["summonElements"]
    summon_list: List[str] = _data["summons"]
    group_number: int = _data["groupNumber"]
    party_number: int = _data["partyNumber"]
    debug_mode: bool = _data["debugMode"]

    # #### twitter ####
    twitter_keys_tokens: List[str] = [_data["twitter"]["apiKey"], _data["twitter"]["apiKeySecret"], _data["twitter"]["accessToken"], _data["twitter"]["accessTokenSecret"]]
    # #### end of twitter ####

    # #### discord ####
    discord_queue = multiprocessing.Queue()
    enable_discord: bool = _data["discord"]["enableDiscordNotifications"]
    discord_token: str = _data["discord"]["discordToken"]
    user_id: int = _data["discord"]["discordUserID"]
    # #### end of discord ####

    # #### refill ####
    enabled_auto_restore: bool = _data["enableAutoRestore"]
    use_full_elixir: bool = _data["enableFullElixir"]
    use_soul_balm: bool = _data["enableSoulBalm"]
    # #### end of refill ####

    # #### configuration ####
    enable_bezier_curve_mouse_movement: bool = _data["enableBezierCurveMouseMovement"]
    custom_mouse_speed: float = float(_data["mouseSpeed"])
    enable_delay_between_runs: bool = _data["delayBetweenRuns"]["enableDelayBetweenRuns"]
    delay_in_seconds: int = _data["delayBetweenRuns"]["delay"]
    enable_randomized_delay_between_runs: bool = _data["randomizedDelayBetweenRuns"]["enableRandomizedDelayBetweenRuns"]
    delay_in_seconds_lower_bound: int = _data["randomizedDelayBetweenRuns"]["delayLowerBound"]
    delay_in_seconds_upper_bound: int = _data["randomizedDelayBetweenRuns"]["delayUpperBound"]
    # #### end of configuration ####

    # #### nightmare ####
    enable_nightmare: bool = _data["nightmare"]["enableNightmare"]
    _enable_custom_nightmare_settings: bool = _data["nightmare"]["enableCustomNightmareSettings"]
    _farming_modes_with_nightmares = ["Event", "Event (Token Drawboxes)", "Rise of the Beasts", "Xeno Clash"]
    if enable_nightmare and ((farming_mode == "Special" and mission_name == "VH Angel Halo") or _farming_modes_with_nightmares.__contains__(mission_name)):
        MessageLog.print_message(f"\n[NIGHTMARE] Initializing settings for {farming_mode}'s Nightmare...")

        if _enable_custom_nightmare_settings:
            # Start checking for validity and if not, default back to the settings for Farming Mode.
            nightmare_combat_script: List[str] = _data["nightmare"]["nightmareCombatScript"]
            nightmare_combat_script_name: str = _data["nightmare"]["nightmareCombatScriptName"]
            if len(nightmare_combat_script) == 0:
                MessageLog.print_message(f"[NIGHTMARE] Combat Script for {farming_mode}'s Nightmare will reuse the one for Farming Mode.")
                nightmare_combat_script = combat_script

            nightmare_summon_list: List[str] = _data["nightmare"]["nightmareSummons"]
            if len(nightmare_summon_list) == 0:
                MessageLog.print_message(f"[NIGHTMARE] Summons for {farming_mode}'s Nightmare will reuse the ones for Farming Mode.")
                nightmare_summon_list = summon_list

            nightmare_summon_elements_list: List[str] = _data["nightmare"]["nightmareSummonElements"]
            if len(nightmare_summon_elements_list) == 0:
                MessageLog.print_message(f"[NIGHTMARE] Summon Elements for {farming_mode}'s Nightmare will reuse the ones for Farming Mode.")
                nightmare_summon_elements_list = summon_element_list

            nightmare_group_number: int = _data["nightmare"]["nightmareGroupNumber"]
            if nightmare_group_number < 1 or nightmare_group_number > 7:
                MessageLog.print_message(f"[NIGHTMARE] Group Number for {farming_mode}'s Nightmare will reuse the one for Farming Mode.")
                nightmare_group_number = group_number

            nightmare_party_number: int = _data["nightmare"]["nightmarePartyNumber"]
            if nightmare_party_number < 1 or nightmare_party_number > 6:
                MessageLog.print_message(f"[NIGHTMARE] Party Number for {farming_mode}'s Nightmare will reuse the one for Farming Mode.")
                nightmare_party_number = party_number
        else:
            MessageLog.print_message(f"[NIGHTMARE] Reusing settings from Farming Mode for {farming_mode}'s Nightmare...")
            nightmare_combat_script = combat_script
            nightmare_summon_list = summon_list
            nightmare_summon_elements_list = summon_element_list
            nightmare_group_number = group_number
            nightmare_party_number = party_number

        MessageLog.print_message(f"[NIGHTMARE] Settings initialized for {farming_mode}'s Nightmare...")
    # #### end of nightmare ####

    # #### arcarum ####
    enable_stop_on_arcarum_boss: bool = _data["arcarum"]["enableStopOnArcarumBoss"]
    # #### end of arcarum ####
    # ################## end of settings.json ###################
    #############################################################

    # ################## Window Dimensions ###################
    window_left: int = None
    window_top: int = None
    window_width: int = None
    window_height: int = None
    home_button_location: Tuple[int, int] = None
    calibration_complete: bool = False
    additional_calibration_required: bool = False
    party_selection_first_run: bool = True
    # ################## end of Window Dimensions ###################
