class ProvingGroundsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ProvingGrounds:
    """
    Provides the navigation and any necessary utility functions to handle the Proving Grounds game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): The name of the Proving Grounds mission.

    """

    def __init__(self, game, mission_name: str):
        super().__init__()

        self._game = game
        self._mission_name: str = mission_name
        self._first_time = True

    def _navigate(self):
        """Navigates to the specified Proving Grounds mission.

        Returns:
            None
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        self._game.print_and_save(f"\n[PROVING.GROUNDS] Now navigating to Proving Grounds...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        banner_locations = self._game.image_tools.find_all("event_banner")
        if len(banner_locations) == 0:
            banner_locations = self._game.image_tools.find_all("event_banner_blue")
            if len(banner_locations) == 0:
                raise ProvingGroundsException("Failed to find the Event banner.")
        self._game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        self._game.wait(1)

        difficulty = ""
        if self._mission_name == "Extreme":
            difficulty = "Extreme"
        elif self._mission_name == "Extreme+":
            difficulty = "Extreme+"

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
        else:
            raise ProvingGroundsException("Failed to arrive at the main screen for Proving Grounds.")

        return None

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Proving Grounds Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of runs completed.
        """
        number_of_items_dropped: int = 0

        # Start the navigation process.
        if first_run and self._first_time:
            self._navigate()
        elif self._first_time and self._game.find_and_click_button("play_again"):
            self._game.print_and_save("\n[PROVING.GROUNDS] Starting Proving Grounds Mission again...")

        # Check for AP.
        self._game.check_for_ap()

        # Check if the bot is at the Summon Selection screen.
        if (first_run or self._first_time) and self._game.image_tools.confirm_location("proving_grounds_summon_selection"):
            summon_check = self._game.select_summon(self._game.summon_list, self._game.summon_element_list)
            if summon_check:
                self._game.wait(1)

                # No need to select a Party. Just click "OK" to start the mission and confirming the selected summon.
                self._game.find_and_click_button("ok")

                self._game.print_and_save("\n[PROVING.GROUNDS] Now starting Mission for Proving Grounds...")
                self._game.find_and_click_button("proving_grounds_start")

                # Now start Combat Mode and detect any item drops.
                if self._game.combat_mode.start_combat_mode(self._game.combat_script):
                    number_of_items_dropped = self._game.collect_loot()

                    # Click the "Next Battle" button if there are any battles left.
                    if self._game.find_and_click_button("proving_grounds_next_battle"):
                        self._game.print_and_save("\n[PROVING.GROUNDS] Moving onto the next battle for Proving Grounds...")
                        self._game.find_and_click_button("ok")
                        self._first_time = False
        elif first_run is False and self._first_time is False:
            # No need to select a Summon again as it is reused.
            if self._game.combat_mode.start_combat_mode(self._game.combat_script):
                number_of_items_dropped = self._game.collect_loot()

                # Click the "Next Battle" button if there are any battles left.
                if self._game.find_and_click_button("proving_grounds_next_battle"):
                    self._game.print_and_save("\n[PROVING.GROUNDS] Moving onto the next battle for Proving Grounds...")
                    self._game.find_and_click_button("ok")
                else:
                    # Otherwise, all battles for the Mission has been completed. Collect the completion rewards at the end.
                    self._game.print_and_save("\n[PROVING.GROUNDS] Proving Grounds Mission has been completed.")
                    self._game.find_and_click_button("event")

                    self._game.wait(2)
                    self._game.find_and_click_button("proving_grounds_open_chest", tries = 5)

                    if self._game.image_tools.confirm_location("proving_grounds_completion_loot"):
                        self._game.print_and_save("\n[PROVING.GROUNDS] Completion rewards has been acquired.")

                        # Reset the First Time flag so the bot can select a Summon and select the Mission again.
                        if self._game.item_amount_farmed < self._game.item_amount_to_farm:
                            self._first_time = True
                    else:
                        raise ProvingGroundsException("Failed to detect the Completion Loot screen for completing this Proving Grounds mission.")
        else:
            raise ProvingGroundsException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
