class RaidException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Raid:
    """
    Provides the navigation and any necessary utility functions to handle the Raid game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): The name of the Raid mission.

    """

    def __init__(self, game, mission_name: str):
        super().__init__()

        self._game = game
        self._mission_name: str = mission_name
        self._raids_joined = 0

    def _check_for_joined_raids(self):
        """Check and update the number of raids currently joined.

        Returns:
            None
        """
        # Find out the number of currently joined raids.
        self._game.wait(1)
        joined_locations = self._game.image_tools.find_all("joined")

        if joined_locations is not None:
            self._raids_joined = len(joined_locations)
            self._game.print_and_save(f"\n[RAID] There are currently {self._raids_joined} raids joined.")

        return None

    def _clear_joined_raids(self):
        """Begin process to wait out the joined raids if there are 3 or more currently active.

        Returns:
            None
        """
        # If the maximum number of raids has been joined, collect any pending rewards with a interval of 30 seconds in between until the number of joined raids is below 3.
        while self._raids_joined >= 3:
            self._game.print_and_save(f"\n[RAID] Maximum raids of 3 has been joined. Waiting 30 seconds to see if any finish.")
            self._game.wait(30)

            self._game.go_back_home(confirm_location_check = True)
            self._game.find_and_click_button("quest")

            if self._game.check_for_pending():
                self._game.find_and_click_button("quest")
                self._game.wait(1)

            self._game.find_and_click_button("raid")
            self._game.wait(1)
            self._check_for_joined_raids()

        return None

    def _join_raid(self) -> bool:
        """Start the process to fetch a valid room code and join it.

        Returns:
            (bool): True if the bot arrived at the Summon Selection screen.
        """
        recovery_time = 15

        # Make preparations for farming raids by saving the location of the "Join Room" button and the "Room Code" textbox.
        join_room_button = self._game.image_tools.find_button("join_a_room")
        room_code_textbox = (join_room_button[0] - 185, join_room_button[1])

        # Loop and try to join a raid. If none of the room codes worked, wait before trying again with a new set of room codes for a maximum of 10 tries.
        tries = 10
        while tries > 0:
            room_code_tries = 5
            while room_code_tries > 0:
                # Attempt to find a room code.
                room_code = self._game.room_finder.get_room_code()

                if room_code != "":
                    # Select the "Room Code" textbox and then clear all text from it.
                    self._game.mouse_tools.move_and_click_point(room_code_textbox[0], room_code_textbox[1], "template_room_code_textbox", mouse_clicks = 2)
                    self._game.mouse_tools.clear_textbox()

                    # Copy the room code to the clipboard and then paste it into the "Room Code" textbox.
                    self._game.mouse_tools.copy_to_clipboard(room_code)
                    self._game.mouse_tools.paste_from_clipboard()

                    # Now click on the "Join Room" button.
                    self._game.mouse_tools.move_and_click_point(join_room_button[0], join_room_button[1], "join_a_room")

                    # If the room code is valid and the raid is able to be joined, break out and head to the Summon Selection screen.
                    if self._game.find_and_click_button("ok", suppress_error = True) is False:
                        # Check for EP.
                        self._game.check_for_ep()

                        self._game.print_and_save(f"[SUCCESS] Joining {room_code} was successful.")
                        self._raids_joined += 1

                        return self._game.image_tools.confirm_location("select_a_summon")
                    elif self._game.check_for_pending() is False:
                        self._game.print_and_save(f"[WARNING] {room_code} already ended or invalid.")
                    else:
                        # Move from the Home screen back to the Backup Requests screen after clearing out all the Pending Battles.
                        self._game.find_and_click_button("quest")
                        self._game.find_and_click_button("raid")
                        self._game.find_and_click_button("enter_id")

                room_code_tries -= 1
                self._game.wait(1)

            tries -= 1
            self._game.print_and_save(f"\n[WARNING] Could not find any valid room codes. \nWaiting {recovery_time} seconds and then trying again with {tries} tries left before exiting.")
            self._game.wait(recovery_time)

        raise RaidException("Failed to find any valid room codes for 10 total times.")

    def _navigate(self):
        """Navigates to the specified Raid.

        Returns:
            None
        """
        self._game.print_and_save(f"\n[RAID] Beginning process to navigate to the raid: {self._mission_name}...")

        # Head to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Then navigate to the Quest screen.
        self._game.find_and_click_button("quest")

        self._game.wait(1)

        # Check for the "You retreated from the raid battle" popup.
        if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 1):
            self._game.find_and_click_button("ok")

        # Check for any Pending Battles popup.
        if self._game.check_for_pending():
            self._game.find_and_click_button("quest")

        # Now navigate to the Raid screen.
        self._game.find_and_click_button("raid")

        if self._game.image_tools.confirm_location("raid"):
            # Check for any joined raids and if the max number of raids joined was reached, clear them.
            self._check_for_joined_raids()
            self._clear_joined_raids()

            # Click on the "Enter ID" button and then start the process to join a raid.
            self._game.print_and_save(f"\n[RAID] Now moving to the \"Enter ID\" screen.")
            if self._game.find_and_click_button("enter_id"):
                self._join_raid()
        else:
            raise RaidException("Failed to reach the Backup Requests screen.")

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Raid Farming Mode and returns the number of items detected.

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
            # Check for Pending Battles and then perform navigation again.
            self._game.check_for_pending()
            self._navigate()

        # Check for EP.
        self._game.check_for_ep()

        # Check if the bot is at the Summon Selection screen.
        if self._game.image_tools.confirm_location("select_a_summon"):
            summon_check = self._game.select_summon(self._game.summon_list, self._game.summon_element_list)

            if summon_check:
                # Select the Party.
                if self._game.find_party_and_start_mission(self._game.group_number, self._game.party_number):
                    self._game.wait(1)

                    # Handle the rare case where joining the Raid after selecting the Summon and Party led the bot to the Quest Results screen with no loot to collect.
                    if self._game.image_tools.confirm_location("no_loot", tries = 1):
                        self._game.print_and_save("\n[RAID] Seems that the Raid just ended. Moving back to the Home screen and joining another Raid...")
                    else:
                        # Now start Combat Mode and detect any item drops.
                        if self._game.combat_mode.start_combat_mode(self._game.combat_script):
                            number_of_items_dropped = self._game.collect_loot()
                else:
                    self._game.print_and_save("\n[RAID] Seems that the Raid ended before the bot was able to join. Now looking for another Raid to join...")
        else:
            raise RaidException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
