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

        if Settings.enable_nightmare and ImageUtils.confirm_location("limited_time_quests", tries = 1):
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
            if ImageUtils.confirm_location("select_a_summon"):
                Game.select_summon(Settings.nightmare_summon_list, Settings.nightmare_summon_elements_list)
                start_check = Game.find_party_and_start_mission(int(Settings.nightmare_group_number), int(Settings.nightmare_party_number))

                # Once preparations are completed, start Combat Mode.
                if start_check and CombatMode.start_combat_mode(is_nightmare = True):
                    Game.collect_loot(is_completed = False, is_event_nightmare = True)
                    return True

        elif not Settings.enable_nightmare and ImageUtils.confirm_location("limited_time_quests", tries = 1):
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
        Game.wait(1)
        if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 1):
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
                    # Scroll the screen down if its any of the Special Quests that are more towards the bottom of the page to alleviate problems for smaller screens.
                    if Settings.map_name != "Campaign-Exclusive Quest" and Settings.map_name != "Basic Treasure Quests" and Settings.map_name != "Shiny Slime Search!" and Settings.map_name != "Six Dragon Trial":
                        MouseUtils.scroll_screen_from_home_button(-500)

                    mission_select_button = ImageUtils.find_button(Settings.map_name.lower().replace(" ", "_").replace("-", "_"))
                    if mission_select_button is not None:
                        MessageLog.print_message(f"[SPECIAL] Navigating to {Settings.map_name}...")

                        # Move to the specified Special by clicking its "Select" button.
                        special_quest_select_button = (mission_select_button[0] + 145, mission_select_button[1] + 75)
                        MouseUtils.move_and_click_point(special_quest_select_button[0], special_quest_select_button[1], "select")

                        Game.wait(1)

                        if Settings.map_name == "Basic Treasure Quests":
                            locations = ImageUtils.find_all("play_round_button")

                            if formatted_mission_name == "Scarlet Trial":
                                # Navigate to Scarlet Trial.
                                MessageLog.print_message(f"[SPECIAL] Selecting Scarlet Trial...")
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif formatted_mission_name == "Cerulean Trial":
                                # Navigate to Cerulean Trial.
                                MessageLog.print_message(f"[SPECIAL] Selecting Cerulean Trial...")
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif formatted_mission_name == "Violet Trial":
                                # Navigate to Violet Trial.
                                MessageLog.print_message(f"[SPECIAL] Selecting Violet Trial...")
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

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
                            locations = ImageUtils.find_all("play_round_button")

                            if difficulty == "Normal":
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif Settings.map_name == "Six Dragon Trial":
                            # Start up the Six Dragon Trial mission by selecting its difficulty.
                            MessageLog.print_message(f"[SPECIAL] Selecting {difficulty} Six Dragon Trial...")
                            locations = ImageUtils.find_all("play_round_button")

                            if difficulty == "Normal":
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif Settings.map_name == "Elemental Treasure Quests":
                            # Start up the specified Elemental Treasure Quest mission.
                            MessageLog.print_message(f"[SPECIAL] Selecting {Settings.mission_name}...")
                            locations = ImageUtils.find_all("play_round_button")

                            if formatted_mission_name == "The Hellfire Trial":
                                MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif formatted_mission_name == "The Deluge Trial":
                                MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif formatted_mission_name == "The Wasteland Trial":
                                MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")
                            elif formatted_mission_name == "The Typhoon Trial":
                                MouseUtils.move_and_click_point(locations[3][0], locations[3][1], "play_round_button")
                            elif formatted_mission_name == "The Aurora Trial":
                                MouseUtils.move_and_click_point(locations[4][0], locations[4][1], "play_round_button")
                            elif formatted_mission_name == "The Oblivion Trial":
                                MouseUtils.move_and_click_point(locations[5][0], locations[5][1], "play_round_button")

                        elif Settings.map_name == "Showdowns":
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
                            locations = ImageUtils.find_all("play_round_button")

                            # There is only one round "Play" button for this time-limited quest.
                            MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")

                        else:
                            # Start up the Angel Halo mission by selecting its difficulty.
                            MessageLog.print_message(f"[SPECIAL] Selecting {difficulty} Angel Halo...")
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

        return None

    @staticmethod
    def start(first_run: bool) -> int:
        """Starts the process to complete a run for Special Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of items detected.
        """
        from bot.game import Game

        number_of_items_dropped: int = 0

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
                    number_of_items_dropped = Game.collect_loot(is_completed = True)
        else:
            raise SpecialException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
