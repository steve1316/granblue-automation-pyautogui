from configparser import ConfigParser


class RiseOfTheBeastsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RiseOfTheBeasts:
    """
    Provides the navigation and any necessary utility functions to handle the Rise of the Beasts game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): The name of the Rise of the Beasts mission.

    """

    def __init__(self, game, mission_name: str):
        super().__init__()

        self._game = game
        self._mission_name: str = mission_name

        config = ConfigParser()
        config.read("config.ini")

        ##########################
        # #### Advanced Setup ####
        self._game.print_and_save("\n[ROTB] Initializing settings for Rise of the Beasts Extreme+...")

        # #### config.ini ####
        self._enable_rotb_extreme_plus = config.getboolean("rise_of_the_beasts", "enable_rotb_extreme_plus")
        if self._enable_rotb_extreme_plus:
            self._rotb_extreme_plus_combat_script = config.get("rise_of_the_beasts", "rotb_extreme_plus_combat_script")

            self._rotb_extreme_plus_summon_list = config.get("rise_of_the_beasts", "rotb_extreme_plus_summon_list").replace(" ", "_").split(",")
            if len(self._rotb_extreme_plus_summon_list) == 1 and self._rotb_extreme_plus_summon_list[0] == "":
                self._rotb_extreme_plus_summon_list.clear()

            self._rotb_extreme_plus_summon_element_list = config.get("rise_of_the_beasts", "rotb_extreme_plus_summon_element_list").replace(" ", "_").split(",")
            if len(self._rotb_extreme_plus_summon_element_list) == 1 and self._rotb_extreme_plus_summon_element_list[0] == "":
                self._rotb_extreme_plus_summon_element_list.clear()

            self._rotb_extreme_plus_group_number = config.get("rise_of_the_beasts", "rotb_extreme_plus_group_number")
            self._rotb_extreme_plus_party_number = config.get("rise_of_the_beasts", "rotb_extreme_plus_party_number")
            self._rotb_extreme_plus_amount = 0
        # #### end of config.ini ####

        if self._rotb_extreme_plus_combat_script == "":
            self._game.print_and_save("[ROTB] Combat Script for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
            self._rotb_extreme_plus_combat_script = self._game.combat_script

        if len(self._rotb_extreme_plus_summon_element_list) == 0:
            self._game.print_and_save("[ROTB] Summon Elements for Rise of the Beasts Extreme+ will reuse the ones for Farming Mode.")
            self._rotb_extreme_plus_summon_element_list = self._game.summon_element_list

        if len(self._rotb_extreme_plus_summon_list) == 0:
            self._game.print_and_save("[ROTB] Summons for Rise of the Beasts Extreme+ will reuse the ones for Farming Mode.")
            self._rotb_extreme_plus_summon_list = self._game.summon_list

        if self._rotb_extreme_plus_group_number == "":
            self._game.print_and_save("[ROTB] Group Number for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
            self._rotb_extreme_plus_group_number = self._game.group_number
        else:
            self._rotb_extreme_plus_group_number = int(self._rotb_extreme_plus_group_number)

        if self._rotb_extreme_plus_party_number == "":
            self._game.print_and_save("[ROTB] Party Number for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
            self._rotb_extreme_plus_party_number = self._game.party_number
        else:
            self._rotb_extreme_plus_party_number = int(self._rotb_extreme_plus_party_number)

        self._game.print_and_save("[ROTB] Settings initialized for Rise of the Beasts Extreme+...")
        # #### end of Advanced Setup ####
        #################################

    def check_for_rotb_extreme_plus(self):
        """Checks for Extreme+ for Rise of the Beasts and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Extreme+ was detected and successfully completed. Otherwise, return False.
        """
        if self._enable_rotb_extreme_plus and self._game.image_tools.confirm_location("rotb_extreme_plus", tries = 1):
            self._game.print_and_save("\n[ROTB] Detected Extreme+. Starting it now...")

            self._game.print_and_save("\n********************************************************************************")
            self._game.print_and_save("********************************************************************************")
            self._game.print_and_save(f"[ROTB] Rise of the Beasts Extreme+")
            self._game.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Summon Elements: {self._rotb_extreme_plus_summon_element_list}")
            self._game.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Summons: {self._rotb_extreme_plus_summon_list}")
            self._game.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Group Number: {self._rotb_extreme_plus_group_number}")
            self._game.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Party Number: {self._rotb_extreme_plus_party_number}")
            self._game.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Combat Script: {self._rotb_extreme_plus_combat_script}")
            self._game.print_and_save(f"[ROTB] Amount of Rise of the Beasts Extreme+ encountered: {self._rotb_extreme_plus_amount}")
            self._game.print_and_save("********************************************************************************")
            self._game.print_and_save("********************************************************************************\n")

            # Click the "Play Next" button to head to the Summon Selection screen.
            self._game.find_and_click_button("play_next")

            self._game.wait(1)

            # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
            if self._game.image_tools.confirm_location("select_a_summon"):
                self._game.select_summon(self._rotb_extreme_plus_summon_list, self._rotb_extreme_plus_summon_element_list)
                start_check = self._game.find_party_and_start_mission(int(self._rotb_extreme_plus_group_number), int(self._rotb_extreme_plus_party_number))

                # Once preparations are completed, start Combat mode.
                if start_check and self._game.combat_mode.start_combat_mode(self._rotb_extreme_plus_combat_script, is_nightmare = True):
                    self._game.collect_loot()
                    return True

        elif not self._enable_rotb_extreme_plus and self._game.image_tools.confirm_location("rotb_extreme_plus", tries = 2):
            self._game.print_and_save("\n[ROTB] Rise of the Beasts Extreme+ detected but user opted to not run it. Moving on...")
            self._game.find_and_click_button("close")
        else:
            self._game.print_and_save("\n[ROTB] No Rise of the Beasts Extreme+ detected. Moving on...")

        return False

    def _navigate(self):
        """Navigates to the specified Rise of the Beasts mission.

        Returns:
            None
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        self._game.print_and_save(f"\n[ROTB] Now navigating to Rise of the Beasts...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        banner_locations = self._game.image_tools.find_all("event_banner")
        if len(banner_locations) == 0:
            banner_locations = self._game.image_tools.find_all("event_banner_blue")
        self._game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        self._game.wait(1)

        if self._game.image_tools.confirm_location("rotb"):
            # Remove the difficulty prefix from the mission name.
            difficulty = ""
            temp_mission_name = ""
            if self._mission_name.find("VH ") == 0:
                difficulty = "Very Hard"
                temp_mission_name = self._mission_name[3:]
            elif self._mission_name.find("EX ") == 0:
                difficulty = "Extreme"
                temp_mission_name = self._mission_name[3:]

            # Only Raids are marked with Extreme difficulty.
            if difficulty == "Extreme":
                # Click on the Raid banner.
                self._game.print_and_save(f"[ROTB] Now hosting {temp_mission_name} Raid...")
                self._game.find_and_click_button("rotb_extreme")

                if self._game.image_tools.confirm_location("rotb_battle_the_beasts"):
                    if temp_mission_name == "Zhuque":
                        self._game.print_and_save(f"[ROTB] Now starting EX Zhuque Raid...")
                        self._game.find_and_click_button("rotb_raid_zhuque")
                    elif temp_mission_name == "Xuanwu":
                        self._game.print_and_save(f"[ROTB] Now starting EX Xuanwu Raid...")
                        self._game.find_and_click_button("rotb_raid_xuanwu")
                    elif temp_mission_name == "Baihu":
                        self._game.print_and_save(f"[ROTB] Now starting EX Baihu Raid...")
                        self._game.find_and_click_button("rotb_raid_baihu")
                    elif temp_mission_name == "Qinglong":
                        self._game.print_and_save(f"[ROTB] Now starting EX Qinglong Raid...")
                        self._game.find_and_click_button("rotb_raid_qinglong")

            elif self._mission_name == "Lvl 100 Shenxian":
                # Click on Shenxian to host.
                self._game.print_and_save(f"[ROTB] Now hosting Shenxian Raid...")
                self._game.find_and_click_button("rotb_shenxian_host")

                if self._game.image_tools.wait_vanish("rotb_shenxian_host", timeout = 10) is False:
                    self._game.print_and_save(f"[ROTB] There are no more Shenxian hosts left. Alerting user...")
                    raise RiseOfTheBeastsException("There are no more Shenxian hosts left.")

            else:
                self._game.print_and_save(f"[ROTB] Now hosting {temp_mission_name} Quest...")

                # Scroll the screen down to make way for smaller screens.
                self._game.mouse_tools.scroll_screen_from_home_button(-400)

                # Find all instances of the "Select" button on the screen and click on the first instance.
                select_button_locations = self._game.image_tools.find_all("select")
                self._game.mouse_tools.move_and_click_point(select_button_locations[0][0], select_button_locations[0][1], "select")

                if self._game.image_tools.confirm_location("rotb_rising_beasts_showdown"):
                    # Find all the round "Play" buttons.
                    round_play_button_locations = self._game.image_tools.find_all("play_round_button")

                    if temp_mission_name == "Zhuque":
                        self._game.mouse_tools.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "play_round_button")
                    elif temp_mission_name == "Xuanwu":
                        self._game.mouse_tools.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "play_round_button")
                    elif temp_mission_name == "Baihu":
                        self._game.mouse_tools.move_and_click_point(round_play_button_locations[2][0], round_play_button_locations[2][1], "play_round_button")
                    elif temp_mission_name == "Qinglong":
                        self._game.mouse_tools.move_and_click_point(round_play_button_locations[3][0], round_play_button_locations[3][1], "play_round_button")

                    self._game.wait(1)

                    # Find all the round "Play" buttons again.
                    round_play_button_locations = self._game.image_tools.find_all("play_round_button")

                    # Only Very Hard difficulty will be supported for farming efficiency
                    self._game.mouse_tools.move_and_click_point(round_play_button_locations[2][0], round_play_button_locations[2][1], "play_round_button")

        return None

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Rise of the Beasts Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of runs completed.
        """
        number_of_items_dropped: int = 0

        # Start the navigation process.
        if first_run:
            self._navigate()
        elif self._game.find_and_click_button("play_again"):
            self._game.check_for_popups()
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
                    number_of_items_dropped = self._game.collect_loot()
        else:
            raise ROTBException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
