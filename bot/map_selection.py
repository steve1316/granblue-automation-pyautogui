class MapSelection:
    """Provides the utility functions needed to perform navigation across the bot.

    Attributes
    ----------
    bot (bot.Game): The Game object.
    
    is_bot_running (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
    
    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.
    """

    def __init__(self, game, is_bot_running: int, debug_mode: bool = False):
        super().__init__()

        self._game = game
        self._is_bot_running = is_bot_running
        self._debug_mode = debug_mode

        # Makes sure that the number of raids currently joined does not exceed 3.
        self._raids_joined = 0

    def _navigate_to_special(self, map_name: str, mission_name: str, difficulty: str):
        """Navigates the bot to the specified Special mission.

        Args:
            map_name (str): Name of the Map to look for the specified Mission.
            mission_name (str): Name of the Mission to farm.
            difficulty (str): Difficulty of the specified Mission.
        """
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
            formatted_mission_name = mission_name
            if difficulty == "Normal":
                formatted_mission_name = mission_name[2:]
            elif difficulty == "Hard":
                formatted_mission_name = mission_name[2:]
            elif difficulty == "Very Hard":
                formatted_mission_name = mission_name[3:]
            elif difficulty == "Extreme":
                formatted_mission_name = mission_name[3:]

            if self._game.image_tools.confirm_location("special"):
                tries = 2

                # Try to select the specified Special mission for a number of tries.
                while tries != 0:
                    # Scroll the screen down if its any of the Special Quests that are more towards the bottom of the page to alleviate problems for smaller screens.
                    if map_name != "Campaign-Exclusive Quest" and map_name != "Basic Treasure Quests" and map_name != "Shiny Slime Search!" and map_name != "Six Dragon Trial":
                        self._game.mouse_tools.scroll_screen_from_home_button(-500)

                    mission_select_button = self._game.image_tools.find_button(map_name.lower().replace(" ", "_").replace("-", "_"))
                    if mission_select_button is not None:
                        self._game.print_and_save(f"\n[INFO] Navigating to {map_name}...")

                        # Move to the specified Special by clicking its "Select" button.
                        special_quest_select_button = (mission_select_button[0] + 145, mission_select_button[1] + 75)
                        self._game.mouse_tools.move_and_click_point(special_quest_select_button[0], special_quest_select_button[1], "select")

                        self._game.wait(1)

                        if map_name == "Basic Treasure Quests":
                            special_play_round_button_locations = self._game.image_tools.find_all("play_round_button")

                            if formatted_mission_name == "Scarlet Trial":
                                # Navigate to Scarlet Trial.
                                self._game.print_and_save(f"[INFO] Selecting Scarlet Trial...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[0][0], special_play_round_button_locations[0][1], "play_round_button")
                            elif formatted_mission_name == "Cerulean Trial":
                                # Navigate to Cerulean Trial.
                                self._game.print_and_save(f"[INFO] Selecting Cerulean Trial...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[1][0], special_play_round_button_locations[1][1], "play_round_button")
                            elif formatted_mission_name == "Violet Trial":
                                # Navigate to Violet Trial.
                                self._game.print_and_save(f"[INFO] Selecting Violet Trial...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[2][0], special_play_round_button_locations[2][1], "play_round_button")

                            self._game.wait(1)

                            # Now start the Trial with the specified difficulty.
                            self._game.print_and_save(f"[INFO] Now navigating to {difficulty}...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            else:
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        elif map_name == "Shiny Slime Search!":
                            # Start up the Shiny Slime Search! mission by selecting its difficulty.
                            self._game.print_and_save(f"[INFO] Selecting {difficulty} Shiny Slime Search!...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            else:
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        elif map_name == "Six Dragon Trial":
                            # Start up the Six Dragon Trial mission by selecting its difficulty.
                            self._game.print_and_save(f"[INFO] Selecting {difficulty} Six Dragon Trial...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            else:
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        elif map_name == "Elemental Treasure Quests":
                            # Start up the specified Elemental Treasure Quest mission.
                            self._game.print_and_save(f"[INFO] Selecting {mission_name}...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if formatted_mission_name == "The Hellfire Trial":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif formatted_mission_name == "The Deluge Trial":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            elif formatted_mission_name == "The Wasteland Trial":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")
                            elif formatted_mission_name == "The Typhoon Trial":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[3][0], round_difficulty_play_button_locations[3][1], "play_round_button")
                            elif formatted_mission_name == "The Aurora Trial":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[4][0], round_difficulty_play_button_locations[4][1], "play_round_button")
                            elif formatted_mission_name == "The Oblivion Trial":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[5][0], round_difficulty_play_button_locations[5][1], "play_round_button")

                        elif map_name == "Showdowns":
                            special_play_round_button_locations = self._game.image_tools.find_all("play_round_button")

                            if formatted_mission_name == "Ifrit Showdown":
                                # Navigate to Ifrit Showdown.
                                self._game.print_and_save(f"[INFO] Selecting Ifrit Showdown...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[0][0], special_play_round_button_locations[0][1], "play_round_button")
                            elif formatted_mission_name == "Cocytus Showdown":
                                # Navigate to Cocytus Showdown.
                                self._game.print_and_save(f"[INFO] Selecting Cocytus Showdown...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[1][0], special_play_round_button_locations[1][1], "play_round_button")
                            elif formatted_mission_name == "Vohu Manah Showdown":
                                # Navigate to Vohu Manah Showdown.
                                self._game.print_and_save(f"[INFO] Selecting Vohu Manah Showdown...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[2][0], special_play_round_button_locations[2][1], "play_round_button")
                            elif formatted_mission_name == "Sagittarius Showdown":
                                # Navigate to Sagittarius Showdown.
                                self._game.print_and_save(f"[INFO] Selecting Sagittarius Showdown...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[3][0], special_play_round_button_locations[3][1], "play_round_button")
                            elif formatted_mission_name == "Corow Showdown":
                                # Navigate to Corow Showdown.
                                self._game.print_and_save(f"[INFO] Selecting Corow Showdown...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[4][0], special_play_round_button_locations[4][1], "play_round_button")
                            elif formatted_mission_name == "Diablo Showdown":
                                # Navigate to Diablo Showdown.
                                self._game.print_and_save(f"[INFO] Selecting Diablo Showdown...")
                                self._game.mouse_tools.move_and_click_point(special_play_round_button_locations[5][0], special_play_round_button_locations[5][1], "play_round_button")

                            # Now start the Showdown with the specified difficulty.
                            self._game.wait(1)
                            self._game.print_and_save(f"[INFO] Now navigating to {difficulty}...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            elif difficulty == "Extreme":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        elif map_name == "Campaign-Exclusive Quest":
                            self._game.print_and_save(f"[INFO] Selecting Campaign-Exclusive Quest...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            # There is only one round "Play" button for this time-limited quest.
                            self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")

                        else:
                            # Start up the Angel Halo mission by selecting its difficulty.
                            self._game.print_and_save(f"[INFO] Selecting {difficulty} Angel Halo...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            else:
                                self._game.mouse_tools.move_and_click_point(round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        break
                    else:
                        # Scroll the screen down more if on a smaller screen and it obscures the targeted mission.
                        self._game.mouse_tools.scroll_screen(self._game.home_button_location[0], self._game.home_button_location[1] - 50, -500)
                        tries -= 1

        return None

    def _navigate_to_coop(self, mission_name: str):
        """Navigates the bot to the specified Coop mission.

        Args:
            mission_name (str): Name of the Mission to farm.
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Click the "Menu" button on the Home screen and then go to the Coop screen.
        self._game.find_and_click_button("home_menu")
        self._game.find_and_click_button("coop")

        if self._game.image_tools.confirm_location("coop"):
            # Scroll down the screen to see more of the Coop missions on smaller screens.
            self._game.mouse_tools.scroll_screen_from_home_button(-400)

            # Find the locations of all of the "Host Quest" buttons.
            host_quest_button_locations = self._game.image_tools.find_all("coop_host_quest")

            # Select the difficulty of the mission that it is under.
            if mission_name == "In a Dusk Dream":
                # Check if Hard difficulty is already selected. If not, make it active.
                if self._game.image_tools.find_button("coop_hard_selected") is None:
                    self._game.find_and_click_button("coop_hard")

                self._game.print_and_save(f"\n[INFO] Hard difficulty for Coop is now selected.")

                # Select the category, "Save the Oceans", which should be the 3rd category.
                self._game.print_and_save(f"[INFO] Now navigating to \"{mission_name}\" for Hard difficulty.")
                self._game.mouse_tools.move_and_click_point(host_quest_button_locations[2][0], host_quest_button_locations[2][1], "coop_host_quest")

                if self._game.image_tools.confirm_location("coop_save_the_oceans"):
                    # Now click "In a Dusk Dream".
                    host_quests_circle_buttons = self._game.image_tools.find_all("coop_host_quest_circle")
                    self._game.mouse_tools.move_and_click_point(host_quests_circle_buttons[0][0], host_quests_circle_buttons[0][1], "coop_host_quest")

            else:
                # Check if Extra difficulty is already selected. If not, make it active.
                if self._game.image_tools.find_button("coop_extra_selected") is None:
                    self._game.find_and_click_button("coop_extra")

                self._game.print_and_save(f"\n[INFO] Extra difficulty for Coop is now selected.")

                # The 2nd element of the list of EX1 missions is designated "empty" because it is used to navigate properly to "Lost in the Dark" from "Corridor of Puzzles".
                coop_ex1_list = ["Corridor of Puzzles", "empty", "Lost in the Dark"]
                coop_ex2_list = ["Time of Judgement", "Time of Revelation", "Time of Eminence"]
                coop_ex3_list = ["Rule of the Tundra", "Rule of the Plains", "Rule of the Twilight"]
                coop_ex4_list = ["Amidst the Waves", "Amidst the Petals", "Amidst Severe Cliffs", "Amidst the Flames"]

                # Make the specified EX category active. Then click the mission's button while making sure that the first mission in each category is skipped.
                if mission_name in coop_ex1_list:
                    self._game.print_and_save(f"\n[INFO] Now navigating to \"{mission_name}\" from EX1...")
                    self._game.mouse_tools.move_and_click_point(host_quest_button_locations[0][0], host_quest_button_locations[0][1], "coop_host_quest")

                    if self._game.image_tools.confirm_location("coop_ex1"):
                        self._game.print_and_save(f"\n[INFO] Now selecting Coop mission: \"{mission_name}\"")
                        coop_host_locations = self._game.image_tools.find_all("coop_host_quest_circle")
                        self._game.mouse_tools.move_and_click_point(coop_host_locations[coop_ex1_list.index(mission_name)][0], coop_host_locations[coop_ex1_list.index(mission_name)][1],
                                                                    "coop_host_quest")

                elif mission_name in coop_ex2_list:
                    self._game.print_and_save(f"\n[INFO] Now navigating to \"{mission_name}\" from EX2...")
                    self._game.mouse_tools.move_and_click_point(host_quest_button_locations[1][0], host_quest_button_locations[1][1], "coop_host_quest")

                    if self._game.image_tools.confirm_location("coop_ex2"):
                        self._game.print_and_save(f"\n[INFO] Now selecting Coop mission: \"{mission_name}\"")
                        coop_host_locations = self._game.image_tools.find_all("coop_host_quest_circle")
                        self._game.mouse_tools.move_and_click_point(coop_host_locations[coop_ex2_list.index(mission_name) + 1][0], coop_host_locations[coop_ex2_list.index(mission_name) + 1][1],
                                                                    "coop_host_quest")

                elif mission_name in coop_ex3_list:
                    self._game.print_and_save(f"\n[INFO] Now navigating to \"{mission_name}\" from EX3.")
                    self._game.mouse_tools.move_and_click_point(host_quest_button_locations[2][0], host_quest_button_locations[2][1], "coop_host_quest")

                    if self._game.image_tools.confirm_location("coop_ex3"):
                        self._game.print_and_save(f"\n[INFO] Now selecting Coop mission: \"{mission_name}\"")
                        coop_host_locations = self._game.image_tools.find_all("coop_host_quest_circle")
                        self._game.mouse_tools.move_and_click_point(coop_host_locations[coop_ex3_list.index(mission_name) + 1][0], coop_host_locations[coop_ex3_list.index(mission_name) + 1][1],
                                                                    "coop_host_quest")

                elif mission_name in coop_ex4_list:
                    self._game.print_and_save(f"\n[INFO] Now navigating to \"{mission_name}\" from EX4.")
                    self._game.mouse_tools.move_and_click_point(host_quest_button_locations[3][0], host_quest_button_locations[3][1], "coop_host_quest")

                    if self._game.image_tools.confirm_location("coop_ex4"):
                        self._game.print_and_save(f"\n[INFO] Now selecting Coop mission: \"{mission_name}\"")
                        coop_host_locations = self._game.image_tools.find_all("coop_host_quest_circle")
                        self._game.mouse_tools.move_and_click_point(coop_host_locations[coop_ex4_list.index(mission_name) + 1][0], coop_host_locations[coop_ex4_list.index(mission_name) + 1][1],
                                                                    "coop_host_quest")

            # After clicking on the Coop mission, create a new Room.
            self._game.print_and_save(f"\n[INFO] Opening up a new Coop room...")
            self._game.find_and_click_button("coop_post_to_crew_chat")

            # Scroll down the screen to see the "OK" button just in case of smaller screens.
            self._game.mouse_tools.scroll_screen_from_home_button(-400)
            self._game.find_and_click_button("ok")

            self._game.wait(1)

            # Just in case, check for the "You retreated from the raid battle" popup.
            if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 1):
                self._game.find_and_click_button("ok")

            self._game.print_and_save(f"\n[INFO] Selecting a Party for Coop mission: \"{mission_name}\".")
            self._game.find_and_click_button("coop_select_party")

        return None

    def _navigate_to_event(self, farming_mode: str, mission_name: str, difficulty: str):
        """Navigates the bot to the specified Event or Event (Token Drawboxes) mission.

        Args:
            farming_mode (str): The specified Farming Mode, Event or Event (Token Drawboxes).
            mission_name (str): Name of the Mission to farm.
            difficulty (str): Difficulty of the specified Mission.
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        event_banner_locations = self._game.image_tools.find_all("event_banner")
        if len(event_banner_locations) == 0:
            event_banner_locations = self._game.image_tools.find_all("event_banner_blue")
        self._game.mouse_tools.move_and_click_point(event_banner_locations[0][0], event_banner_locations[0][1], "event_banner")

        self._game.wait(1)

        # Check and click away the "Daily Missions" popup.
        if self._game.image_tools.confirm_location("event_daily_missions", tries = 1):
            self._game.print_and_save(f"\n[INFO] Detected \"Daily Missions\" popup. Clicking it away...")
            self._game.find_and_click_button("close")

        # Remove the difficulty prefix from the mission name.
        if difficulty == "Very Hard":
            formatted_mission_name = mission_name[3:]
        elif difficulty == "Extreme":
            formatted_mission_name = mission_name[3:]
        elif difficulty == "Impossible":
            formatted_mission_name = mission_name[3:]
        else:
            formatted_mission_name = mission_name

        # Perform different navigation actions depending on if this is a "Event" or "Event (Token Drawboxes)".
        if farming_mode == "Event":
            # Click on the "Special Quest" button to head to the Special screen.
            if not self._game.find_and_click_button("event_special_quest"):
                self._game.image_tools.generate_alert(
                    "Failed to detect layout for this Event. Are you sure this Event has no Token Drawboxes? If not, switch to \"Event (Token Drawboxes)\" Farming Mode.")
                self._is_bot_running.value = 1
                raise Exception("Failed to detect layout for this Event. Are you sure this Event has no Token Drawboxes? If not, switch to \"Event (Token Drawboxes)\" Farming Mode.")

            if self._game.image_tools.confirm_location("special"):
                # Check to see if the user already has a Nightmare available.
                nightmare_is_available = 0
                if self._game.image_tools.find_button("event_nightmare", tries = 1) is not None:
                    nightmare_is_available = 1

                # Find all the "Select" buttons.
                select_button_locations = self._game.image_tools.find_all("select")

                # Select the Event Quest or Event Raid. Additionally, offset the locations by 1 if there is a Nightmare available.
                if formatted_mission_name == "Event Quest":
                    self._game.print_and_save(f"[INFO] Now hosting Event Quest...")
                    self._game.mouse_tools.move_and_click_point(select_button_locations[0 + nightmare_is_available][0], select_button_locations[0 + nightmare_is_available][1], "select")
                elif formatted_mission_name == "Event Raid":
                    self._game.print_and_save(f"[INFO] Now hosting Event Raid...")
                    self._game.mouse_tools.move_and_click_point(select_button_locations[1 + nightmare_is_available][0], select_button_locations[1 + nightmare_is_available][1], "play_round_button")

                self._game.wait(1)

                # Find all the round "Play" buttons.
                round_play_button_locations = self._game.image_tools.find_all("play_round_button")

                # Now select the chosen difficulty.
                if difficulty == "Very Hard":
                    self._game.mouse_tools.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "play_round_button")
                elif difficulty == "Extreme":
                    self._game.mouse_tools.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "play_round_button")
        else:
            # Scroll down the screen a little bit for this UI layout that has Token Drawboxes.
            self._game.mouse_tools.scroll_screen_from_home_button(-200)

            if formatted_mission_name == "Event Quest":
                self._game.print_and_save(f"[INFO] Now hosting Event Quest...")
                self._game.find_and_click_button("event_quests")

                self._game.wait(1)

                # Find all the round "Play" buttons.
                quest_play_locations = self._game.image_tools.find_all("play_round_button")

                # Only Extreme difficulty is supported for farming efficiency.
                self._game.mouse_tools.move_and_click_point(quest_play_locations[3][0], quest_play_locations[3][1], "play_round_button")

            elif formatted_mission_name == "Event Raid":
                # Bring up the "Raid Battle" popup. Then scroll down the screen a bit for screens less than 1440p to see the entire popup.
                self._game.print_and_save(f"[INFO] Now hosting Event Raid...")
                if not self._game.find_and_click_button("event_raid_battle"):
                    self._game.image_tools.generate_alert(
                        "Failed to detect Token Drawbox layout for this Event. Are you sure this Event has Token Drawboxes? If not, switch to \"Event\" Farming Mode.")
                    self._is_bot_running.value = 1
                    raise Exception("Failed to detect Token Drawbox layout for this Event. Are you sure this Event has Token Drawboxes? If not, switch to \"Event\" Farming Mode.")
                self._game.mouse_tools.scroll_screen_from_home_button(-200)

                self._game.wait(1)

                ap_locations = self._game.image_tools.find_all("ap", custom_confidence = 0.8, grayscale_check = True)

                if difficulty == "Very Hard":
                    self._game.mouse_tools.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
                    if not self._game.image_tools.wait_vanish("close", timeout = 3):
                        self._game.wait(0.5)
                        self._game.mouse_tools.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
                elif difficulty == "Extreme":
                    self._game.mouse_tools.move_and_click_point(ap_locations[1][0], ap_locations[1][1], "ap")
                    if not self._game.image_tools.wait_vanish("close", timeout = 3):
                        self._game.wait(0.5)
                        self._game.mouse_tools.move_and_click_point(ap_locations[1][0], ap_locations[1][1], "ap")
                elif difficulty == "Impossible":
                    self._game.mouse_tools.move_and_click_point(ap_locations[2][0], ap_locations[2][1], "ap")
                    if not self._game.image_tools.wait_vanish("close", timeout = 3):
                        self._game.wait(0.5)
                        self._game.mouse_tools.move_and_click_point(ap_locations[2][0], ap_locations[2][1], "ap")

                # If the user does not have enough Treasures to host a Extreme or an Impossible Raid, host a Very Hard Raid instead.
                if not self._game.image_tools.wait_vanish("close", timeout = 3):
                    self._game.print_and_save(f"[INFO] Not enough materials to host {difficulty}. Hosting Very Hard instead...")
                    self._game.mouse_tools.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
                    self._game.wait(0.5)
                    self._game.mouse_tools.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")

        return None

    def _navigate_to_dread_barrage(self, difficulty: str):
        """Navigates the bot to the specified Dread Barrage mission.

        Args:
            difficulty (str): Difficulty of the specified Mission.
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Scroll down the screen a little bit and then click the Dread Barrage banner.
        self._game.print_and_save(f"\n[INFO] Now navigating to Dread Barrage...")
        self._game.mouse_tools.scroll_screen_from_home_button(-400)
        self._game.find_and_click_button("dread_barrage")

        self._game.wait(2)

        if self._game.image_tools.confirm_location("dread_barrage"):
            # Check if there is already a hosted Dread Barrage mission.
            if self._game.image_tools.confirm_location("resume_quests", tries = 1):
                self._game.print_and_save(f"\n[WARNING] Detected that there is already a hosted Dread Barrage mission.")
                expiry_time_in_seconds = 0

                while self._game.image_tools.confirm_location("resume_quests", tries = 1):
                    # If there is already a hosted Dread Barrage mission, the bot will wait for a total of 1 hour and 30 minutes
                    # for either the raid to expire or for anyone in the room to clear it.
                    self._game.print_and_save(f"\n[WARNING] The bot will now either wait for the expiry time of 1 hour and 30 minutes or for someone else in the room to clear it.")
                    self._game.print_and_save(f"[WARNING] The bot will now refresh the page every 30 seconds to check if it is still there before proceeding.")
                    self._game.print_and_save(f"[WARNING] User can either wait it out, revive and fight it to completion, or retreat from the mission manually.")
                    self._game.wait(30)

                    self._game.find_and_click_button("reload")
                    self._game.wait(2)

                    expiry_time_in_seconds += 30
                    if expiry_time_in_seconds >= 5400:
                        break

                self._game.print_and_save(f"\n[SUCCESS] Hosted Dread Barrage mission is now gone either because of timeout or someone else in the room killed it. Moving on...\n")

            # Find all the "Play" buttons at the top of the window.
            dread_barrage_play_button_locations = self._game.image_tools.find_all("dread_barrage_play")

            # Navigate to the specified difficulty.
            if difficulty == "1 Star":
                self._game.print_and_save(f"[INFO] Now starting 1 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[0][0], dread_barrage_play_button_locations[0][1], "dread_barrage_play")
            elif difficulty == "2 Star":
                self._game.print_and_save(f"[INFO] Now starting 2 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[1][0], dread_barrage_play_button_locations[1][1], "dread_barrage_play")
            elif difficulty == "3 Star":
                self._game.print_and_save(f"[INFO] Now starting 3 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[2][0], dread_barrage_play_button_locations[2][1], "dread_barrage_play")
            elif difficulty == "4 Star":
                self._game.print_and_save(f"[INFO] Now starting 4 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[3][0], dread_barrage_play_button_locations[3][1], "dread_barrage_play")
            elif difficulty == "5 Star":
                self._game.print_and_save(f"[INFO] Now starting 5 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[4][0], dread_barrage_play_button_locations[4][1], "dread_barrage_play")

            self._game.wait(2)

        return None

    def _navigate_to_rotb(self, mission_name: str, difficulty: str):
        """Navigates the bot to the specified Rise of the Beasts mission.

        Args:
            mission_name (str): Name of the Mission to farm.
            difficulty (str): Difficulty of the specified Mission.
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        self._game.print_and_save(f"\n[INFO] Now navigating to Rise of the Beasts...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        banner_locations = self._game.image_tools.find_all("event_banner")
        if len(banner_locations) == 0:
            banner_locations = self._game.image_tools.find_all("event_banner_blue")
        self._game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        self._game.wait(1)

        if self._game.image_tools.confirm_location("rotb"):
            # Remove the difficulty prefix from the mission name.
            if difficulty == "Very Hard":
                temp_mission_name = mission_name[3:]
            elif difficulty == "Extreme":
                temp_mission_name = mission_name[3:]
            elif difficulty == "Impossible":
                temp_mission_name = mission_name[3:]
            else:
                temp_mission_name = mission_name

            # Only Raids are marked with Extreme difficulty.
            if difficulty == "Extreme":
                # Click on the Raid banner.
                self._game.print_and_save(f"[INFO] Now hosting {temp_mission_name} Raid...")
                self._game.find_and_click_button("rotb_extreme")

                if self._game.image_tools.confirm_location("rotb_battle_the_beasts"):
                    if temp_mission_name == "Zhuque":
                        self._game.print_and_save(f"[INFO] Now starting EX Zhuque Raid...")
                        self._game.find_and_click_button("rotb_raid_zhuque")
                    elif temp_mission_name == "Xuanwu":
                        self._game.print_and_save(f"[INFO] Now starting EX Xuanwu Raid...")
                        self._game.find_and_click_button("rotb_raid_xuanwu")
                    elif temp_mission_name == "Baihu":
                        self._game.print_and_save(f"[INFO] Now starting EX Baihu Raid...")
                        self._game.find_and_click_button("rotb_raid_baihu")
                    elif temp_mission_name == "Qinglong":
                        self._game.print_and_save(f"[INFO] Now starting EX Qinglong Raid...")
                        self._game.find_and_click_button("rotb_raid_qinglong")

            elif mission_name == "Lvl 100 Shenxian":
                # Click on Shenxian to host.
                self._game.print_and_save(f"[INFO] Now hosting Shenxian Raid...")
                self._game.find_and_click_button("rotb_shenxian_host")

                if self._game.image_tools.wait_vanish("rotb_shenxian_host", timeout = 10) is False:
                    self._game.print_and_save(f"[INFO] There are no more Shenxian hosts left. Alerting user...")
                    raise Exception("There are no more Shenxian hosts left.")

            else:
                self._game.print_and_save(f"[INFO] Now hosting {temp_mission_name} Quest...")

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

    def _navigate_to_guild_wars(self, difficulty: str):
        """Navigates the bot to the specified Guild Wars mission.

        Args:
            difficulty (str): Difficulty of the specified Mission.
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        self._game.print_and_save(f"\n[INFO] Now navigating to Guild Wars...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        banner_locations = self._game.image_tools.find_all("event_banner")
        if len(banner_locations) == 0:
            banner_locations = self._game.image_tools.find_all("event_banner_blue")
        self._game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        self._game.wait(1)

        if self._game.image_tools.confirm_location("guild_wars"):
            # Scroll the screen down a little bit.
            self._game.mouse_tools.scroll_screen_from_home_button(-200)

            # Perform different navigation actions based on whether the user wants to farm meat or to farm Nightmares.
            if difficulty == "Very Hard" or difficulty == "Extreme" or difficulty == "Extreme+":
                self._game.print_and_save(f"\n[INFO] Now proceeding to farm meat.")

                # Click on the banner to farm meat.
                self._game.find_and_click_button("guild_wars_meat", grayscale = True)

                if self._game.image_tools.confirm_location("guild_wars_meat"):
                    # Now click on the specified Mission to start.
                    if difficulty == "Very Hard":
                        self._game.print_and_save(f"[INFO] Now hosting Very Hard now...")
                        self._game.find_and_click_button("guild_wars_meat_very_hard")
                        self._game.wait(0.5)
                        self._game.find_and_click_button("guild_wars_meat_very_hard", tries = 1, suppress_error = True)
                    elif difficulty == "Extreme":
                        self._game.print_and_save(f"[INFO] Now hosting Extreme now...")
                        self._game.find_and_click_button("guild_wars_meat_extreme")
                        self._game.wait(0.5)
                        self._game.find_and_click_button("guild_wars_meat_extreme", tries = 1, suppress_error = True)
                    elif difficulty == "Extreme+":
                        self._game.print_and_save(f"[INFO] Now hosting Extreme+ now...")
                        self._game.find_and_click_button("guild_wars_meat_extreme+")
                        self._game.wait(0.5)
                        self._game.find_and_click_button("guild_wars_meat_extreme+", tries = 1, suppress_error = True)

                        # Alert the user if they did not unlock Extreme+ and stop the bot.
                        if not self._game.image_tools.wait_vanish("guild_wars_meat_extreme+", 5):
                            self._game.image_tools.generate_alert("You did not unlock Extreme+ yet!")
                            self._is_bot_running.value = 1
                            raise Exception("You did not unlock Extreme+ yet!")

            else:
                self._game.print_and_save(f"\n[INFO] Now proceeding to farm Nightmares.")

                # Click on the banner to farm Nightmares.
                if difficulty != "NM150":
                    self._game.find_and_click_button("guild_wars_nightmare")
                    self._game.find_and_click_button("guild_wars_nightmare", tries = 1, suppress_error = True)
                else:
                    self._game.print_and_save(f"\n[INFO] Now hosting NM150 now...")
                    self._game.find_and_click_button("guild_wars_nightmare_150")
                    self._game.find_and_click_button("guild_wars_nightmare_150", tries = 1, suppress_error = True)

                    if self._game.image_tools.confirm_location("guild_wars_nightmare"):
                        self._game.find_and_click_button("start")

                if difficulty != "NM150" and self._game.image_tools.confirm_location("guild_wars_nightmare"):
                    nightmare_locations = self._game.image_tools.find_all("guild_wars_nightmares")

                    # If today is the first/second day of Guild Wars, only NM90 will be available.
                    if self._game.image_tools.confirm_location("guild_wars_nightmare_first_day", tries = 1):
                        self._game.print_and_save(f"[INFO] Today is the first/second day so hosting NM90.")
                        self._game.find_and_click_button("ok")

                        # Alert the user if they lack the meat to host this and stop the bot.
                        if not self._game.image_tools.wait_vanish("ok", 5):
                            self._game.image_tools.generate_alert("You do not have enough meat to host this NM90!")
                            self._is_bot_running.value = 1
                            raise Exception("You do not have enough meat to host this NM90!")

                    # If it is not the first/second day of Guild Wars, that means that other difficulties are now available.
                    elif difficulty == "NM90":
                        self._game.print_and_save(f"[INFO] Now hosting NM90 now...")
                        self._game.mouse_tools.move_and_click_point(nightmare_locations[0][0], nightmare_locations[0][1], "guild_wars_nightmares")
                    elif difficulty == "NM95":
                        self._game.print_and_save(f"[INFO] Now hosting NM95 now...")
                        self._game.mouse_tools.move_and_click_point(nightmare_locations[1][0], nightmare_locations[1][1], "guild_wars_nightmares")
                    elif difficulty == "NM100":
                        self._game.print_and_save(f"[INFO] Now hosting NM100 now...")
                        self._game.mouse_tools.move_and_click_point(nightmare_locations[2][0], nightmare_locations[2][1], "guild_wars_nightmares")

                else:
                    # If there is not enough meat to host, host Extreme+ instead.
                    self._game.print_and_save(f"\n[INFO] User lacks meat to host the Nightmare. Hosting Extreme+ instead...")

                    if difficulty != "NM150":
                        self._game.find_and_click_button("close")
                    else:
                        self._game.find_and_click_button("cancel")

                    # Click on the banner to farm meat.
                    self._game.find_and_click_button("guild_wars_meat")

                    if self._game.image_tools.confirm_location("guild_wars_meat"):
                        self._game.print_and_save(f"[INFO] Now hosting Extreme+ now...")
                        self._game.find_and_click_button("guild_wars_meat_extreme+")

                        # Alert the user if they did not unlock Extreme+ and stop the bot.
                        if not self._game.image_tools.wait_vanish("guild_wars_meat_extreme+", 5):
                            self._game.image_tools.generate_alert("You did not unlock Extreme+ yet!")
                            self._is_bot_running.value = 1
                            raise Exception("You did not unlock Extreme+ yet!")

        return None

    def _navigate_to_proving_grounds(self, difficulty: str):
        """Navigates the bot to the specified Proving Grounds mission.

        Args:
            difficulty (str): Difficulty of the specified Mission.
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        self._game.print_and_save(f"\n[INFO] Now navigating to Proving Grounds...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        banner_locations = self._game.image_tools.find_all("event_banner")
        if len(banner_locations) == 0:
            banner_locations = self._game.image_tools.find_all("event_banner_blue")
        self._game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        self._game.wait(1)

        # Select the difficulty.
        if self._game.image_tools.confirm_location("proving_grounds"):
            if self._game.find_and_click_button("proving_grounds_missions"):
                difficulty_button_locations = self._game.image_tools.find_all("play_round_button")

                if difficulty == "Extreme":
                    self._game.mouse_tools.move_and_click_point(difficulty_button_locations[1][0], difficulty_button_locations[1][1], "play_round_button")
                elif difficulty == "Extreme+":
                    self._game.mouse_tools.move_and_click_point(difficulty_button_locations[2][0], difficulty_button_locations[2][1], "play_round_button")

                # After the difficulty has been selected, click "Play" to land the bot at the Proving Grounds' Summon Selection screen.
                self._game.find_and_click_button("play")

        return None

    def _navigate_to_xeno_clash(self, mission_name: str):
        """Navigates the bot to the specified Xeno Clash mission.

        Args:
            mission_name (str): Name of the Mission to farm.
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        self._game.print_and_save(f"\n[INFO] Now navigating to Xeno Clash...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        event_banner_locations = self._game.image_tools.find_all("event_banner")
        if len(event_banner_locations) == 0:
            event_banner_locations = self._game.image_tools.find_all("event_banner_blue")
        self._game.mouse_tools.move_and_click_point(event_banner_locations[0][0], event_banner_locations[0][1], "event_banner")

        self._game.wait(1)

        if self._game.find_and_click_button("xeno_special"):
            # Check to see if the user already has a Nightmare available.
            nightmare_is_available = 0
            if self._game.image_tools.find_button("event_nightmare", tries = 1) is not None:
                nightmare_is_available = 1

            # Find all the "Select" buttons.
            select_button_locations = self._game.image_tools.find_all("select")

            if mission_name == "Xeno Clash Extreme":
                self._game.print_and_save(f"[INFO] Now hosting Xeno Clash Extreme...")
                self._game.mouse_tools.move_and_click_point(select_button_locations[1 + nightmare_is_available][0], select_button_locations[1 + nightmare_is_available][1], "select")

                difficulty_button_locations = self._game.image_tools.find_all("play_round_button")
                self._game.mouse_tools.move_and_click_point(difficulty_button_locations[0][0], difficulty_button_locations[0][1], "play_round_button")
            elif mission_name == "Xeno Clash Raid":
                self._game.print_and_save(f"[INFO] Now hosting Xeno Clash Raid...")
                self._game.mouse_tools.move_and_click_point(select_button_locations[2 + nightmare_is_available][0], select_button_locations[2 + nightmare_is_available][1], "select")

                self._game.wait(1)

                self._game.find_and_click_button("play")

        return None

    def select_map(self, farming_mode: str, map_name: str, mission_name: str, difficulty: str):
        """Navigates the bot to the specified map and preps the bot for Summon/Party selection.

        Args:
            farming_mode (str): Mode to look for the specified item and map in.
            map_name (str): Name of the map to look for the specified mission in.
            mission_name (str): Name of the mission to farm the item in.
            difficulty (str): Selected difficulty for certain missions that require it.

        Returns:
            (bool): Return True if the bot reached the Summon Selection screen. Otherwise, return False.
        """
        # Perform different navigation actions based on the selected Farming Mode.
        if farming_mode == "Quest":
            self._navigate_to_quest(map_name, mission_name)
        elif farming_mode == "Special":
            self._navigate_to_special(map_name, mission_name, difficulty)
        elif farming_mode == "Coop":
            self._navigate_to_coop(mission_name)
        elif farming_mode == "Event" or farming_mode == "Event (Token Drawboxes)":
            self._navigate_to_event(farming_mode, mission_name, difficulty)
        elif farming_mode == "Dread Barrage":
            self._navigate_to_dread_barrage(difficulty)
        elif farming_mode == "Rise of the Beasts":
            self._navigate_to_rotb(mission_name, difficulty)
        elif farming_mode == "Guild Wars":
            self._navigate_to_guild_wars(difficulty)
        elif farming_mode == "Proving Grounds":
            self._navigate_to_proving_grounds(difficulty)
        elif farming_mode == "Xeno Clash":
            self._navigate_to_xeno_clash(mission_name)

        # Check for available AP. Note that Proving Grounds has the AP check after you select your Summon.
        if farming_mode != "Proving Grounds":
            self._game.check_for_ap()

        # Check to see if the bot is at the Summon Selection screen.
        if farming_mode != "Coop":
            self._game.print_and_save(f"[INFO] Now checking if bot is currently at Summon Selection screen...")

            if farming_mode != "Proving Grounds" and self._game.image_tools.confirm_location("select_a_summon", tries = 5):
                self._game.print_and_save(f"[INFO] Bot is currently at Summon Selection screen.")
                return True
            elif farming_mode == "Proving Grounds" and self._game.image_tools.confirm_location("proving_grounds_summon_selection", tries = 5):
                self._game.print_and_save(f"[INFO] Bot is currently at the Proving Grounds' Summon Selection screen.")
                return True
            else:
                self._game.print_and_save(f"[WARNING] Bot is not at Summon Selection screen.")
                return False
        else:
            # If its Coop, check to see if the bot is at the Party Selection screen.
            self._game.print_and_save(f"[INFO] Now checking if bot is currently at Coop Party Selection screen...")

            if self._game.image_tools.confirm_location("coop_without_support_summon", tries = 5):
                self._game.print_and_save(f"[INFO] Bot is currently at Coop Party Selection screen.")
                return True
            else:
                self._game.print_and_save(f"[INFO] Bot is not at Coop Party Selection screen.")
                return False

    def join_raid(self, mission_name: str):
        """Attempt to join the specified raid.

        Args:
            mission_name (str): Name of the mission to farm the item in.

        Returns:
            (bool): Return True if the bot reached the Summon Selection screen. Otherwise, return False.
        """
        # Head to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Then navigate to the Quest screen.
        self._game.find_and_click_button("quest")

        self._game.wait(1)

        # Check for the "You retreated from the raid battle" popup.
        if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 1):
            self._game.find_and_click_button("ok")

        # Check for any Pending Battles popup.
        if self.check_for_pending("raid"):
            self._game.find_and_click_button("quest")

        # Now navigate to the Raid screen.
        self._game.find_and_click_button("raid")

        if self._game.image_tools.confirm_location("raid"):
            # Check for any joined raids.
            self._check_for_joined()

            if self._raids_joined >= 3:
                # If the maximum number of raids has been joined, collect any pending rewards with a interval of 30 seconds in between until the number of joined raids is below 3.
                while self._raids_joined >= 3:
                    self._game.print_and_save(f"\n[INFO] Maximum raids of 3 has been joined. Waiting 30 seconds to see if any finish.")
                    self._game.wait(30)

                    self._game.go_back_home(confirm_location_check = True)
                    self._game.find_and_click_button("quest")

                    if self.check_for_pending("raid"):
                        self._game.find_and_click_button("quest")
                        self._game.wait(1)

                    self._game.find_and_click_button("raid")
                    self._game.wait(1)
                    self._check_for_joined()

            # Click on the "Enter ID" button.
            self._game.print_and_save(f"\n[INFO] Now moving to the \"Enter ID\" screen.")
            self._game.find_and_click_button("enter_id")

            # Make preparations for farming raids by saving the location of the "Join Room" button and the "Room Code" textbox.
            join_room_button = self._game.image_tools.find_button("join_a_room")
            room_code_textbox = (join_room_button[0] - 185, join_room_button[1])

            # Loop and try to join a raid from a parsed list of room codes. If none of the room codes worked, wait 30 seconds before trying again with a new set of room codes for a maximum of 10 tries.
            tries = 10
            while tries > 0:
                # Find 5 most recent tweets for the specified raid and then parse for room codes.
                tweets = self._game.room_finder.find_most_recent(mission_name, 5)
                room_codes = self._game.room_finder.clean_tweets(tweets)

                for room_code in room_codes:
                    # Select the "Room Code" textbox and then clear all text from it.
                    self._game.mouse_tools.move_and_click_point(room_code_textbox[0], room_code_textbox[1], "template_room_code_textbox", mouse_clicks = 2)
                    self._game.mouse_tools.clear_textbox()

                    # Copy the room code to the clipboard and then paste it into the "Room Code" textbox.
                    self._game.mouse_tools.copy_to_clipboard(room_code)
                    self._game.mouse_tools.paste_from_clipboard()

                    # Now click on the "Join Room" button.
                    self._game.mouse_tools.move_and_click_point(join_room_button[0], join_room_button[1], "join_a_room")

                    # If the room code is valid and the raid is able to be joined, break out and head to the Summon Selection screen.
                    if self._game.find_and_click_button("ok") is False:
                        # Check for EP.
                        self._game.check_for_ep()

                        self._game.print_and_save(f"[SUCCESS] Joining {room_code} was successful.")
                        self._raids_joined += 1

                        return self._game.image_tools.confirm_location("select_a_summon")
                    else:
                        if self.check_for_pending("raid") is False:
                            self._game.print_and_save(f"[WARNING] {room_code} already ended or invalid.")
                            self._game.find_and_click_button("ok")
                        else:
                            # Move from the Home screen back to the Backup Requests screen after clearing out all the Pending Battles.
                            self._game.find_and_click_button("quest")
                            self._game.find_and_click_button("raid")
                            self._game.find_and_click_button("enter_id")

                tries -= 1
                self._game.print_and_save(f"\n[WARNING] Could not find any valid room codes. \nWaiting 30 seconds and then trying again with {tries} tries left before exiting.")
                self._game.wait(30)

        return False
