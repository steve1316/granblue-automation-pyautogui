class DreadBarrageException(Exception):
    def __init__(self, message):
        super().__init__(message)


class DreadBarrage:
    """
    Provides the navigation and any necessary utility functions to handle the Dread Barrage game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): The name of the Dread Barrage mission.

    """

    def __init__(self, game, mission_name: str):
        super().__init__()

        self._game = game
        self._mission_name: str = mission_name

    def _navigate(self):
        """Navigates to the specified Dread Barrage mission.

        Returns:
            None
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Scroll down the screen a little bit and then click the Dread Barrage banner.
        self._game.print_and_save(f"\n[DREAD.BARRAGE] Now navigating to Dread Barrage...")
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

            difficulty = ""
            if self._mission_name.find("1 Star") == 0:
                difficulty = "1 Star"
            elif self._mission_name.find("2 Star") == 0:
                difficulty = "2 Star"
            elif self._mission_name.find("3 Star") == 0:
                difficulty = "3 Star"
            elif self._mission_name.find("4 Star") == 0:
                difficulty = "4 Star"
            elif self._mission_name.find("5 Star") == 0:
                difficulty = "5 Star"

            # Navigate to the specified difficulty.
            if difficulty == "1 Star":
                self._game.print_and_save(f"[DREAD.BARRAGE] Now starting 1 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[0][0], dread_barrage_play_button_locations[0][1], "dread_barrage_play")
            elif difficulty == "2 Star":
                self._game.print_and_save(f"[DREAD.BARRAGE] Now starting 2 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[1][0], dread_barrage_play_button_locations[1][1], "dread_barrage_play")
            elif difficulty == "3 Star":
                self._game.print_and_save(f"[DREAD.BARRAGE] Now starting 3 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[2][0], dread_barrage_play_button_locations[2][1], "dread_barrage_play")
            elif difficulty == "4 Star":
                self._game.print_and_save(f"[DREAD.BARRAGE] Now starting 4 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[3][0], dread_barrage_play_button_locations[3][1], "dread_barrage_play")
            elif difficulty == "5 Star":
                self._game.print_and_save(f"[DREAD.BARRAGE] Now starting 5 Star Dread Barrage Raid...")
                self._game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[4][0], dread_barrage_play_button_locations[4][1], "dread_barrage_play")

            self._game.wait(2)

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Dread Barrage Farming Mode and returns the number of items detected.

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
                    number_of_items_dropped = self._game.collect_loot(is_completed = True)
        else:
            raise DreadBarrageException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
