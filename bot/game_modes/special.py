from configparser import ConfigParser


class SpecialException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Special:
    """
    Provides the navigation and any necessary utility functions to handle the Special game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    map_name (str): Name of the Map to look for the specified Mission.

    mission_name (str): Name of the Mission to farm.

    """

    def __init__(self, game, map_name: str, mission_name: str):
        super().__init__()

        self._game = game
        self._map_name: str = map_name
        self._mission_name: str = mission_name

        config = ConfigParser()
        config.read("config.ini")

        ##########################
        # #### Advanced Setup ####
        self._game.print_and_save("\n[SPECIAL] Initializing settings for Dimensional Halo...")

        # #### config.ini ####
        self._enable_dimensional_halo = config.getboolean("dimensional_halo", "enable_dimensional_halo")
        if self._enable_dimensional_halo and self._mission_name == "VH Angel Halo":
            self._dimensional_halo_combat_script = config.get("dimensional_halo", "dimensional_halo_combat_script")

            self._dimensional_halo_summon_list = config.get("dimensional_halo", "dimensional_halo_summon_list").replace(" ", "_").split(",")
            if len(self._dimensional_halo_summon_list) == 1 and self._dimensional_halo_summon_list[0] == "":
                self._dimensional_halo_summon_list.clear()

            self._dimensional_halo_summon_element_list = config.get("dimensional_halo", "dimensional_halo_summon_element_list").replace(" ", "_").split(",")
            if len(self._dimensional_halo_summon_element_list) == 1 and self._dimensional_halo_summon_element_list[0] == "":
                self._dimensional_halo_summon_element_list.clear()

            self._dimensional_halo_group_number = config.get("dimensional_halo", "dimensional_halo_group_number")
            self._dimensional_halo_party_number = config.get("dimensional_halo", "dimensional_halo_party_number")
            self._dimensional_halo_amount = 0

            if self._dimensional_halo_combat_script == "":
                self._game.print_and_save("[SPECIAL] Combat Script for Dimensional Halo will reuse the one for Farming Mode.")
                self._dimensional_halo_combat_script = self._game.combat_script

            if len(self._dimensional_halo_summon_element_list) == 0:
                self._game.print_and_save("[SPECIAL] Summon Elements for Dimensional Halo will reuse the ones for Farming Mode.")
                self._dimensional_halo_summon_element_list = self._game.summon_element_list

            if len(self._dimensional_halo_summon_list) == 0:
                self._game.print_and_save("[SPECIAL] Summons for Dimensional Halo will reuse the ones for Farming Mode.")
                self._dimensional_halo_summon_list = self._game.summon_list

            if self._dimensional_halo_group_number == "":
                self._game.print_and_save("[SPECIAL] Group Number for Dimensional Halo will reuse the one for Farming Mode.")
                self._dimensional_halo_group_number = self._game.group_number
            else:
                self._dimensional_halo_group_number = int(self._dimensional_halo_group_number)

            if self._dimensional_halo_party_number == "":
                self._game.print_and_save("[SPECIAL] Party Number for Dimensional Halo will reuse the one for Farming Mode.")
                self._dimensional_halo_party_number = self._game.party_number
            else:
                self._dimensional_halo_party_number = int(self._dimensional_halo_party_number)
        # #### end of config.ini ####

        self._game.print_and_save("[SPECIAL] Settings initialized for Special...")
        # #### end of Advanced Setup ####
        #################################

    def check_for_dimensional_halo(self):
        """Checks for Dimensional Halo and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Dimensional Halo was detected and successfully completed. Otherwise, return False.
        """
        if self._enable_dimensional_halo and self._game.image_tools.confirm_location("limited_time_quests", tries = 1):
            self._game.print_and_save("\n[D.HALO] Detected Dimensional Halo. Starting it now...")
            self._dimensional_halo_amount += 1

            self._game.print_and_save("\n********************************************************************************")
            self._game.print_and_save("********************************************************************************")
            self._game.print_and_save(f"[D.HALO] Dimensional Halo")
            self._game.print_and_save(f"[D.HALO] Dimensional Halo Summon Elements: {self._dimensional_halo_summon_element_list}")
            self._game.print_and_save(f"[D.HALO] Dimensional Halo Summons: {self._dimensional_halo_summon_list}")
            self._game.print_and_save(f"[D.HALO] Dimensional Halo Group Number: {self._dimensional_halo_group_number}")
            self._game.print_and_save(f"[D.HALO] Dimensional Halo Party Number: {self._dimensional_halo_party_number}")
            self._game.print_and_save(f"[D.HALO] Dimensional Halo Combat Script: {self._dimensional_halo_combat_script}")
            self._game.print_and_save(f"[D.HALO] Amount of Dimensional Halos encountered: {self._dimensional_halo_amount}")
            self._game.print_and_save("********************************************************************************")
            self._game.print_and_save("********************************************************************************\n")

            # Click the "Play Next" button to head to the Summon Selection screen.
            self._game.find_and_click_button("play_next")

            self._game.wait(1)

            # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
            if self._game.image_tools.confirm_location("select_a_summon"):
                self._game.select_summon(self._dimensional_halo_summon_list, self._dimensional_halo_summon_element_list)
                start_check = self._game.find_party_and_start_mission(int(self._dimensional_halo_group_number), int(self._dimensional_halo_party_number))

                # Once preparations are completed, start Combat Mode.
                if start_check and self._game.combat_mode.start_combat_mode(self._dimensional_halo_combat_script, is_nightmare = True):
                    self._game.collect_loot(is_completed = False, is_event_nightmare = True)
                    return True

        elif not self._enable_dimensional_halo and self._game.image_tools.confirm_location("limited_time_quests", tries = 1):
            self._game.print_and_save("\n[D.HALO] Dimensional Halo detected but user opted to not run it. Moving on...")
            self._game.find_and_click_button("close")
        else:
            self._game.print_and_save("\n[D.HALO] No Dimensional Halo detected. Moving on...")

        return False

    def _navigate(self):
        """Navigates to the specified Special mission.

        Returns:
            None
        """
        self._game.print_and_save(f"\n[SPECIAL] Beginning process to navigate to the mission: {self._mission_name}...")

        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Go to the Quest screen.
        self._game.find_and_click_button("quest", suppress_error = True)

        # Check for the "You retreated from the raid battle" popup.
        self._game.wait(1)
        if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 1):
            self._game.find_and_click_button("ok")

        if self._game.image_tools.confirm_location("quest"):
            # Go to the Special screen.
            self._game.find_and_click_button("special")

            # Remove the difficulty prefix from the mission name.
            difficulty = ""
            formatted_mission_name = ""
            if self._mission_name.find("N ") == 0:
                difficulty = "Normal"
                formatted_mission_name = self._mission_name[2:]
            elif self._mission_name.find("H ") == 0:
                difficulty = "Hard"
                formatted_mission_name = self._mission_name[2:]
            elif self._mission_name.find("VH ") == 0:
                difficulty = "Very Hard"
                formatted_mission_name = self._mission_name[3:]
            elif self._mission_name.find("EX ") == 0:
                difficulty = "Extreme"
                formatted_mission_name = self._mission_name[3:]
            else:
                formatted_mission_name = self._mission_name

            if self._game.image_tools.confirm_location("special"):
                tries = 2

                # Try to select the specified Special mission for a number of tries.
                while tries != 0:
                    # Scroll the screen down if its any of the Special Quests that are more towards the bottom of the page to alleviate problems for smaller screens.
                    if self._map_name != "Campaign-Exclusive Quest" and self._map_name != "Basic Treasure Quests" and self._map_name != "Shiny Slime Search!" and self._map_name != "Six Dragon Trial":
                        self._game.mouse_tools.scroll_screen_from_home_button(-500)

                    mission_select_button = self._game.image_tools.find_button(self._map_name.lower().replace(" ", "_").replace("-", "_"))
                    if mission_select_button is not None:
                        self._game.print_and_save(f"[SPECIAL] Navigating to {self._map_name}...")

                        # Move to the specified Special by clicking its "Select" button.
                        special_quest_select_button = (mission_select_button[0] + 145, mission_select_button[1] + 75)
                        self._game.mouse_tools.move_and_click_point(special_quest_select_button[0], special_quest_select_button[1], "select")

                        self._game.wait(1)

                        if self._map_name == "Basic Treasure Quests":
                            locations = self._game.image_tools.find_all("play_round_button")

                            if formatted_mission_name == "Scarlet Trial":
                                # Navigate to Scarlet Trial.
                                self._game.print_and_save(f"[SPECIAL] Selecting Scarlet Trial...")
                                self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif formatted_mission_name == "Cerulean Trial":
                                # Navigate to Cerulean Trial.
                                self._game.print_and_save(f"[SPECIAL] Selecting Cerulean Trial...")
                                self._game.mouse_tools.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif formatted_mission_name == "Violet Trial":
                                # Navigate to Violet Trial.
                                self._game.print_and_save(f"[SPECIAL] Selecting Violet Trial...")
                                self._game.mouse_tools.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                            self._game.wait(1)

                            # Now start the Trial with the specified difficulty.
                            self._game.print_and_save(f"[SPECIAL] Now navigating to {difficulty}...")
                            locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                self._game.mouse_tools.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif self._map_name == "Shiny Slime Search!":
                            # Start up the Shiny Slime Search! mission by selecting its difficulty.
                            self._game.print_and_save(f"[SPECIAL] Selecting {difficulty} Shiny Slime Search!...")
                            locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                self._game.mouse_tools.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif self._map_name == "Six Dragon Trial":
                            # Start up the Six Dragon Trial mission by selecting its difficulty.
                            self._game.print_and_save(f"[SPECIAL] Selecting {difficulty} Six Dragon Trial...")
                            locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                self._game.mouse_tools.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif self._map_name == "Elemental Treasure Quests":
                            # Start up the specified Elemental Treasure Quest mission.
                            self._game.print_and_save(f"[SPECIAL] Selecting {self._mission_name}...")
                            locations = self._game.image_tools.find_all("play_round_button")

                            if formatted_mission_name == "The Hellfire Trial":
                                self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif formatted_mission_name == "The Deluge Trial":
                                self._game.mouse_tools.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif formatted_mission_name == "The Wasteland Trial":
                                self._game.mouse_tools.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")
                            elif formatted_mission_name == "The Typhoon Trial":
                                self._game.mouse_tools.move_and_click_point(locations[3][0], locations[3][1], "play_round_button")
                            elif formatted_mission_name == "The Aurora Trial":
                                self._game.mouse_tools.move_and_click_point(locations[4][0], locations[4][1], "play_round_button")
                            elif formatted_mission_name == "The Oblivion Trial":
                                self._game.mouse_tools.move_and_click_point(locations[5][0], locations[5][1], "play_round_button")

                        elif self._map_name == "Showdowns":
                            locations = self._game.image_tools.find_all("play_round_button")

                            if formatted_mission_name == "Ifrit Showdown":
                                # Navigate to Ifrit Showdown.
                                self._game.print_and_save(f"[SPECIAL] Selecting Ifrit Showdown...")
                                self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif formatted_mission_name == "Cocytus Showdown":
                                # Navigate to Cocytus Showdown.
                                self._game.print_and_save(f"[SPECIAL] Selecting Cocytus Showdown...")
                                self._game.mouse_tools.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif formatted_mission_name == "Vohu Manah Showdown":
                                # Navigate to Vohu Manah Showdown.
                                self._game.print_and_save(f"[SPECIAL] Selecting Vohu Manah Showdown...")
                                self._game.mouse_tools.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")
                            elif formatted_mission_name == "Sagittarius Showdown":
                                # Navigate to Sagittarius Showdown.
                                self._game.print_and_save(f"[SPECIAL] Selecting Sagittarius Showdown...")
                                self._game.mouse_tools.move_and_click_point(locations[3][0], locations[3][1], "play_round_button")
                            elif formatted_mission_name == "Corow Showdown":
                                # Navigate to Corow Showdown.
                                self._game.print_and_save(f"[SPECIAL] Selecting Corow Showdown...")
                                self._game.mouse_tools.move_and_click_point(locations[4][0], locations[4][1], "play_round_button")
                            elif formatted_mission_name == "Diablo Showdown":
                                # Navigate to Diablo Showdown.
                                self._game.print_and_save(f"[SPECIAL] Selecting Diablo Showdown...")
                                self._game.mouse_tools.move_and_click_point(locations[5][0], locations[5][1], "play_round_button")

                            # Now start the Showdown with the specified difficulty.
                            self._game.wait(1)
                            self._game.print_and_save(f"[SPECIAL] Now navigating to {difficulty}...")
                            locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                self._game.mouse_tools.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Extreme":
                                self._game.mouse_tools.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        elif self._map_name == "Campaign-Exclusive Quest":
                            self._game.print_and_save(f"[SPECIAL] Selecting Campaign-Exclusive Quest...")
                            locations = self._game.image_tools.find_all("play_round_button")

                            # There is only one round "Play" button for this time-limited quest.
                            self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")

                        else:
                            # Start up the Angel Halo mission by selecting its difficulty.
                            self._game.print_and_save(f"[SPECIAL] Selecting {difficulty} Angel Halo...")
                            locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                self._game.mouse_tools.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                self._game.mouse_tools.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")

                        break
                    else:
                        # Scroll the screen down more if on a smaller screen and it obscures the targeted mission.
                        self._game.mouse_tools.scroll_screen(self._game.home_button_location[0], self._game.home_button_location[1] - 50, -500)
                        tries -= 1

        return None

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Special Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of items detected.
        """
        number_of_items_dropped: int = 0

        # Start the navigation process.
        if first_run:
            self._navigate()
        elif self._game.find_and_click_button("play_again"):
            if self._game.check_for_popups():
                self._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            self._game.check_for_pending()
            self._navigate()

        # Check for AP.
        self._game.check_for_ap()

        # Check if the bot is at the Summon Selection screen.
        if self._game.image_tools.confirm_location("select_a_summon"):
            summon_check = self._game.select_summon(self._game.summon_list, self._game.summon_element_list)
            if summon_check:
                # Select the Party.
                self._game.find_party_and_start_mission(self._game.group_number, self._game.party_number)

                self._game.wait(1)

                # Now start Combat Mode and detect any item drops.
                if self._game.combat_mode.start_combat_mode(self._game.combat_script):
                    number_of_items_dropped = self._game.collect_loot(is_completed = True)
        else:
            raise SpecialException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
