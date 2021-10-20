from configparser import ConfigParser


class EventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Event:
    """
    Provides the navigation and any necessary utility functions to handle the Event or Event (Token Drawboxes) game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): The name of the Event mission.

    """

    def __init__(self, game, mission_name: str):
        super().__init__()

        self._game = game
        self._mission_name: str = mission_name

        self._move_one_down: bool = True
        self._fallback: bool = True

        ##########################
        # #### Advanced Setup ####
        self._game.print_and_save("\n[EVENT] Initializing settings for Event...")

        # #### config.ini ####
        config = ConfigParser()
        config.read("config.ini")
        self._enable_event_nightmare = config.getboolean("event", "enable_event_nightmare")
        if self._enable_event_nightmare:
            self._event_nightmare_combat_script = config.get("event", "event_nightmare_combat_script")

            self._event_nightmare_summon_list = config.get("event", "event_nightmare_summon_list").replace(" ", "_").split(",")
            if len(self._event_nightmare_summon_list) == 1 and self._event_nightmare_summon_list[0] == "":
                self._event_nightmare_summon_list.clear()

            self._event_nightmare_summon_element_list = config.get("event", "event_nightmare_summon_element_list").replace(" ", "_").split(",")
            if len(self._event_nightmare_summon_element_list) == 1 and self._event_nightmare_summon_element_list[0] == "":
                self._event_nightmare_summon_element_list.clear()

            self._event_nightmare_group_number = config.get("event", "event_nightmare_group_number")
            self._event_nightmare_party_number = config.get("event", "event_nightmare_party_number")

            if self._event_nightmare_combat_script == "":
                self._game.print_and_save("[EVENT] Combat Script for Event will reuse the one for Farming Mode.")
                self._event_nightmare_combat_script = self._game.combat_script

            if len(self._event_nightmare_summon_element_list) == 0:
                self._game.print_and_save("[EVENT] Summon Elements for Event will reuse the ones for Farming Mode.")
                self._event_nightmare_summon_element_list = self._game.summon_element_list

            if len(self._event_nightmare_summon_list) == 0:
                self._game.print_and_save("[EVENT] Summons for Event will reuse the ones for Farming Mode.")
                self._event_nightmare_summon_list = self._game.summon_list

            if self._event_nightmare_group_number == "":
                self._game.print_and_save("[EVENT] Group Number for Event will reuse the one for Farming Mode.")
                self._event_nightmare_group_number = self._game.group_number
            else:
                self._event_nightmare_group_number = int(self._event_nightmare_group_number)

            if self._event_nightmare_party_number == "":
                self._game.print_and_save("[EVENT] Party Number for Event will reuse the one for Farming Mode.")
                self._event_nightmare_party_number = self._game.party_number
            else:
                self._event_nightmare_party_number = int(self._event_nightmare_party_number)
        # #### end of config.ini ####

        self._game.print_and_save("[EVENT] Settings initialized for Event...")
        # #### end of Advanced Setup ####
        #################################

    def check_for_event_nightmare(self):
        """Checks for Event Nightmare and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Event Nightmare was detected and successfully completed. Otherwise, return False.
        """
        if self._enable_event_nightmare and self._game.image_tools.confirm_location("limited_time_quests", tries = 1):
            # First check if the Event Nightmare is skippable.
            event_claim_loot_location = self._game.image_tools.find_button("event_claim_loot", tries = 1, suppress_error = True)
            if event_claim_loot_location is not None:
                self._game.print_and_save("\n[EVENT] Skippable Event Nightmare detected. Claiming it now...")
                self._game.mouse_tools.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                self._game.collect_loot(is_completed = False, is_event_nightmare = True)
                return True
            else:
                self._game.print_and_save("\n[EVENT] Detected Event Nightmare. Starting it now...")

                self._game.print_and_save("\n********************************************************************************")
                self._game.print_and_save("********************************************************************************")
                self._game.print_and_save(f"[EVENT] Event Nightmare")
                self._game.print_and_save(f"[EVENT] Event Nightmare Summon Elements: {self._event_nightmare_summon_element_list}")
                self._game.print_and_save(f"[EVENT] Event Nightmare Summons: {self._event_nightmare_summon_list}")
                self._game.print_and_save(f"[EVENT] Event Nightmare Group Number: {self._event_nightmare_group_number}")
                self._game.print_and_save(f"[EVENT] Event Nightmare Party Number: {self._event_nightmare_party_number}")
                self._game.print_and_save(f"[EVENT] Event Nightmare Combat Script: {self._event_nightmare_combat_script}")
                self._game.print_and_save("********************************************************************************")
                self._game.print_and_save("********************************************************************************\n")

                # Click the "Play Next" button to head to the Summon Selection screen.
                self._game.find_and_click_button("play_next")

                self._game.wait(1)

                # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
                if self._game.image_tools.confirm_location("select_a_summon"):
                    self._game.select_summon(self._event_nightmare_summon_list, self._event_nightmare_summon_element_list)
                    start_check = self._game.find_party_and_start_mission(int(self._event_nightmare_group_number), int(self._event_nightmare_party_number))

                    # Once preparations are completed, start Combat Mode.
                    if start_check and self._game.combat_mode.start_combat_mode(self._event_nightmare_combat_script, is_nightmare = True):
                        self._game.collect_loot(is_completed = False, is_event_nightmare = True)
                        return True

        elif not self._enable_event_nightmare and self._game.image_tools.confirm_location("limited_time_quests", tries = 1):
            # First check if the Event Nightmare is skippable.
            event_claim_loot_location = self._game.image_tools.find_button("event_claim_loot", tries = 1, suppress_error = True)
            if event_claim_loot_location is not None:
                self._game.print_and_save("\n[EVENT] Skippable Event Nightmare detected but user opted to not run it. Claiming it regardless...")
                self._game.mouse_tools.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                self._game.collect_loot(is_completed = False, is_event_nightmare = True)
                return True
            else:
                self._game.print_and_save("\n[EVENT] Event Nightmare detected but user opted to not run it. Moving on...")
                self._game.find_and_click_button("close")
        else:
            self._game.print_and_save("\n[EVENT] No Event Nightmare detected. Moving on...")

        return False

    def _navigate_token_drawboxes(self):
        """Navigates to the specified Event (Token Drawboxes) mission.

        Returns:
            None
        """
        self._game.print_and_save(f"[EVENT.TOKEN.DRAWBOXES] Now beginning process to navigate to the mission: {self._mission_name}...")

        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        banner_locations = self._game.image_tools.find_all("event_banner", custom_confidence = 0.7)
        if len(banner_locations) == 0:
            banner_locations = self._game.image_tools.find_all("event_banner_blue", custom_confidence = 0.7)
            if len(banner_locations) == 0:
                raise EventException("Failed to find the Event banner.")
        self._game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        self._game.wait(1)

        # Check and click away the "Daily Missions" popup.
        if self._game.image_tools.confirm_location("event_daily_missions", tries = 1):
            self._game.print_and_save(f"\n[EVENT.TOKEN.DRAWBOXES] Detected \"Daily Missions\" popup. Clicking it away...")
            self._game.find_and_click_button("close")

        # Remove the difficulty prefix from the mission name.
        difficulty = ""
        formatted_mission_name = ""
        if self._mission_name.find("VH ") == 0:
            difficulty = "Very Hard"
            formatted_mission_name = self._mission_name[3:]
        elif self._mission_name.find("EX ") == 0:
            difficulty = "Extreme"
            formatted_mission_name = self._mission_name[3:]
        elif self._mission_name.find("IM ") == 0:
            difficulty = "Impossible"
            formatted_mission_name = self._mission_name[3:]

        # Scroll down the screen a little bit for this UI layout that has Token Drawboxes.
        self._game.mouse_tools.scroll_screen_from_home_button(-200)

        if formatted_mission_name == "Event Quest":
            self._game.print_and_save(f"[EVENT.TOKEN.DRAWBOXES] Now hosting Event Quest...")
            self._game.find_and_click_button("event_quests")

            self._game.wait(1)

            # Find all the round "Play" buttons.
            quest_play_locations = self._game.image_tools.find_all("play_round_button")

            # Only Extreme difficulty is supported for farming efficiency.
            self._game.mouse_tools.move_and_click_point(quest_play_locations[3][0], quest_play_locations[3][1], "play_round_button")
        elif formatted_mission_name == "Event Raid":
            # Bring up the "Raid Battle" popup. Then scroll down the screen a bit for screens less than 1440p to see the entire popup.
            self._game.print_and_save(f"[EVENT.TOKEN.DRAWBOXES] Now hosting Event Raid...")
            if not self._game.find_and_click_button("event_raid_battle"):
                self._game.image_tools.generate_alert(
                    "Failed to detect Token Drawbox layout for this Event. Are you sure this Event has Token Drawboxes? If not, switch to \"Event\" Farming Mode.")
                raise EventException("Failed to detect Token Drawbox layout for this Event. Are you sure this Event has Token Drawboxes? If not, switch to \"Event\" Farming Mode.")
            self._game.mouse_tools.scroll_screen_from_home_button(-200)

            self._game.wait(1)

            ap_locations = self._game.image_tools.find_all("ap")

            if difficulty == "Very Hard":
                self._game.mouse_tools.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
                if not self._game.image_tools.wait_vanish("close", timeout = 10):
                    self._game.mouse_tools.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
                else:
                    return None
            elif difficulty == "Extreme":
                self._game.mouse_tools.move_and_click_point(ap_locations[1][0], ap_locations[1][1], "ap")
                if not self._game.image_tools.wait_vanish("close", timeout = 10):
                    self._game.mouse_tools.move_and_click_point(ap_locations[1][0], ap_locations[1][1], "ap")
                else:
                    return None
            elif difficulty == "Impossible":
                self._game.mouse_tools.move_and_click_point(ap_locations[2][0], ap_locations[2][1], "ap")
                if not self._game.image_tools.wait_vanish("close", timeout = 10):
                    self._game.mouse_tools.move_and_click_point(ap_locations[2][0], ap_locations[2][1], "ap")
                else:
                    return None

            # If the user does not have enough Treasures to host a Extreme or an Impossible Raid, host a Very Hard Raid instead.
            self._game.print_and_save(f"[EVENT.TOKEN.DRAWBOXES] Not enough materials to host {difficulty}. Hosting Very Hard instead...")
            self._game.mouse_tools.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
            if not self._game.image_tools.wait_vanish("close", timeout = 10):
                self._game.mouse_tools.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")

        return None

    def _navigate(self):
        """Navigates to the specified Event mission.

        Returns:
            None
        """
        # Switch over to the navigation logic for Event (Token Drawboxes) if needed.
        if self._game.farming_mode == "Event (Token Drawboxes)":
            self._navigate_token_drawboxes()
        else:
            self._game.print_and_save(f"[EVENT] Now beginning process to navigate to the mission: {self._mission_name}...")

            # Go to the Home screen.
            self._game.go_back_home(confirm_location_check = True)

            self._game.find_and_click_button("quest")

            self._game.wait(1)

            # Check for the "You retreated from the raid battle" popup.
            if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
                self._game.find_and_click_button("ok")

            # Go to the Special screen.
            self._game.find_and_click_button("special")
            self._game.wait(3.0)

            self._game.find_and_click_button("special_event")

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
            elif self._mission_name.find("EX+ ") == 0:
                difficulty = "Extreme+"
                formatted_mission_name = self._mission_name[4:]

            if self._game.image_tools.confirm_location("special"):
                # Check to see if the user already has a Nightmare available.
                nightmare_is_available = 0
                if self._game.image_tools.find_button("event_nightmare", tries = 1) is not None:
                    nightmare_is_available = 1

                # Find all the "Select" buttons.
                select_button_locations = self._game.image_tools.find_all("select")
                if self._move_one_down:
                    position = 1
                else:
                    position = 0

                # Select the Event Quest or Event Raid. Additionally, offset the locations by 1 if there is a Nightmare available.
                if formatted_mission_name == "Event Quest":
                    self._game.print_and_save(f"[EVENT] Now hosting Event Quest...")
                    self._game.mouse_tools.move_and_click_point(select_button_locations[position + nightmare_is_available][0], select_button_locations[position + nightmare_is_available][1], "select")
                elif formatted_mission_name == "Event Raid":
                    self._game.print_and_save(f"[EVENT] Now hosting Event Raid...")
                    self._game.mouse_tools.move_and_click_point(select_button_locations[(position + 1) + nightmare_is_available][0], select_button_locations[(position + 1) + nightmare_is_available][1], "play_round_button")

                self._game.wait(1)

                # Find all the round "Play" buttons.
                round_play_button_locations = self._game.image_tools.find_all("play_round_button")

                # Now select the chosen difficulty.
                if difficulty == "Very Hard":
                    self._game.mouse_tools.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "play_round_button")
                elif difficulty == "Extreme":
                    self._game.mouse_tools.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "play_round_button")
                elif difficulty == "Extreme+":
                    self._game.mouse_tools.move_and_click_point(round_play_button_locations[2][0], round_play_button_locations[2][1], "play_round_button")
            else:
                raise EventException("Failed to arrive at the Special Quest screen.")

        return None

    def start(self, first_run: bool):
        """Starts the process to complete a run for Event or Event (Token Drawboxes) Farming Mode and returns the number of items detected.

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
            raise EventException("Failed to arrive at the Summon Selection screen.")

        return runs_completed
