from typing import List


class QuestException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Quest:
    """
    Provides the navigation and any necessary utility functions to handle the Quest game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    map_name (str): Name of the Map to look for the specified Mission.

    mission_name (str): Name of the Mission to farm.

    """

    def __init__(self, game, map_name: str, mission_name: str):
        super().__init__()

        self._game = game
        self._map_name: str = map_name
        self._mission_name: str = mission_name

        self._page_1_list: List[str] = ["Zinkenstill", "Port Breeze Archipelago", "Valtz Duchy", "Auguste Isles", "Lumacie Archipelago", "Albion Citadel"]
        self._page_2_list: List[str] = ["Mist-Shrouded Isle", "Golonzo Island", "Amalthea Island", "Former Capital Mephorash", "Agastia"]

    def _navigate_to_map(self, map_name: str, current_location: str) -> bool:
        """Navigates the bot to the specified Map for Quest Farming Mode.

        Args:
            map_name (str): Name of the Map to navigate to.
            current_location (str): Name of the Map that the bot is currently at.

        Returns:
            (bool): Return True if the bot reached the Summon Selection screen. Otherwise, return False.
        """
        self._game.print_and_save(f"\n[QUEST] Beginning process to navigate to the island: {map_name}...")

        # Phantagrande Skydom Page 1
        if self._page_1_list.__contains__(map_name):
            # Switch pages if needed.
            if self._page_2_list.__contains__(current_location):
                self._game.find_and_click_button("world_left_arrow")

            # Click on the Map to move to it.
            if not self._game.find_and_click_button(map_name.lower().replace(" ", "_").replace("-", "_")):
                # If the name of the island is obscured, like by the "Next" text indicating that the user's next quest is there, fallback to a manual method.
                arrow_location = self._game.image_tools.find_button("world_right_arrow")

                if map_name == "Port Breeze Archipelago":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] - 320, arrow_location[1] - 159, "world_right_arrow")
                elif map_name == "Valtz Duchy":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] - 150, arrow_location[1] - 85, "world_right_arrow")
                elif map_name == "Auguste Isles":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] - 374, arrow_location[1] - 5, "world_right_arrow")
                elif map_name == "Lumacie Archipelago":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] - 84, arrow_location[1] + 39, "world_right_arrow")
                elif map_name == "Albion Citadel":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] - 267, arrow_location[1] + 121, "world_right_arrow")

            return True

        # Phantagrande Skydom Page 2
        elif self._page_2_list.__contains__(map_name):
            if self._page_1_list.__contains__(current_location):
                self._game.find_and_click_button("world_right_arrow")

            if not self._game.find_and_click_button(map_name.lower().replace(" ", "_").replace("-", "_")):
                arrow_location = self._game.image_tools.find_button("world_left_arrow")

                if map_name == "Mist-Shrouded Isle":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] + 162, arrow_location[1] + 114, "world_left_arrow")
                elif map_name == "Golonzo Island":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] + 362, arrow_location[1] + 85, "world_left_arrow")
                elif map_name == "Amalthea Island":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] + 127, arrow_location[1] - 14, "world_left_arrow")
                elif map_name == "Former Capital Mephorash":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] + 352, arrow_location[1] - 51, "world_left_arrow")
                elif map_name == "Agastia":
                    self._game.mouse_tools.move_and_click_point(arrow_location[0] + 190, arrow_location[1] - 148, "world_left_arrow")

            return True

        return False

    def _navigate(self):
        """Navigates to the specified Quest mission.

        Returns:
            None
        """
        self._game.print_and_save(f"\n[QUEST] Beginning process to navigate to the mission: {self._mission_name}...")

        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        current_location = ""
        formatted_map_name = self._map_name.lower().replace(" ", "_").replace("-", "_")

        # Check which island the bot is at.
        if self._game.image_tools.confirm_location(f"map_{formatted_map_name}", tries = 5):
            self._game.print_and_save(f"[QUEST] Bot is currently on the correct island.")
            check_location = True
        else:
            self._game.print_and_save(f"[QUEST] Bot is currently not on the correct island.")
            check_location = False

            location_list = ["Zinkenstill", "Port Breeze Archipelago", "Valtz Duchy", "Auguste Isles", "Lumacie Archipelago", "Albion Citadel", "Mist-Shrouded Isle", "Golonzo Island",
                             "Amalthea Island", "Former Capital Mephorash", "Agastia"]

            while len(location_list) > 0:
                temp_map_location = location_list.pop(0)
                temp_formatted_map_location = temp_map_location.lower().replace(" ", "_").replace("-", "_")

                if self._game.image_tools.confirm_location(f"map_{temp_formatted_map_location}", tries = 5):
                    self._game.print_and_save(f"[QUEST] Bot's current location is at {temp_map_location}. Now moving to {self._map_name}...")
                    current_location = temp_map_location
                    break

        # Once the bot has determined where it is, go to the Quest screen.
        self._game.find_and_click_button("quest")

        self._game.wait(1)

        # Check for the "You retreated from the raid battle" popup.
        if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
            self._game.find_and_click_button("ok")

        if self._game.image_tools.confirm_location("quest"):
            # If the bot is currently not at the correct island, move to it.
            if not check_location:
                # Click the "World" button.
                self._game.find_and_click_button("world")

                # On the World screen, click the specified coordinates on the window to move to the island. If the island is on a different world page, switch pages as necessary.
                self._navigate_to_map(self._map_name, current_location)

                # Click "Go" on the popup after clicking on the map node.
                self._game.find_and_click_button("go")

            # Grab the location of the "World" button.
            world_location = self._game.image_tools.find_button("world", tries = 5)
            if world_location is None:
                world_location = self._game.image_tools.find_button("world2", tries = 5)

            # Now that the bot is on the correct island and is at the Quest screen, click the correct chapter node.
            if self._mission_name == "Scattered Cargo":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 1 (115) node at ({world_location[0] + 97}, {world_location[1] + 97})...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 97, world_location[1] + 97, "template_node")
            elif self._mission_name == "Lucky Charm Hunt":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 6 (122) node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 332, world_location[1] + 16, "template_node")
            elif self._mission_name == "Special Op's Request":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 8 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 258, world_location[1] + 151, "template_node")
            elif self._mission_name == "Threat to the Fisheries":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 9 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 216, world_location[1] + 113, "template_node")
            elif self._mission_name == "The Fruit of Lumacie" or self._mission_name == "Whiff of Danger":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 13 (39/52) node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 78, world_location[1] + 92, "template_node")
            elif self._mission_name == "I Challenge You!":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 17 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 119, world_location[1] + 121, "template_node")
            elif self._mission_name == "For Whom the Bell Tolls":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 22 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 178, world_location[1] + 33, "template_node")
            elif self._mission_name == "Golonzo's Battles of Old":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 25 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 196, world_location[1] + 5, "template_node")
            elif self._mission_name == "The Dungeon Diet":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 30 (44/65) node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 242, world_location[1] + 24, "template_node")
            elif self._mission_name == "Trust Busting Dustup":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 36 (123) node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 319, world_location[1] + 13, "template_node")
            elif self._mission_name == "Erste Kingdom Episode 4":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 70 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 253, world_location[1] + 136, "template_node")
            elif self._mission_name == "Imperial Wanderer's Soul":
                self._game.print_and_save(f"\n[QUEST] Moving to Chapter 55 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 162, world_location[1] + 143, "template_node")

            # After being on the correct chapter node, scroll down the screen as far as possible and then click the mission to start.
            self._game.mouse_tools.scroll_screen(self._game.home_button_location[0], self._game.home_button_location[1] - 50, -1000)
            self._game.find_and_click_button(self._mission_name.replace(" ", "_"))

            # Apply special navigation for mission "Ch. 70 - Erste Kingdom".
            if self._mission_name == "Erste Kingdom Episode 4":
                self._game.find_and_click_button("episode_4")
                self._game.find_and_click_button("ok")

        return None

    def start(self, first_run: bool) -> int:
        """Starts the process to complete a run for Quest Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of items detected.
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

                # Close the "Item Picked Up" popup.
                if self._game.image_tools.confirm_location("items_picked_up"):
                    self._game.find_and_click_button("ok")

                # Now start Combat Mode and detect any item drops.
                if self._game.combat_mode.start_combat_mode(self._game.combat_script):
                    number_of_items_dropped = self._game.collect_loot(is_completed = True)
        else:
            raise QuestException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
