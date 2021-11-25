import json
import os
import sys
from typing import List, Tuple

from utils.message_log import MessageLog


class Settings:
    ######################################################
    # ################## settings.json ###################
    # Read from settings.json and populate the class variables.
    try:
        _file = open(f"{os.getcwd()}/backend/settings.json")
    except FileNotFoundError:
        try:
            _file = open(f"{os.getcwd()}/settings.json")
        except FileNotFoundError:
            print("[ERROR] Failed to find settings.json. Exiting now...")
            sys.exit(1)

    _data = json.load(_file)

    combat_script_name: str = _data["game"]["combatScriptName"]
    combat_script: List[str] = _data["game"]["combatScript"]
    farming_mode: str = _data["game"]["farmingMode"]
    item_name: str = _data["game"]["item"]
    map_name: str = _data["game"]["map"]
    mission_name: str = _data["game"]["mission"]
    item_amount_to_farm: int = _data["game"]["itemAmount"]
    item_amount_farmed: int = 0
    amount_of_runs_finished: int = 0
    summon_element_list: List[str] = _data["game"]["summonElements"]
    summon_list: List[str] = _data["game"]["summons"]
    group_number: int = _data["game"]["groupNumber"]
    party_number: int = _data["game"]["partyNumber"]
    debug_mode: bool = _data["game"]["debugMode"]

    # #### twitter ####
    twitter_keys_tokens: List[str] = [_data["twitter"]["twitterAPIKey"], _data["twitter"]["twitterAPIKeySecret"], _data["twitter"]["twitterAccessToken"], _data["twitter"]["twitterAccessTokenSecret"]]
    # #### end of twitter ####

    # #### discord ####
    enable_discord: bool = _data["discord"]["enableDiscordNotifications"]
    discord_token: str = _data["discord"]["discordToken"]
    user_id: int = _data["discord"]["discordUserID"]
    # #### end of discord ####

    # #### configuration ####
    enabled_auto_restore: bool = _data["configuration"]["enableAutoRestore"]
    use_full_elixir: bool = _data["configuration"]["enableFullElixir"]
    use_soul_balm: bool = _data["configuration"]["enableSoulBalm"]
    enable_bezier_curve_mouse_movement: bool = _data["configuration"]["enableBezierCurveMouseMovement"]
    custom_mouse_speed: float = float(_data["configuration"]["mouseSpeed"])
    enable_delay_between_runs: bool = _data["configuration"]["enableDelayBetweenRuns"]
    delay_in_seconds: int = _data["configuration"]["delayBetweenRuns"]
    enable_randomized_delay_between_runs: bool = _data["configuration"]["enableRandomizedDelayBetweenRuns"]
    delay_in_seconds_lower_bound: int = _data["configuration"]["delayBetweenRunsLowerBound"]
    delay_in_seconds_upper_bound: int = _data["configuration"]["delayBetweenRunsUpperBound"]
    # #### end of configuration ####

    # #### nightmare ####
    enable_nightmare: bool = _data["nightmare"]["enableNightmare"]
    _enable_custom_nightmare_settings: bool = _data["nightmare"]["enableCustomNightmareSettings"]
    _farming_modes_with_nightmares = ["Event", "Event (Token Drawboxes)", "Rise of the Beasts", "Xeno Clash"]
    nightmare_combat_script: List[str] = _data["nightmare"]["nightmareCombatScript"]
    nightmare_combat_script_name: str = _data["nightmare"]["nightmareCombatScriptName"]
    nightmare_summon_list: List[str] = _data["nightmare"]["nightmareSummons"]
    nightmare_summon_elements_list: List[str] = _data["nightmare"]["nightmareSummonElements"]
    nightmare_group_number: int = _data["nightmare"]["nightmareGroupNumber"]
    nightmare_party_number: int = _data["nightmare"]["nightmarePartyNumber"]
    if enable_nightmare and ((farming_mode == "Special" and mission_name == "VH Angel Halo") or _farming_modes_with_nightmares.__contains__(mission_name)):
        MessageLog.print_message(f"\n[NIGHTMARE] Initializing settings for {farming_mode}'s Nightmare...")

        if _enable_custom_nightmare_settings:
            # Start checking for validity and if not, default back to the settings for Farming Mode.
            if len(nightmare_combat_script) == 0:
                MessageLog.print_message(f"[NIGHTMARE] Combat Script for {farming_mode}'s Nightmare will reuse the one for Farming Mode.")
                nightmare_combat_script = combat_script

            if len(nightmare_summon_list) == 0:
                MessageLog.print_message(f"[NIGHTMARE] Summons for {farming_mode}'s Nightmare will reuse the ones for Farming Mode.")
                nightmare_summon_list = summon_list

            if len(nightmare_summon_elements_list) == 0:
                MessageLog.print_message(f"[NIGHTMARE] Summon Elements for {farming_mode}'s Nightmare will reuse the ones for Farming Mode.")
                nightmare_summon_elements_list = summon_element_list

            if nightmare_group_number < 1 or nightmare_group_number > 7:
                MessageLog.print_message(f"[NIGHTMARE] Group Number for {farming_mode}'s Nightmare will reuse the one for Farming Mode.")
                nightmare_group_number = group_number

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

    # #### raid ####
    enable_auto_exit_raid: bool = _data["raid"]["enableAutoExitRaid"]
    time_allowed_until_auto_exit_raid: int = _data["raid"]["timeAllowedUntilAutoExitRaid"] * 60
    enable_no_timeout: bool = _data["raid"]["enableNoTimeout"]
    # #### end of raid ####

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
