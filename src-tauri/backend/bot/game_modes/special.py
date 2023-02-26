from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class SpecialException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Special:
    """
    Provides the navigation and any necessary utility functions to handle the Special game mode.
    """

    _dimensional_halo_amount = 0

    @staticmethod
    def check_for_dimensional_halo():
        """Checks for Dimensional Halo and if it appears and the user enabled it in user settings, start it.

        Returns:
            (bool): Return True if Dimensional Halo was detected and successfully completed. Otherwise, return False.
        """
        from bot.game import Game

        if Settings.enable_nightmare and ImageUtils.confirm_location("limited_time_quests", tries = 3):
            MessageLog.print_message("\n[D.HALO] Detected Dimensional Halo. Starting it now...")
            Special._dimensional_halo_amount += 1

            MessageLog.print_message("\n********************************************************************************")
            MessageLog.print_message("********************************************************************************")
            MessageLog.print_message(f"[D.HALO] Dimensional Halo")
            MessageLog.print_message(f"[D.HALO] Dimensional Halo Summon Elements: {Settings.nightmare_summon_elements_list}")
            MessageLog.print_message(f"[D.HALO] Dimensional Halo Summons: {Settings.nightmare_summon_list}")
            MessageLog.print_message(f"[D.HALO] Dimensional Halo Group Number: {Settings.nightmare_group_number}")
            MessageLog.print_message(f"[D.HALO] Dimensional Halo Party Number: {Settings.nightmare_party_number}")
            MessageLog.print_message(f"[D.HALO] Dimensional Halo Combat Script: {Settings.nightmare_combat_script_name}")
            MessageLog.print_message("********************************************************************************")
            MessageLog.print_message("********************************************************************************\n")

            # Click the "Play Next" button to head to the Summon Selection screen.
            Game.find_and_click_button("play_next")

            Game.wait(1)

            # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
            if ImageUtils.confirm_location("select_a_summon", tries = 30):
                Game.select_summon(Settings.nightmare_summon_list, Settings.nightmare_summon_elements_list)
                start_check = Game.find_party_and_start_mission(int(Settings.nightmare_group_number), int(Settings.nightmare_party_number), bypass_first_run = True)

                # Once preparations are completed, start Combat Mode.
                if start_check and CombatMode.start_combat_mode(is_nightmare = True):
                    Game.collect_loot(is_completed = False, is_event_nightmare = True)
                    return True

        elif not Settings.enable_nightmare and ImageUtils.confirm_location("limited_time_quests", tries = 3):
            MessageLog.print_message("\n[D.HALO] Dimensional Halo detected but user opted to not run it. Moving on...")
            Game.find_and_click_button("close")
        else:
            MessageLog.print_message("\n[D.HALO] No Dimensional Halo detected. Moving on...")

        return False

    @staticmethod
    def _navigate():
        """Navigates to the specified Special mission.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[SPECIAL] Beginning process to navigate to the mission: {Settings.mission_name}...")

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        # Go to the Quest screen.
        Game.find_and_click_button("quest", suppress_error = True)

        # Check for the "You retreated from the raid battle" popup.
        Game.wait(3.0)
        if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
            Game.find_and_click_button("ok")

        if ImageUtils.confirm_location("quest"):
            # Go to the Special screen.
            Game.find_and_click_button("special")

            # Remove the difficulty prefix from the mission name.
            difficulty = ""
            if Settings.mission_name.find("N ") == 0:
                difficulty = "Normal"
                formatted_mission_name = Settings.mission_name[2:]
            elif Settings.mission_name.find("H ") == 0:
                difficulty = "Hard"
                formatted_mission_name = Settings.mission_name[2:]
            elif Settings.mission_name.find("VH ") == 0:
                difficulty = "Very Hard"
                formatted_mission_name = Settings.mission_name[3:]
            elif Settings.mission_name.find("EX ") == 0:
                difficulty = "Extreme"
                formatted_mission_name = Settings.mission_name[3:]
            else:
                formatted_mission_name = Settings.mission_name

            if ImageUtils.confirm_location("special"):
                tries = 2

                # Try to select the specified Special mission for a number of tries.
                while tries != 0:
                    scrolled = False
                    # Scroll the screen down if its any of the Special Quests that are more towards the bottom of the page to alleviate problems for smaller screens.
                    if Settings.map_name != "Campaign-Exclusive Quest" and Settings.map_name != "Uncap Treasure Quests" and Settings.map_name != "Shiny Slime Search!":
                        MouseUtils.scroll_screen_from_home_button(-500)
                        scrolled = True

                    mission_select_button = ImageUtils.find_button(Settings.map_name.lower().replace(" ", "_").replace("-", "_"))
                    if mission_select_button is not None:
                        MessageLog.print_message(f"[SPECIAL] Navigating to {Settings.map_name}...")

                        # Find all instances of the Select button.
                        select_buttons = ImageUtils.find_all("select")
                        if scrolled is False and Settings.map_name != "Campaign-Exclusive Quest" and \
                                ImageUtils.find_button("Campaign-Exclusive Quest".lower().replace(" ", "_").replace("-", "_")) is not None:
                            select_buttons.pop(0)

                        if Settings.map_name == "Uncap Treasure Quests":
                            MouseUtils.move_and_click_point(select_buttons[0][0], select_buttons[0][1], "select")
                            Game.wait(1)

                            locations = ImageUtils.find_all("play_round_button")

                            if formatted_mission_name == "Fire Trial":
                                MessageLog.print_message(f"[SPECIAL] Selecting Fire Trial...")
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif formatted_mission_name == "Water Trial":
                                MessageLog.print_message(f"[SPECIAL] Selecting Water Trial...")
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif formatted_mission_name == "Earth Trial":
                                MessageLog.print_message(f"[SPECIAL] Selecting Earth Trial...")
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")
                            elif formatted_mission_name == "Wind Trial":
                                MessageLog.print_message(f"[SPECIAL] Selecting Wind Trial...")
                                MouseUtils.move_and_click_point(locations[3][0], locations[3][1], "play_round_button")
                            elif formatted_mission_name == "Light Trial":
                                MessageLog.print_message(f"[SPECIAL] Selecting Light Trial...")
                                MouseUtils.move_and_click_point(locations[4][0], locations[4][1], "play_round_button")
                            elif formatted_mission_name == "Dark Trial":
                                MessageLog.print_message(f"[SPECIAL] Selecting Dark Trial...")
                                MouseUtils.move_and_click_point(locations[5][0], locations[5][1], "play_round_button")

                            Game.wait(1)

                            # Now start the Trial with the specified difficulty.
                            MessageLog.print_message(f"[SPECIAL] Now navigating to {difficulty}...")
                            locations = ImageUtils.find_all("play_round_button")

                            if difficulty == "Normal":
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif Settings.map_name == "Shiny Slime Search!":
                            # Start up the Shiny Slime Search! mission by selecting its difficulty.
                            MessageLog.print_message(f"[SPECIAL] Selecting {difficulty} Shiny Slime Search!...")

                            MouseUtils.move_and_click_point(select_buttons[1][0], select_buttons[1][1], "select")
                            Game.wait(1)

                            locations = ImageUtils.find_all("play_round_button")

                            if difficulty == "Normal":
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif Settings.map_name == "Showdowns":
                            if scrolled: MouseUtils.move_and_click_point(select_buttons[len(select_buttons) - 1 - 2][0], select_buttons[len(select_buttons) - 1 - 2][1], "select")
                            else: MouseUtils.move_and_click_point(select_buttons[2][0], select_buttons[2][1], "select")
                            Game.wait(1)

                            locations = ImageUtils.find_all("play_round_button")

                            if formatted_mission_name == "Ifrit Showdown":
                                # Navigate to Ifrit Showdown.
                                MessageLog.print_message(f"[SPECIAL] Selecting Ifrit Showdown...")
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif formatted_mission_name == "Cocytus Showdown":
                                # Navigate to Cocytus Showdown.
                                MessageLog.print_message(f"[SPECIAL] Selecting Cocytus Showdown...")
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif formatted_mission_name == "Vohu Manah Showdown":
                                # Navigate to Vohu Manah Showdown.
                                MessageLog.print_message(f"[SPECIAL] Selecting Vohu Manah Showdown...")
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")
                            elif formatted_mission_name == "Sagittarius Showdown":
                                # Navigate to Sagittarius Showdown.
                                MessageLog.print_message(f"[SPECIAL] Selecting Sagittarius Showdown...")
                                MouseUtils.move_and_click_point(locations[3][0], locations[3][1], "play_round_button")
                            elif formatted_mission_name == "Corow Showdown":
                                # Navigate to Corow Showdown.
                                MessageLog.print_message(f"[SPECIAL] Selecting Corow Showdown...")
                                MouseUtils.move_and_click_point(locations[4][0], locations[4][1], "play_round_button")
                            elif formatted_mission_name == "Diablo Showdown":
                                # Navigate to Diablo Showdown.
                                MessageLog.print_message(f"[SPECIAL] Selecting Diablo Showdown...")
                                MouseUtils.move_and_click_point(locations[5][0], locations[5][1], "play_round_button")

                            # Now start the Showdown with the specified difficulty.
                            Game.wait(1)
                            MessageLog.print_message(f"[SPECIAL] Now navigating to {difficulty}...")
                            locations = ImageUtils.find_all("play_round_button")

                            if difficulty == "Hard":
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Extreme":
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif Settings.map_name == "Campaign-Exclusive Quest":
                            MessageLog.print_message(f"[SPECIAL] Selecting Campaign-Exclusive Quest...")

                            MouseUtils.move_and_click_point(select_buttons[0][0], select_buttons[0][1], "select")
                            Game.wait(1)

                            locations = ImageUtils.find_all("play_round_button")

                            # There is only one round "Play" button for this time-limited quest.
                            MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")

                        else:
                            # Start up the Angel Halo mission by selecting its difficulty.
                            MessageLog.print_message(f"[SPECIAL] Selecting {difficulty} Angel Halo...")

                            if scrolled: MouseUtils.move_and_click_point(select_buttons[len(select_buttons) - 1 - 1][0], select_buttons[len(select_buttons) - 1 - 1][1], "select")
                            else: MouseUtils.move_and_click_point(select_buttons[3][0], select_buttons[3][1], "select")
                            Game.wait(1)

                            locations = ImageUtils.find_all("play_round_button")

                            if difficulty == "Normal":
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        break
                    else:
                        # Scroll the screen down more if on a smaller screen and it obscures the targeted mission.
                        MouseUtils.scroll_screen(Settings.home_button_location[0], Settings.home_button_location[1] - 50, -500)
                        tries -= 1
            else:
                raise SpecialException("Failed to arrive at the Special page to continue with Special navigation.")
        else:
            raise SpecialException("Failed to arrive at the Quest page to continue with Special navigation.")

        return None

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Special Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            Special._navigate()
        elif Game.find_and_click_button("play_again"):
            if Game.check_for_popups():
                Special._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            Special._navigate()

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
                    Game.collect_loot(is_completed = True)
        else:
            raise SpecialException("Failed to arrive at the Summon Selection screen.")

        return None
