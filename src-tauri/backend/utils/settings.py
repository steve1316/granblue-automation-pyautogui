import json
import os
import multiprocessing
from configparser import ConfigParser
from typing import List, Tuple

from utils.message_log import MessageLog


class Settings:
    bot_status_flag = multiprocessing.Value("i", 0)

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
    # ################## end of settings.json ###################

    # ################## config.ini ###################
    # Grab the Twitter API keys and tokens from config.ini. The list order is: [consumer key, consumer secret key, access token, access secret token].
    _config = ConfigParser()
    _config.read(f"{os.getcwd()}/backend/config.ini")

    # #### discord ####
    discord_queue = multiprocessing.Queue()
    enable_discord: bool = _config.getboolean("discord", "enable_discord")
    discord_token: str = _config.get("discord", "discord_token")
    user_id: int = _config.getint("discord", "user_id")
    # #### end of discord ####

    # #### twitter ####
    twitter_keys_tokens: List[str] = [_config.get("twitter", "api_key"), _config.get("twitter", "api_key_secret"),
                                      _config.get("twitter", "access_token"), _config.get("twitter", "access_token_secret")]
    # #### end of twitter ####

    # #### refill ####
    use_full_elixir: bool = _config.getboolean("refill", "refill_using_full_elixir")
    use_soul_balm: bool = _config.getboolean("refill", "refill_using_soul_balms")
    enabled_auto_restore: bool = _config.getboolean("refill", "enabled_auto_restore")
    # #### end of refill ####

    # #### configuration ####
    enable_bezier_curve_mouse_movement: bool = _config.getboolean("configuration", "enable_bezier_curve_mouse_movement")
    custom_mouse_speed: float = float(_config.get("configuration", "mouse_speed"))
    enable_delay_between_runs: bool = _config.getboolean("configuration", "enable_delay_between_runs")
    delay_in_seconds: int = _config.getint("configuration", "delay_in_seconds")
    enable_randomized_delay_between_runs: bool = _config.getboolean("configuration", "enable_randomized_delay_between_runs")
    delay_in_seconds_lower_bound: int = _config.getint("configuration", "delay_in_seconds_lower_bound")
    delay_in_seconds_upper_bound: int = _config.getint("configuration", "delay_in_seconds_upper_bound")
    # #### end of configuration ####

    # #### dimensional_halo ####
    enable_dimensional_halo = _config.getboolean("dimensional_halo", "enable_dimensional_halo")
    if enable_dimensional_halo and mission_name == "VH Angel Halo":
        MessageLog.print_message("\n[SPECIAL] Initializing settings for Dimensional Halo...")

        dimensional_halo_combat_script = _config.get("dimensional_halo", "dimensional_halo_combat_script")

        dimensional_halo_summon_list = _config.get("dimensional_halo", "dimensional_halo_summon_list").replace(" ", "_").split(",")
        if len(dimensional_halo_summon_list) == 1 and dimensional_halo_summon_list[0] == "":
            dimensional_halo_summon_list.clear()

        dimensional_halo_summon_element_list = _config.get("dimensional_halo", "dimensional_halo_summon_element_list").replace(" ", "_").split(",")
        if len(dimensional_halo_summon_element_list) == 1 and dimensional_halo_summon_element_list[0] == "":
            dimensional_halo_summon_element_list.clear()

        dimensional_halo_group_number = _config.get("dimensional_halo", "dimensional_halo_group_number")
        dimensional_halo_party_number = _config.get("dimensional_halo", "dimensional_halo_party_number")
        dimensional_halo_amount = 0

        if dimensional_halo_combat_script == "":
            MessageLog.print_message("[SPECIAL] Combat Script for Dimensional Halo will reuse the one for Farming Mode.")
            dimensional_halo_combat_script = combat_script

        if len(dimensional_halo_summon_element_list) == 0:
            MessageLog.print_message("[SPECIAL] Summon Elements for Dimensional Halo will reuse the ones for Farming Mode.")
            dimensional_halo_summon_element_list = summon_element_list

        if len(dimensional_halo_summon_list) == 0:
            MessageLog.print_message("[SPECIAL] Summons for Dimensional Halo will reuse the ones for Farming Mode.")
            dimensional_halo_summon_list = summon_list

        if dimensional_halo_group_number == "":
            MessageLog.print_message("[SPECIAL] Group Number for Dimensional Halo will reuse the one for Farming Mode.")
            dimensional_halo_group_number = group_number
        else:
            dimensional_halo_group_number = int(dimensional_halo_group_number)

        if dimensional_halo_party_number == "":
            MessageLog.print_message("[SPECIAL] Party Number for Dimensional Halo will reuse the one for Farming Mode.")
            dimensional_halo_party_number = party_number
        else:
            dimensional_halo_party_number = int(dimensional_halo_party_number)

        MessageLog.print_message("[SPECIAL] Settings initialized for Special...")
    # #### end of dimensional_halo ####

    # ### event ####
    enable_event_nightmare = _config.getboolean("event", "enable_event_nightmare")
    if enable_event_nightmare:
        MessageLog.print_message("\n[EVENT] Initializing settings for Event Nightmare...")

        event_nightmare_combat_script = _config.get("event", "event_nightmare_combat_script")

        event_nightmare_summon_list = _config.get("event", "event_nightmare_summon_list").replace(" ", "_").split(",")
        if len(event_nightmare_summon_list) == 1 and event_nightmare_summon_list[0] == "":
            event_nightmare_summon_list.clear()

        event_nightmare_summon_element_list = _config.get("event", "event_nightmare_summon_element_list").replace(" ", "_").split(",")
        if len(event_nightmare_summon_element_list) == 1 and event_nightmare_summon_element_list[0] == "":
            event_nightmare_summon_element_list.clear()

        event_nightmare_group_number = _config.get("event", "event_nightmare_group_number")
        event_nightmare_party_number = _config.get("event", "event_nightmare_party_number")

        if event_nightmare_combat_script == "":
            MessageLog.print_message("[EVENT] Combat Script for Event Nightmare will reuse the one for Farming Mode.")
            event_nightmare_combat_script = combat_script

        if len(event_nightmare_summon_element_list) == 0:
            MessageLog.print_message("[EVENT] Summon Elements for Event Nightmare will reuse the ones for Farming Mode.")
            event_nightmare_summon_element_list = summon_element_list

        if len(event_nightmare_summon_list) == 0:
            MessageLog.print_message("[EVENT] Summons for Event Nightmare will reuse the ones for Farming Mode.")
            event_nightmare_summon_list = summon_list

        if event_nightmare_group_number == "":
            MessageLog.print_message("[EVENT] Group Number for Event Nightmare will reuse the one for Farming Mode.")
            event_nightmare_group_number = group_number
        else:
            event_nightmare_group_number = int(event_nightmare_group_number)

        if event_nightmare_party_number == "":
            MessageLog.print_message("[EVENT] Party Number for Event Nightmare will reuse the one for Farming Mode.")
            event_nightmare_party_number = party_number
        else:
            event_nightmare_party_number = int(event_nightmare_party_number)

        MessageLog.print_message("[EVENT] Settings initialized for Event Nightmare...")
    # ### end of event ####

    # #### rotb ####
    enable_rotb_extreme_plus = _config.getboolean("rise_of_the_beasts", "enable_rotb_extreme_plus")
    if enable_rotb_extreme_plus:
        MessageLog.print_message("\n[ROTB] Initializing settings for Rise of the Beasts Extreme+...")

        rotb_extreme_plus_combat_script = _config.get("rise_of_the_beasts", "rotb_extreme_plus_combat_script")

        rotb_extreme_plus_summon_list = _config.get("rise_of_the_beasts", "rotb_extreme_plus_summon_list").replace(" ", "_").split(",")
        if len(rotb_extreme_plus_summon_list) == 1 and rotb_extreme_plus_summon_list[0] == "":
            rotb_extreme_plus_summon_list.clear()

        rotb_extreme_plus_summon_element_list = _config.get("rise_of_the_beasts", "rotb_extreme_plus_summon_element_list").replace(" ", "_").split(",")
        if len(rotb_extreme_plus_summon_element_list) == 1 and rotb_extreme_plus_summon_element_list[0] == "":
            rotb_extreme_plus_summon_element_list.clear()

        rotb_extreme_plus_group_number = _config.get("rise_of_the_beasts", "rotb_extreme_plus_group_number")
        rotb_extreme_plus_party_number = _config.get("rise_of_the_beasts", "rotb_extreme_plus_party_number")
        rotb_extreme_plus_amount = 0

        if rotb_extreme_plus_combat_script == "":
            MessageLog.print_message("[ROTB] Combat Script for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
            rotb_extreme_plus_combat_script = combat_script

        if len(rotb_extreme_plus_summon_element_list) == 0:
            MessageLog.print_message("[ROTB] Summon Elements for Rise of the Beasts Extreme+ will reuse the ones for Farming Mode.")
            rotb_extreme_plus_summon_element_list = summon_element_list

        if len(rotb_extreme_plus_summon_list) == 0:
            MessageLog.print_message("[ROTB] Summons for Rise of the Beasts Extreme+ will reuse the ones for Farming Mode.")
            rotb_extreme_plus_summon_list = summon_list

        if rotb_extreme_plus_group_number == "":
            MessageLog.print_message("[ROTB] Group Number for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
            rotb_extreme_plus_group_number = group_number
        else:
            rotb_extreme_plus_group_number = int(rotb_extreme_plus_group_number)

        if rotb_extreme_plus_party_number == "":
            MessageLog.print_message("[ROTB] Party Number for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
            rotb_extreme_plus_party_number = party_number
        else:
            rotb_extreme_plus_party_number = int(rotb_extreme_plus_party_number)

        MessageLog.print_message("[ROTB] Settings initialized for Rise of the Beasts Extreme+...")
    # #### end of rotb ####

    # #### xeno_clash ####
    enable_xeno_clash_nightmare = _config.getboolean("xeno_clash", "enable_xeno_clash_nightmare")
    if enable_xeno_clash_nightmare:
        MessageLog.print_message("\n[XENO.CLASH] Initializing settings for Xeno Clash Nightmare...")

        xeno_clash_nightmare_combat_script = _config.get("xeno_clash", "xeno_clash_nightmare_combat_script")

        xeno_clash_nightmare_summon_list = _config.get("xeno_clash", "xeno_clash_nightmare_summon_list").replace(" ", "_").split(",")
        if len(xeno_clash_nightmare_summon_list) == 1 and xeno_clash_nightmare_summon_list[0] == "":
            xeno_clash_nightmare_summon_list.clear()

        xeno_clash_nightmare_summon_element_list = _config.get("xeno_clash", "xeno_clash_nightmare_summon_element_list").replace(" ", "_").split(",")
        if len(xeno_clash_nightmare_summon_element_list) == 1 and xeno_clash_nightmare_summon_element_list[0] == "":
            xeno_clash_nightmare_summon_element_list.clear()

        xeno_clash_nightmare_group_number = _config.get("xeno_clash", "xeno_clash_nightmare_group_number")
        xeno_clash_nightmare_party_number = _config.get("xeno_clash", "xeno_clash_nightmare_party_number")

        if xeno_clash_nightmare_combat_script == "":
            MessageLog.print_message("[XENO.CLASH] Combat Script for Xeno Clash Nightmare will reuse the one for Farming Mode.")
            xeno_clash_nightmare_combat_script = combat_script

        if len(xeno_clash_nightmare_summon_element_list) == 0:
            MessageLog.print_message("[XENO.CLASH] Summon Elements for Xeno Clash Nightmare will reuse the ones for Farming Mode.")
            xeno_clash_nightmare_summon_element_list = summon_element_list

        if len(xeno_clash_nightmare_summon_list) == 0:
            MessageLog.print_message("[XENO.CLASH] Summons for Xeno Clash Nightmare will reuse the ones for Farming Mode.")
            xeno_clash_nightmare_summon_list = summon_list

        if xeno_clash_nightmare_group_number == "":
            MessageLog.print_message("[XENO.CLASH] Group Number for Xeno Clash Nightmare will reuse the one for Farming Mode.")
            xeno_clash_nightmare_group_number = group_number
        else:
            xeno_clash_nightmare_number = int(xeno_clash_nightmare_group_number)

        if xeno_clash_nightmare_party_number == "":
            MessageLog.print_message("[XENO.CLASH] Party Number for Xeno Clash Nightmare will reuse the one for Farming Mode.")
            xeno_clash_nightmare_party_number = party_number
        else:
            xeno_clash_nightmare_party_number = int(xeno_clash_nightmare_party_number)

        MessageLog.print_message("[XENO.CLASH] Settings initialized for Xeno Clash Nightmare...")
    # #### end of xeno_clash ####

    # #### arcarum ####
    enable_stop_on_arcarum_boss: bool = _config.getboolean("arcarum", "enable_stop_on_arcarum_boss")
    # #### end of arcarum ####
    # ################## end of config.ini ###################

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
