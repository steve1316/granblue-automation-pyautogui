class CoopException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Coop:
    """
    Provides the navigation and any necessary utility functions to handle the Coop game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): Name of the Mission to farm.

    """

    def __init__(self, game, mission_name: str):
        super().__init__()

        self._game = game
        self._mission_name: str = mission_name

        # The 2nd element of the list of EX1 missions is designated "empty" because it is used to navigate properly to "Lost in the Dark" from "Corridor of Puzzles".
        self._coop_ex1_list = ["Corridor of Puzzles", "empty", "Lost in the Dark"]
        self._coop_ex2_list = ["Time of Judgement", "Time of Revelation", "Time of Eminence"]
        self._coop_ex3_list = ["Rule of the Tundra", "Rule of the Plains", "Rule of the Twilight"]
        self._coop_ex4_list = ["Amidst the Waves", "Amidst the Petals", "Amidst Severe Cliffs", "Amidst the Flames"]

    def _navigate(self):
        """Navigates to the specified Coop mission.

        Returns:
            None
        """
        self._game.print_and_save(f"\n[COOP] Beginning process to navigate to the mission: {self._mission_name}...")

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
            if self._mission_name == "In a Dusk Dream":
                # Check if Hard difficulty is already selected. If not, make it active.
                if self._game.image_tools.find_button("coop_hard_selected") is None:
                    self._game.find_and_click_button("coop_hard")

                self._game.print_and_save(f"\n[COOP] Hard difficulty for Coop is now selected.")

                # Select the category, "Save the Oceans", which should be the 3rd category.
                self._game.print_and_save(f"[COOP] Now navigating to \"{self._mission_name}\" for Hard difficulty.")
                self._game.mouse_tools.move_and_click_point(host_quest_button_locations[2][0], host_quest_button_locations[2][1], "coop_host_quest")

                if self._game.image_tools.confirm_location("coop_save_the_oceans"):
                    # Now click "In a Dusk Dream".
                    host_quests_circle_buttons = self._game.image_tools.find_all("coop_host_quest_circle")
                    self._game.mouse_tools.move_and_click_point(host_quests_circle_buttons[0][0], host_quests_circle_buttons[0][1], "coop_host_quest")

            else:
                # Check if Extra difficulty is already selected. If not, make it active.
                if self._game.image_tools.find_button("coop_extra_selected") is None:
                    self._game.find_and_click_button("coop_extra")

                self._game.print_and_save(f"\n[COOP] Extra difficulty for Coop is now selected.")

                # Make the specified EX category active. Then click the mission's button while making sure that the first mission in each category is skipped.
                if self._mission_name in self._coop_ex1_list:
                    self._game.print_and_save(f"\n[COOP] Now navigating to \"{self._mission_name}\" from EX1...")
                    self._game.mouse_tools.move_and_click_point(host_quest_button_locations[0][0], host_quest_button_locations[0][1], "coop_host_quest")

                    if self._game.image_tools.confirm_location("coop_ex1"):
                        self._game.print_and_save(f"\n[COOP] Now selecting Coop mission: \"{self._mission_name}\"")
                        coop_host_locations = self._game.image_tools.find_all("coop_host_quest_circle")
                        self._game.mouse_tools.move_and_click_point(coop_host_locations[self._coop_ex1_list.index(self._mission_name)][0],
                                                                    coop_host_locations[self._coop_ex1_list.index(self._mission_name)][1],
                                                                    "coop_host_quest")

                elif self._mission_name in self._coop_ex2_list:
                    self._game.print_and_save(f"\n[COOP] Now navigating to \"{self._mission_name}\" from EX2...")
                    self._game.mouse_tools.move_and_click_point(host_quest_button_locations[1][0], host_quest_button_locations[1][1], "coop_host_quest")

                    if self._game.image_tools.confirm_location("coop_ex2"):
                        self._game.print_and_save(f"\n[COOP] Now selecting Coop mission: \"{self._mission_name}\"")
                        coop_host_locations = self._game.image_tools.find_all("coop_host_quest_circle")
                        self._game.mouse_tools.move_and_click_point(coop_host_locations[self._coop_ex2_list.index(self._mission_name) + 1][0],
                                                                    coop_host_locations[self._coop_ex2_list.index(self._mission_name) + 1][1],
                                                                    "coop_host_quest")

                elif self._mission_name in self._coop_ex3_list:
                    self._game.print_and_save(f"\n[COOP] Now navigating to \"{self._mission_name}\" from EX3.")
                    self._game.mouse_tools.move_and_click_point(host_quest_button_locations[2][0], host_quest_button_locations[2][1], "coop_host_quest")

                    if self._game.image_tools.confirm_location("coop_ex3"):
                        self._game.print_and_save(f"\n[COOP] Now selecting Coop mission: \"{self._mission_name}\"")
                        coop_host_locations = self._game.image_tools.find_all("coop_host_quest_circle")
                        self._game.mouse_tools.move_and_click_point(coop_host_locations[self._coop_ex3_list.index(self._mission_name) + 1][0],
                                                                    coop_host_locations[self._coop_ex3_list.index(self._mission_name) + 1][1],
                                                                    "coop_host_quest")

                elif self._mission_name in self._coop_ex4_list:
                    self._game.print_and_save(f"\n[COOP] Now navigating to \"{self._mission_name}\" from EX4.")
                    self._game.mouse_tools.move_and_click_point(host_quest_button_locations[3][0], host_quest_button_locations[3][1], "coop_host_quest")

                    if self._game.image_tools.confirm_location("coop_ex4"):
                        self._game.print_and_save(f"\n[COOP] Now selecting Coop mission: \"{self._mission_name}\"")
                        coop_host_locations = self._game.image_tools.find_all("coop_host_quest_circle")
                        self._game.mouse_tools.move_and_click_point(coop_host_locations[self._coop_ex4_list.index(self._mission_name) + 1][0],
                                                                    coop_host_locations[self._coop_ex4_list.index(self._mission_name) + 1][1],
                                                                    "coop_host_quest")

            # After clicking on the Coop mission, create a new Room.
            self._game.print_and_save(f"\n[COOP] Opening up a new Coop room...")
            self._game.find_and_click_button("coop_post_to_crew_chat")

            # Scroll down the screen to see the "OK" button just in case of smaller screens.
            self._game.mouse_tools.scroll_screen_from_home_button(-400)
            self._game.find_and_click_button("ok")

            self._game.wait(1)

            # Just in case, check for the "You retreated from the raid battle" popup.
            if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 1):
                self._game.find_and_click_button("ok")

            self._game.print_and_save(f"\n[COOP] Selecting a Party for Coop mission: \"{self._mission_name}\".")
            self._game.find_and_click_button("coop_select_party")

        return None

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Coop Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of items detected.
        """
        number_of_items_dropped: int = 0

        # Start the navigation process.
        if first_run:
            self._navigate()
        else:
            # Head back to the Coop Room.
            self._game.find_and_click_button("coop_room")

            self._game.wait(1)

            # Check for "Daily Missions" popup for Coop.
            if self._game.image_tools.confirm_location("coop_daily_missions", tries = 1):
                self._game.find_and_click_button("close")

            self._game.wait(1)

            # Now that the bot is back at the Coop Room/Lobby, check if it closed due to time running out.
            if self._game.image_tools.confirm_location("coop_room_closed", tries = 1):
                self._game.print_and_save("\n[COOP] Coop room has closed due to time running out.")
                return -1

            # Start the Coop Mission again.
            self._game.find_and_click_button("coop_start")

            self._game.wait(1)

        # Check for AP.
        self._game.check_for_ap()

        # Check if the bot is at the Party Selection screen. Note that the bot is hosting solo so no support summon selection.
        if first_run and self._game.image_tools.confirm_location("coop_without_support_summon"):
            # Select the Party.
            self._game.find_party_and_start_mission(self._game.group_number, self._game.party_number)

            # Now click the "Start" button to start the Coop Mission.
            self._game.find_and_click_button("coop_start")

            self._game.wait(1)

            # Now start Combat Mode and detect any item drops.
            if self._game.combat_mode.start_combat_mode(self._game.combat_script):
                number_of_items_dropped = self._game.collect_loot()
        elif first_run is False:
            self._game.print_and_save("\n[COOP] Starting Coop Mission again.")

            # Now start Combat Mode and detect any item drops.
            if self._game.combat_mode.start_combat_mode(self._game.combat_script):
                number_of_items_dropped = self._game.collect_loot()
        else:
            raise CoopException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
