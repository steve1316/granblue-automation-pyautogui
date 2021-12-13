from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class XenoClashException(Exception):
    def __init__(self, message):
        super().__init__(message)


class XenoClash:
    """
    Provides the navigation and any necessary utility functions to handle the Xeno Clash game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): The name of the Xeno Clash mission.

    """

    @staticmethod
    def check_for_xeno_clash_nightmare():
        """Checks for Xeno Clash Nightmare and if it appears and the user enabled it in user settings, start it.

        Returns:
            (bool): Return True if Xeno Clash Nightmare was detected and successfully completed. Otherwise, return False.
        """
        from bot.game import Game

        if Settings.enable_nightmare and ImageUtils.confirm_location("limited_time_quests", tries = 1):
            # First check if the Xeno Clash Nightmare is skippable.
            event_claim_loot_location = ImageUtils.find_button("event_claim_loot", tries = 1, suppress_error = True)
            if event_claim_loot_location is not None:
                MessageLog.print_message("\n[XENO] Skippable Xeno Clash Nightmare detected. Claiming it now...")
                MouseUtils.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                Game.collect_loot(is_completed = False, is_event_nightmare = True)
                return True
            else:
                MessageLog.print_message("\n[XENO] Detected Xeno Clash Nightmare. Starting it now...")

                MessageLog.print_message("\n********************************************************************************")
                MessageLog.print_message("********************************************************************************")
                MessageLog.print_message(f"[XENO] Xeno Clash Nightmare")
                MessageLog.print_message(f"[XENO] Xeno Clash Nightmare Summon Elements: {Settings.nightmare_summon_elements_list}")
                MessageLog.print_message(f"[XENO] Xeno Clash Nightmare Summons: {Settings.nightmare_summon_list}")
                MessageLog.print_message(f"[XENO] Xeno Clash Nightmare Group Number: {Settings.nightmare_group_number}")
                MessageLog.print_message(f"[XENO] Xeno Clash Nightmare Party Number: {Settings.nightmare_party_number}")
                MessageLog.print_message(f"[XENO] Xeno Clash Nightmare Combat Script: {Settings.nightmare_combat_script_name}")
                MessageLog.print_message("********************************************************************************")
                MessageLog.print_message("********************************************************************************\n")

                # Click the "Play Next" button to head to the Summon Selection screen.
                Game.find_and_click_button("play_next")

                Game.wait(1)

                # Select only the first Nightmare.
                play_round_buttons = ImageUtils.find_all("play_round_button")
                MouseUtils.move_and_click_point(play_round_buttons[0][0], play_round_buttons[0][1], "play_round_button")

                Game.wait(1)

                # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
                if ImageUtils.confirm_location("select_a_summon"):
                    Game.select_summon(Settings.nightmare_summon_list, Settings.nightmare_summon_elements_list)
                    start_check = Game.find_party_and_start_mission(int(Settings.nightmare_group_number), int(Settings.nightmare_party_number))

                    # Once preparations are completed, start Combat Mode.
                    if start_check and CombatMode.start_combat_mode(is_nightmare = True):
                        Game.collect_loot(is_completed = False, is_event_nightmare = True)
                        return True

        elif not Settings.enable_nightmare and ImageUtils.confirm_location("limited_time_quests", tries = 1):
            # First check if the Xeno Clash Nightmare is skippable.
            event_claim_loot_location = ImageUtils.find_button("event_claim_loot", tries = 1, suppress_error = True)
            if event_claim_loot_location is not None:
                MessageLog.print_message("\n[XENO] Skippable Xeno Clash Nightmare detected but user opted to not run it. Claiming it regardless...")
                MouseUtils.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                Game.collect_loot(is_completed = False, is_event_nightmare = True)
                return True
            else:
                MessageLog.print_message("\n[XENO] Xeno Clash Nightmare detected but user opted to not run it. Moving on...")
                Game.find_and_click_button("close")
        else:
            MessageLog.print_message("\n[XENO] No Xeno Clash Nightmare detected. Moving on...")

        return False

    @staticmethod
    def _navigate():
        """Navigates to the specified Xeno Clash mission.

        Returns:
            None
        """
        from bot.game import Game

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        MessageLog.print_message(f"\n[XENO.CLASH] Now navigating to Xeno Clash...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        Game.find_and_click_button("home_menu")
        event_banner_locations = ImageUtils.find_all("event_banner", custom_confidence = 0.7)
        if len(event_banner_locations) == 0:
            event_banner_locations = ImageUtils.find_all("event_banner_blue", custom_confidence = 0.7)
        MouseUtils.move_and_click_point(event_banner_locations[0][0], event_banner_locations[0][1], "event_banner")

        Game.wait(2.0)

        if Game.find_and_click_button("xeno_special", tries = 30):
            # Check to see if the user already has a Nightmare available.
            nightmare_is_available = 0
            if ImageUtils.find_button("event_nightmare", tries = 1) is not None:
                nightmare_is_available = 1

            # Find all the "Select" buttons.
            select_button_locations = ImageUtils.find_all("select")

            if Settings.mission_name == "Xeno Clash Extreme":
                MessageLog.print_message(f"[XENO.CLASH] Now hosting Xeno Clash Extreme...")
                MouseUtils.move_and_click_point(select_button_locations[1 + nightmare_is_available][0], select_button_locations[1 + nightmare_is_available][1], "select")

                difficulty_button_locations = ImageUtils.find_all("play_round_button")
                MouseUtils.move_and_click_point(difficulty_button_locations[0][0], difficulty_button_locations[0][1], "play_round_button")
            elif Settings.mission_name == "Xeno Clash Raid":
                MessageLog.print_message(f"[XENO.CLASH] Now hosting Xeno Clash Raid...")
                MouseUtils.move_and_click_point(select_button_locations[2 + nightmare_is_available][0], select_button_locations[2 + nightmare_is_available][1], "select")

                Game.wait(2.0)

                Game.find_and_click_button("play")
        else:
            raise(XenoClashException("Failed to open the Xeno Special tab."))

        return None

    @staticmethod
    def start(first_run: bool) -> int:
        """Starts the process to complete a run for Xeno Clash Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of runs completed.
        """
        from bot.game import Game

        runs_completed: int = 0

        # Start the navigation process.
        if first_run:
            XenoClash._navigate()
        elif Game.find_and_click_button("play_again"):
            if Game.check_for_popups():
                XenoClash._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            XenoClash._navigate()

        # Check for AP.
        Game.check_for_ap()

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
            if summon_check:
                # Select the Party.
                Game.find_party_and_start_mission(Settings.group_number, Settings.party_number)

                # Now start Combat Mode and detect any item drops.
                if CombatMode.start_combat_mode():
                    runs_completed = Game.collect_loot(is_completed = True)
        else:
            raise XenoClashException("Failed to arrive at the Summon Selection screen.")

        return runs_completed
