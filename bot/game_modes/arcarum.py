from configparser import ConfigParser


class ArcarumException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Arcarum:
    """
    Provides the navigation and any necessary utility functions to handle the Arcarum game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    map_name (str): The name of the Arcarum expedition.

    """

    def __init__(self, game, map_name: str):
        super().__init__()

        self._game = game
        self._expedition: str = map_name
        self._first_run = True
        self._encountered_boss = False

        config = ConfigParser()
        config.read("config.ini")

        # #### config.ini ####
        self._enable_stop_on_arcarum_boss = config.getboolean("arcarum", "enable_stop_on_arcarum_boss")
        # #### end of config.ini ####

    def _navigate_to_map(self) -> bool:
        """Navigates to the specified Arcarum expedition.

        Returns:
            (bool): True if the bot was able to start/resume the expedition. False otherwise.
        """
        if self._first_run:
            self._game.print_and_save(f"\n[ARCARUM] Now beginning navigation to {self._expedition}.")
            self._game.go_back_home()

            # Navigate to the Arcarum banner.
            tries = 5
            while tries > 0:
                if self._game.find_and_click_button("arcarum_banner", tries = 1) is False:
                    self._game.mouse_tools.scroll_screen_from_home_button(-300)
                    tries -= 1
                    if tries <= 0:
                        raise ArcarumException("Failed to navigate to Arcarum from the Home screen.")
                else:
                    break

            self._first_run = False
        else:
            self._game.wait(4)

        # Now make sure that the Extreme difficulty is selected.
        self._game.wait(1)

        # Confirm the completion popup if it shows up.
        if self._game.image_tools.confirm_location("arcarum_expedition", tries = 1):
            self._game.find_and_click_button("ok")

        self._game.find_and_click_button("arcarum_extreme")

        # Finally, navigate to the specified map to start it.
        self._game.print_and_save(f"[ARCARUM] Now starting the specified expedition: {self._expedition}.")
        formatted_map_name = self._expedition.lower().replace(" ", "_")

        if self._game.find_and_click_button(f"arcarum_{formatted_map_name}", tries = 5) is False:
            # Resume the expedition if it is already in-progress.
            self._game.find_and_click_button("arcarum_exploring")
        elif self._game.image_tools.confirm_location("arcarum_departure_check"):
            self._game.print_and_save(f"[ARCARUM] Now using 1 Arcarum ticket to start this expedition...")
            result_check = self._game.find_and_click_button("start_expedition")
            self._game.wait(6)
            return result_check
        elif self._game.find_and_click_button("resume"):
            self._game.wait(3)
            return True
        else:
            raise ArcarumException("Failed to encounter the Departure Check to confirm starting the expedition.")

    def _choose_action(self) -> str:
        """Chooses the next action to take for the current Arcarum expedition.

        Returns:
            (str): The action to take next.
        """
        # Determine what action to take.
        self._game.print_and_save(f"\n[ARCARUM] Now determining what action to take...")

        # Wait a second in case the "Do or Die" animation plays.
        self._game.wait(1)

        tries = 3
        while tries > 0:
            # Prioritise any enemies/chests/thorns that are available on the current node.
            if self._game.find_and_click_button("arcarum_action", tries = 1):
                self._game.wait(2)

                self._game.check_for_captcha()

                if self._game.image_tools.confirm_location("arcarum_party_selection", tries = 1):
                    return "Combat"
                elif self._game.find_and_click_button("ok", tries = 1):
                    return "Claimed Treasure/Keythorn"
                else:
                    return "Claimed Spirethorn"

            # Clear any detected Treasure popup after claiming a chest.
            self._game.print_and_save(f"[ARCARUM] No action found for the current node. Looking for Treasure popup...")
            if self._game.image_tools.confirm_location("arcarum_treasure", tries = 1):
                self._game.find_and_click_button("ok")
                return "Claimed Treasure"

            # Next, determine if there is a available node to move to. Any bound monsters should have been destroyed by now.
            self._game.print_and_save(f"[ARCARUM] No Treasure popup detected. Looking for an available node to move to...")
            if self._game.find_and_click_button("arcarum_node", tries = 1):
                self._game.wait(1)
                return "Navigating"

            # Check if a Arcarum boss has appeared. This is after checking for available actions and before searching for a node to move to avoid false positives.
            if self._check_for_boss():
                return "Boss Detected"

            # Next, attempt to navigate to a node that is occupied by mob(s).
            self._game.print_and_save(f"[ARCARUM] No available node to move to. Looking for nodes with mobs on them...")
            if self._game.find_and_click_button("arcarum_mob", tries = 1) or self._game.find_and_click_button("arcarum_red_mob", tries = 1):
                self._game.wait(1)
                return "Navigating"

            # If all else fails, see if there are any unclaimed chests, like the ones spawned by a random special event that spawns chests on all nodes.
            self._game.print_and_save(f"[ARCARUM] No nodes with mobs on them. Looking for nodes with chests on them...")
            if self._game.find_and_click_button("arcarum_silver_chest", tries = 1) or self._game.find_and_click_button("arcarum_gold_chest", tries = 1):
                self._game.wait(1)
                return "Navigating"

            tries -= 1

        self._game.print_and_save(f"[ARCARUM] No action can be taken. Defaulting to moving to the next area.")
        return "Next Area"

    def _check_for_boss(self) -> bool:
        """Checks for the existence of 3-3, 6-3 or 9-3 boss if config.ini enabled it.

        Returns:
            (bool): Flag on whether or not a Boss was detected.
        """
        if self._enable_stop_on_arcarum_boss:
            self._game.print_and_save(f"\n[ARCARUM] Checking if boss is available...")

            if self._game.image_tools.find_button("arcarum_boss", tries = 1) or self._game.image_tools.find_button("arcarum_boss2", tries = 1):
                return True
            else:
                return False
        else:
            return False

    def start(self) -> int:
        """Starts the process of completing Arcarum expeditions.

        Returns:
            (int): Number of runs completed.
        """
        runs_completed = 0
        while runs_completed < self._game.item_amount_to_farm:
            self._navigate_to_map()

            while True:
                action = self._choose_action()
                self._game.print_and_save(f"[ARCARUM] Action to take will be: {action}")

                if action == "Combat":
                    # Start Combat Mode.
                    if self._game.find_party_and_start_mission(self._game.group_number, self._game.party_number):
                        if self._game.image_tools.confirm_location("elemental_damage", tries = 1):
                            raise ArcarumException(
                                "Encountered an important mob for Arcarum and the selected party does not conform to the enemy's weakness. Perhaps you would like to do this battle yourself?")
                        elif self._game.image_tools.confirm_location("arcarum_restriction", tries = 1):
                            raise ArcarumException("Encountered a party restriction for Arcarum. Perhaps you would like to complete this section by yourself?")

                        self._game.wait(3)
                        if self._game.combat_mode.start_combat_mode(self._game.combat_script):
                            self._game.collect_loot(is_completed = False, skip_info = True)
                            self._game.find_and_click_button("expedition")
                elif action == "Navigating":
                    # Move to the next available node.
                    self._game.find_and_click_button("move")
                elif action == "Next Area":
                    # Either navigate to the next area or confirm the expedition's conclusion.
                    if self._game.find_and_click_button("arcarum_next_stage"):
                        self._game.find_and_click_button("ok")
                        self._game.print_and_save(f"[ARCARUM] Moving to the next area...")
                    elif self._game.find_and_click_button("arcarum_checkpoint"):
                        self._game.find_and_click_button("arcarum")
                        self._game.print_and_save(f"[ARCARUM] Expedition is complete.")
                        runs_completed += 1

                        self._game.wait(1)

                        if self._game.image_tools.confirm_location("skyscope", tries = 1):
                            self._game.find_and_click_button("close")

                        break
                elif action == "Boss Detected":
                    self._game.print_and_save(f"[ARCARUM] Boss has been detected. Stopping the bot.")
                    raise ArcarumException("Boss has been detected. Stopping the bot.")

                self._game.wait(1)

        return runs_completed
