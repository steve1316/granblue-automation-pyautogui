class GuildWarsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GuildWars:
    """
    Provides the navigation and any necessary utility functions to handle the Guild Wars game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): The name of the Guild Wars mission.

    """

    def __init__(self, game, mission_name: str):
        super().__init__()

        self._game = game
        self._mission_name: str = mission_name

    def _navigate(self):
        """Navigates to the specified Guild Wars mission.

        Returns:
            None
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        self._game.print_and_save(f"\n[GUILD.WARS] Now navigating to Guild Wars...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        self._game.find_and_click_button("home_menu")
        banner_locations = self._game.image_tools.find_all("event_banner", custom_confidence = 0.7)
        if len(banner_locations) == 0:
            banner_locations = self._game.image_tools.find_all("event_banner_blue", custom_confidence = 0.7)
        self._game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        self._game.wait(1)

        difficulty = ""
        if self._mission_name == "Very Hard":
            difficulty = "Very Hard"
        elif self._mission_name == "Extreme":
            difficulty = "Extreme"
        elif self._mission_name == "Extreme+":
            difficulty = "Extreme+"
        elif self._mission_name == "NM90":
            difficulty = "NM90"
        elif self._mission_name == "NM95":
            difficulty = "NM95"
        elif self._mission_name == "NM100":
            difficulty = "NM100"
        elif self._mission_name == "NM150":
            difficulty = "NM150"

        if self._game.image_tools.confirm_location("guild_wars"):
            # Scroll the screen down a little bit.
            self._game.mouse_tools.scroll_screen_from_home_button(-200)

            self._game.wait(1.0)

            # Perform different navigation actions based on whether the user wants to farm meat or to farm Nightmares.
            if difficulty == "Very Hard" or difficulty == "Extreme" or difficulty == "Extreme+":
                self._game.print_and_save(f"\n[GUILD.WARS] Now proceeding to farm meat.")

                # Click on the banner to farm meat.
                self._game.find_and_click_button("guild_wars_meat")

                self._game.wait(1.0)

                if self._game.image_tools.confirm_location("guild_wars_meat"):
                    # Now click on the specified Mission to start. Also attempt at fixing the deadzone issue by looping.
                    formatted_mission_name = difficulty.replace(" ", "_")
                    tries = 10
                    self._game.print_and_save(f"[GUILD.WARS] Now hosting {difficulty} now...")
                    while self._game.image_tools.wait_vanish("ap_30", timeout = 10) is False:
                        self._game.find_and_click_button(f"guild_wars_meat_{formatted_mission_name}")

                        self._game.wait(3)

                        tries -= 1
                        if tries <= 0:
                            if difficulty == "Extreme+":
                                self._game.image_tools.generate_alert("You did not unlock Extreme+ yet!")
                                raise GuildWarsException("You did not unlock Extreme+ yet!")
                            else:
                                raise GuildWarsException("There appears to be a deadzone issue that the bot failed 10 times to resolve. Please refresh the page and try again.")

                    return None
            else:
                self._game.print_and_save(f"\n[GUILD.WARS] Now proceeding to farm Nightmares.")

                # Click on the banner to farm Nightmares.
                if difficulty != "NM150":
                    self._game.find_and_click_button("guild_wars_nightmare")
                    if not self._game.image_tools.wait_vanish("guild_wars_nightmare", timeout = 10):
                        self._game.find_and_click_button("guild_wars_nightmare")
                else:
                    self._game.print_and_save(f"\n[GUILD.WARS] Now hosting NM150 now...")
                    self._game.find_and_click_button("guild_wars_nightmare_150")
                    if not self._game.image_tools.wait_vanish("guild_wars_nightmare_150", timeout = 10):
                        self._game.find_and_click_button("guild_wars_nightmare_150")

                    if self._game.image_tools.confirm_location("guild_wars_nightmare"):
                        self._game.find_and_click_button("start")

                if difficulty != "NM150" and self._game.image_tools.confirm_location("guild_wars_nightmare"):
                    nightmare_locations = self._game.image_tools.find_all("guild_wars_nightmares")

                    # If today is the first/second day of Guild Wars, only NM90 will be available.
                    if self._game.image_tools.confirm_location("guild_wars_nightmare_first_day", tries = 1):
                        self._game.print_and_save(f"[GUILD.WARS] Today is the first/second day so hosting NM90.")
                        self._game.find_and_click_button("ok")

                        # Alert the user if they lack the meat to host this and stop the bot.
                        if not self._game.image_tools.wait_vanish("ok", timeout = 10):
                            self._game.image_tools.generate_alert("You do not have enough meat to host this NM90!")
                            raise GuildWarsException("You do not have enough meat to host this NM90!")

                    # If it is not the first/second day of Guild Wars, that means that other difficulties are now available.
                    elif difficulty == "NM90":
                        self._game.print_and_save(f"[GUILD.WARS] Now hosting NM90 now...")
                        self._game.mouse_tools.move_and_click_point(nightmare_locations[0][0], nightmare_locations[0][1], "guild_wars_nightmares")
                    elif difficulty == "NM95":
                        self._game.print_and_save(f"[GUILD.WARS] Now hosting NM95 now...")
                        self._game.mouse_tools.move_and_click_point(nightmare_locations[1][0], nightmare_locations[1][1], "guild_wars_nightmares")
                    elif difficulty == "NM100":
                        self._game.print_and_save(f"[GUILD.WARS] Now hosting NM100 now...")
                        self._game.mouse_tools.move_and_click_point(nightmare_locations[2][0], nightmare_locations[2][1], "guild_wars_nightmares")

                else:
                    # If there is not enough meat to host, host Extreme+ instead.
                    self._game.print_and_save(f"\n[GUILD.WARS] User lacks meat to host the Nightmare. Hosting Extreme+ instead...")

                    if difficulty != "NM150":
                        self._game.find_and_click_button("close")
                    else:
                        self._game.find_and_click_button("cancel")

                    # Click on the banner to farm meat.
                    self._game.find_and_click_button("guild_wars_meat")

                    if self._game.image_tools.confirm_location("guild_wars_meat"):
                        self._game.print_and_save(f"[GUILD.WARS] Now hosting Extreme+ now...")
                        self._game.find_and_click_button("guild_wars_meat_extreme+")

                        # Alert the user if they did not unlock Extreme+ and stop the bot.
                        if not self._game.image_tools.wait_vanish("guild_wars_meat_extreme+", timeout = 10):
                            self._game.image_tools.generate_alert("You did not unlock Extreme+ yet!")
                            raise GuildWarsException("You did not unlock Extreme+ yet!")

        return None

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Guild Wars Farming Mode and returns the number of items detected.

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
                    runs_completed = self._game.collect_loot(is_completed = True)
        else:
            raise GuildWarsException("Failed to arrive at the Summon Selection screen.")

        return runs_completed
