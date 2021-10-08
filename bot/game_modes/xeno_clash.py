from configparser import ConfigParser


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

    def __init__(self, game, mission_name: str):
        super().__init__()

        self._game = game
        self._mission_name: str = mission_name

        config = ConfigParser()
        config.read("config.ini")

        #########################
        # #### Advanced Setup ####
        self._game.print_and_save("\n[XENO.CLASH] Initializing settings for Xeno Clash Nightmare...")

        # #### config.ini ####
        self._enable_xeno_clash_nightmare = config.getboolean("xeno_clash", "enable_xeno_clash_nightmare")
        if self._enable_xeno_clash_nightmare:
            self._xeno_clash_nightmare_combat_script = config.get("xeno_clash", "xeno_clash_nightmare_combat_script")

            self._xeno_clash_nightmare_summon_list = config.get("xeno_clash", "xeno_clash_nightmare_summon_list").replace(" ", "_").split(",")
            if len(self._xeno_clash_nightmare_summon_list) == 1 and self._xeno_clash_nightmare_summon_list[0] == "":
                self._xeno_clash_nightmare_summon_list.clear()

            self._xeno_clash_nightmare_summon_element_list = config.get("xeno_clash", "xeno_clash_nightmare_summon_element_list").replace(" ", "_").split(",")
            if len(self._xeno_clash_nightmare_summon_element_list) == 1 and self._xeno_clash_nightmare_summon_element_list[0] == "":
                self._xeno_clash_nightmare_summon_element_list.clear()

            self._xeno_clash_nightmare_group_number = config.get("xeno_clash", "xeno_clash_nightmare_group_number")
            self._xeno_clash_nightmare_party_number = config.get("xeno_clash", "xeno_clash_nightmare_party_number")

            if self._xeno_clash_nightmare_combat_script == "":
                self._game.print_and_save("[XENO.CLASH] Combat Script for Xeno Clash Nightmare will reuse the one for Farming Mode.")
                self._xeno_clash_nightmare_combat_script = self._game.combat_script

            if len(self._xeno_clash_nightmare_summon_element_list) == 0:
                self._game.print_and_save("[XENO.CLASH] Summon Elements for Xeno Clash Nightmare will reuse the ones for Farming Mode.")
                self._xeno_clash_nightmare_summon_element_list = self._game.summon_element_list

            if len(self._xeno_clash_nightmare_summon_list) == 0:
                self._game.print_and_save("[XENO.CLASH] Summons for Xeno Clash Nightmare will reuse the ones for Farming Mode.")
                self._xeno_clash_nightmare_summon_list = self._game.summon_list

            if self._xeno_clash_nightmare_group_number == "":
                self._game.print_and_save("[XENO.CLASH] Group Number for Xeno Clash Nightmare will reuse the one for Farming Mode.")
                self._xeno_clash_nightmare_group_number = self._game.group_number
            else:
                self._xeno_clash_nightmare_number = int(self._xeno_clash_nightmare_group_number)

            if self._xeno_clash_nightmare_party_number == "":
                self._game.print_and_save("[XENO.CLASH] Party Number for Xeno Clash Nightmare will reuse the one for Farming Mode.")
                self._xeno_clash_nightmare_party_number = self._game.party_number
            else:
                self._xeno_clash_nightmare_party_number = int(self._xeno_clash_nightmare_party_number)
        # #### end of config.ini ####

        self._game.print_and_save("[XENO.CLASH] Settings initialized for Xeno Clash Nightmare...")
        # #### end of Advanced Setup ####
        #################################

    def check_for_xeno_clash_nightmare(self):
        """Checks for Xeno Clash Nightmare and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Xeno Clash Nightmare was detected and successfully completed. Otherwise, return False.
        """
        if self._enable_xeno_clash_nightmare and self._game.image_tools.confirm_location("limited_time_quests", tries = 1):
            # First check if the Xeno Clash Nightmare is skippable.
            event_claim_loot_location = self._game.image_tools.find_button("event_claim_loot", tries = 1, suppress_error = True)
            if event_claim_loot_location is not None:
                self._game.print_and_save("\n[XENO] Skippable Xeno Clash Nightmare detected. Claiming it now...")
                self._game.mouse_tools.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                self._game.collect_loot(is_completed = False, is_event_nightmare = True)
                return True
            else:
                self._game.print_and_save("\n[XENO] Detected Xeno Clash Nightmare. Starting it now...")

                self._game.print_and_save("\n********************************************************************************")
                self._game.print_and_save("********************************************************************************")
                self._game.print_and_save(f"[XENO] Xeno Clash Nightmare")
                self._game.print_and_save(f"[XENO] Xeno Clash Nightmare Summon Elements: {self._xeno_clash_nightmare_summon_element_list}")
                self._game.print_and_save(f"[XENO] Xeno Clash Nightmare Summons: {self._xeno_clash_nightmare_summon_list}")
                self._game.print_and_save(f"[XENO] Xeno Clash Nightmare Group Number: {self._xeno_clash_nightmare_group_number}")
                self._game.print_and_save(f"[XENO] Xeno Clash Nightmare Party Number: {self._xeno_clash_nightmare_party_number}")
                self._game.print_and_save(f"[XENO] Xeno Clash Nightmare Combat Script: {self._xeno_clash_nightmare_combat_script}")
                self._game.print_and_save("********************************************************************************")
                self._game.print_and_save("********************************************************************************\n")

                # Click the "Play Next" button to head to the Summon Selection screen.
                self._game.find_and_click_button("play_next")

                self._game.wait(1)

                # Select only the first Nightmare.
                play_round_buttons = self._game.image_tools.find_all("play_round_button")
                self._game.mouse_tools.move_and_click_point(play_round_buttons[0][0], play_round_buttons[0][1], "play_round_button")

                self._game.wait(1)

                # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
                if self._game.image_tools.confirm_location("select_a_summon"):
                    self._game.select_summon(self._xeno_clash_nightmare_summon_list, self._xeno_clash_nightmare_summon_element_list)
                    start_check = self._game.find_party_and_start_mission(int(self._xeno_clash_nightmare_group_number), int(self._xeno_clash_nightmare_party_number))

                    # Once preparations are completed, start Combat Mode.
                    if start_check and self._game.combat_mode.start_combat_mode(self._xeno_clash_nightmare_combat_script, is_nightmare = True):
                        self._game.collect_loot(is_completed = False, is_event_nightmare = True)
                        return True

        elif not self._enable_xeno_clash_nightmare and self._game.image_tools.confirm_location("limited_time_quests", tries = 1):
            # First check if the Xeno Clash Nightmare is skippable.
            event_claim_loot_location = self._game.image_tools.find_button("event_claim_loot", tries = 1, suppress_error = True)
            if event_claim_loot_location is not None:
                self._game.print_and_save("\n[XENO] Skippable Xeno Clash Nightmare detected but user opted to not run it. Claiming it regardless...")
                self._game.mouse_tools.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                self._game.collect_loot(is_completed = False, is_event_nightmare = True)
                return True
            else:
                self._game.print_and_save("\n[XENO] Xeno Clash Nightmare detected but user opted to not run it. Moving on...")
                self._game.find_and_click_button("close")
        else:
            self._game.print_and_save("\n[XENO] No Xeno Clash Nightmare detected. Moving on...")

        return False

    def _navigate(self):
        """Navigates to the specified Xeno Clash mission.

        Returns:
            None
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        self._game.print_and_save(f"\n[XENO.CLASH] Now navigating to Xeno Clash...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        event_banner_locations = self._game.image_tools.find_all("event_banner", custom_confidence = 0.7)
        if len(event_banner_locations) == 0:
            event_banner_locations = self._game.image_tools.find_all("event_banner_blue", custom_confidence = 0.7)
        self._game.mouse_tools.move_and_click_point(event_banner_locations[0][0], event_banner_locations[0][1], "event_banner")

        self._game.wait(1)

        if self._game.find_and_click_button("xeno_special"):
            # Check to see if the user already has a Nightmare available.
            nightmare_is_available = 0
            if self._game.image_tools.find_button("event_nightmare", tries = 1) is not None:
                nightmare_is_available = 1

            # Find all the "Select" buttons.
            select_button_locations = self._game.image_tools.find_all("select")

            if self._mission_name == "Xeno Clash Extreme":
                self._game.print_and_save(f"[XENO.CLASH] Now hosting Xeno Clash Extreme...")
                self._game.mouse_tools.move_and_click_point(select_button_locations[1 + nightmare_is_available][0], select_button_locations[1 + nightmare_is_available][1], "select")

                difficulty_button_locations = self._game.image_tools.find_all("play_round_button")
                self._game.mouse_tools.move_and_click_point(difficulty_button_locations[0][0], difficulty_button_locations[0][1], "play_round_button")
            elif self._mission_name == "Xeno Clash Raid":
                self._game.print_and_save(f"[XENO.CLASH] Now hosting Xeno Clash Raid...")
                self._game.mouse_tools.move_and_click_point(select_button_locations[2 + nightmare_is_available][0], select_button_locations[2 + nightmare_is_available][1], "select")

                self._game.wait(1)

                self._game.find_and_click_button("play")

        return None

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Xeno Clash Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of runs completed.
        """
        runs_completed: int = 0

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
                    runs_completed = self._game.collect_loot(is_completed = True)
        else:
            raise XenoClashException("Failed to arrive at the Summon Selection screen.")

        return runs_completed
