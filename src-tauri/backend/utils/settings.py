import json
import os
import sys
from typing import List, Tuple

from dictor import dictor

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

    combat_script_name: str = dictor(_data, "game.combatScriptName", "")
    combat_script: List[str] = dictor(_data, "game.combatScript", [])
    combat_elapsed_time: float = 0.0
    farming_mode: str = dictor(_data, "game.farmingMode", checknone = True)
    item_name: str = dictor(_data, "game.item", checknone = True)
    map_name: str = dictor(_data, "game.map", checknone = True)
    mission_name: str = dictor(_data, "game.mission", checknone = True)
    item_amount_to_farm: int = dictor(_data, "game.itemAmount", 1)
    item_amount_farmed: int = 0
    amount_of_runs_finished: int = 0
    summon_element_list: List[str] = dictor(_data, "game.summonElements", [])
    summon_list: List[str] = dictor(_data, "game.summons", [])
    group_number: int = dictor(_data, "game.groupNumber", 1)
    party_number: int = dictor(_data, "game.partyNumber", 1)
    debug_mode: bool = dictor(_data, "game.debugMode", False)

    # #### twitter ####
    twitter_use_version2: bool = dictor(_data, "twitter.twitterUseVersion2", False)
    twitter_keys_tokens: List[str] = [dictor(_data, "twitter.twitterAPIKey", ""),
                                      dictor(_data, "twitter.twitterAPIKeySecret", ""),
                                      dictor(_data, "twitter.twitterAccessToken", ""),
                                      dictor(_data, "twitter.twitterAccessTokenSecret", "")]
    twitter_bearer_token: str = dictor(_data, "twitter.twitterBearerToken", "")
    # #### end of twitter ####

    # #### discord ####
    enable_discord: bool = dictor(_data, "discord.enableDiscordNotifications", False)
    discord_token: str = dictor(_data, "discord.discordToken", "")
    user_id: int = dictor(_data, "discord.discordUserID", "")
    # #### end of discord ####

    # #### api ####
    enable_opt_in_api: bool = dictor(_data, "api.enableOptInAPI", False)
    # #### end of api ####

    # #### configuration ####
    reduce_delay_seconds: float = dictor(_data, "configuration.reduceDelaySeconds", 0.0)
    enable_bezier_curve_mouse_movement: bool = dictor(_data, "configuration.enableBezierCurveMouseMovement", True)
    custom_mouse_speed: float = float(dictor(_data, "configuration.mouseSpeed", 0.2))
    enable_delay_between_runs: bool = dictor(_data, "configuration.enableDelayBetweenRuns", False)
    delay_in_seconds: int = dictor(_data, "configuration.delayBetweenRuns", 15)
    enable_randomized_delay_between_runs: bool = dictor(_data, "configuration.enableRandomizedDelayBetweenRuns", False)
    delay_in_seconds_lower_bound: int = dictor(_data, "configuration.delayBetweenRunsLowerBound", 15)
    delay_in_seconds_upper_bound: int = dictor(_data, "configuration.delayBetweenRunsUpperBound", 60)
    enable_refresh_during_combat: bool = dictor(_data, "configuration.enableRefreshDuringCombat", True)
    enable_auto_quick_summon: bool = dictor(_data, "configuration.enableAutoQuickSummon", False)
    enable_bypass_reset_summon: bool = dictor(_data, "configuration.enableBypassResetSummon", False)
    static_window: bool = dictor(_data, "configuration.staticWindow", True)
    enable_mouse_security_attempt_bypass: bool = dictor(_data, "configuration.enableMouseSecurityAttemptBypass", True)
    # #### end of configuration ####

    # #### nightmare ####
    enable_nightmare: bool = dictor(_data, "nightmare.enableNightmare", False)
    _enable_custom_nightmare_settings: bool = dictor(_data, "nightmare.enableCustomNightmareSettings", False)
    nightmare_combat_script_name: str = dictor(_data, "nightmare.nightmareCombatScriptName", "")
    nightmare_combat_script: List[str] = dictor(_data, "nightmare.nightmareCombatScript", [])
    nightmare_summon_list: List[str] = dictor(_data, "nightmare.nightmareSummons", [])
    nightmare_summon_elements_list: List[str] = dictor(_data, "nightmare.nightmareSummonElements", [])
    nightmare_group_number: int = dictor(_data, "nightmare.nightmareGroupNumber", 1)
    nightmare_party_number: int = dictor(_data, "nightmare.nightmarePartyNumber", 1)

    _farming_modes_with_nightmares = ["Event", "Event (Token Drawboxes)", "Rise of the Beasts", "Xeno Clash"]

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
            MessageLog.print_message(f"[NIGHTMARE] Reusing settings from Farming Mode for Nightmare...")
            nightmare_combat_script = combat_script
            nightmare_summon_list = summon_list
            nightmare_summon_elements_list = summon_element_list
            nightmare_group_number = group_number
            nightmare_party_number = party_number

        MessageLog.print_message(f"[NIGHTMARE] Settings initialized for {farming_mode}'s Nightmare...")
    # #### end of nightmare ####

    # #### sandbox defender #### #
    enable_defender: bool = dictor(_data, "sandbox.enableDefender", False)
    enable_gold_chest: bool = dictor(_data, "sandbox.enableGoldChest", False)
    _enable_custom_defender_settings: bool = dictor(_data, "sandbox.enableCustomDefenderSettings", False)
    defender_combat_script_name: str = dictor(_data, "sandbox.defenderCombatScriptName", "")
    defender_combat_script: List[str] = dictor(_data, "sandbox.defenderCombatScript", [])
    number_of_defenders: int = dictor(_data, "sandbox.numberOfDefenders", 1)
    defender_group_number: int = dictor(_data, "sandbox.defenderGroupNumber", 1)
    defender_party_number: int = dictor(_data, "sandbox.defenderPartyNumber", 1)
    number_of_defeated_defenders: int = 0
    engaged_defender_battle: bool = False
    # #### end of sandbox defender #### #

    # #### raid ####
    enable_auto_exit_raid: bool = dictor(_data, "raid.enableAutoExitRaid", False)
    time_allowed_until_auto_exit_raid: int = dictor(_data, "raid.timeAllowedUntilAutoExitRaid", 10) * 60
    enable_no_timeout: bool = dictor(_data, "raid.enableNoTimeout", False)
    # #### end of raid ####

    # #### event ####
    event_enable_new_position: bool = dictor(_data, "event.enableNewPosition", False)
    event_new_position: int = dictor(_data, "event.newPosition", 0)
    enable_event_location_incrementation_by_one: bool = dictor(_data, "event.enableLocationIncrementByOne", False)
    enable_select_bottom_category: bool = dictor(_data, "event.selectBottomCategory", False)
    # #### end of event ####

    # #### arcarum ####
    enable_stop_on_arcarum_boss: bool = dictor(_data, "arcarum.enableStopOnArcarumBoss", True)
    # #### end of arcarum ####

    # #### generic ####
    enable_force_reload: bool = dictor(_data, "generic.enableForceReload", False)
    # #### end of generic ####

    # #### xeno clash ####
    xeno_clash_enable_new_position: bool = dictor(_data, "xenoClash.enableNewPosition", False)
    xeno_clash_new_position: int = dictor(_data, "xenoClash.newPosition", 0)
    xeno_clash_select_top_option: bool = dictor(_data, "xenoClash.selectTopOption", False)
    # #### end of xeno clash ####

    # #### proving grounds ####
    proving_grounds_enable_new_position: bool = dictor(_data, "provingGrounds.enableNewPosition", False)
    proving_grounds_new_position: int = dictor(_data, "provingGrounds.newPosition", 0)
    # #### end of proving grounds ####

    # #### guild wars ####
    guild_wars_enable_new_position: bool = dictor(_data, "guildWars.enableNewPosition", False)
    guild_wars_new_position: int = dictor(_data, "guildWars.newPosition", 0)
    # #### end of guild wars ####

    # #### rotb ####
    rotb_enable_new_position: bool = dictor(_data, "rotb.enableNewPosition", False)
    rotb_new_position: int = dictor(_data, "rotb.newPosition", 0)
    # #### end of rotb ####

    # #### adjustment ####
    enable_calibration_adjustment: bool = dictor(_data, "adjustment.enableCalibrationAdjustment", False)
    adjust_calibration: int = dictor(_data, "adjustment.adjustCalibration", 5)
    enable_general_adjustment: bool = dictor(_data, "adjustment.enableGeneralAdjustment", False)
    adjust_button_search_general: int = dictor(_data, "adjustment.adjustButtonSearchGeneral", 5)
    adjust_header_search_general: int = dictor(_data, "adjustment.adjustHeaderSearchGeneral", 5)
    enable_pending_battles_adjustment: bool = dictor(_data, "adjustment.enableForceReload", False)
    adjust_before_pending_battle: int = dictor(_data, "adjustment.adjustBeforePendingBattle", 1)
    adjust_pending_battle: int = dictor(_data, "adjustment.adjustPendingBattle", 2)
    enable_captcha_adjustment: bool = dictor(_data, "adjustment.enableCaptchaAdjustment", False)
    adjust_captcha: int = dictor(_data, "adjustment.adjustCaptcha", 5)
    enable_support_summon_selection_screen_adjustment: bool = dictor(_data, "adjustment.enableSupportSummonSelectionScreenAdjustment", False)
    adjust_support_summon_selection_screen: int = dictor(_data, "adjustment.adjustSupportSummonSelectionScreen", 30)
    enable_combat_mode_adjustment: bool = dictor(_data, "adjustment.enableCombatModeAdjustment", False)
    adjust_combat_start: int = dictor(_data, "adjustment.adjustCombatStart", 50)
    adjust_dialog: int = dictor(_data, "adjustment.adjustDialog", 2)
    adjust_skill_usage: int = dictor(_data, "adjustment.adjustSkillUsage", 5)
    adjust_summon_usage: int = dictor(_data, "adjustment.adjustSummonUsage", 5)
    adjust_waiting_for_reload: int = dictor(_data, "adjustment.adjustWaitingForReload", 3)
    adjust_waiting_for_attack: int = dictor(_data, "adjustment.adjustWaitingForAttack", 100)
    adjust_check_for_no_loot_screen: int = dictor(_data, "adjustment.adjustCheckForNoLootScreen", 1)
    adjust_check_for_battle_concluded_popup: int = dictor(_data, "adjustment.adjustCheckForBattleConcludedPopup", 1)
    adjust_check_for_exp_gained_popup: int = dictor(_data, "adjustment.adjustCheckForExpGainedPopup", 1)
    adjust_check_for_loot_collection_screen: int = dictor(_data, "adjustment.adjustCheckForLootCollectionScreen", 1)
    enable_arcarum_adjustment: bool = dictor(_data, "adjustment.enableArcarumAdjustment", False)
    adjust_arcarum_action: int = dictor(_data, "adjustment.adjustArcarumAction", 3)
    adjust_arcarum_stage_effect: int = dictor(_data, "adjustment.adjustArcarumStageEffect", 10)
    # #### end of adjustment ####

    # #### device ####
    use_first_notch: bool = dictor(_data, "device.useFirstNotch", False)
    confidence: float = dictor(_data, "device.confidence", 0.8)
    confidence_all: float = dictor(_data, "device.confidenceAll", 0.8)
    custom_scale: float = dictor(_data, "device.customScale", 1.0)
    enable_test_for_home_screen = dictor(_data, "device.enableTestForHomeScreen", False)
    # #### end of device ####

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
