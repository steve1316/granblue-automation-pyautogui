import traceback

from bot.game import Game


class MapSelection:
    """Provides the utility functions needed to perform navigation across the bot.

    Attributes
    ----------
    bot (bot.Game): The Game object.
    
    isBotRunning (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
    
    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.
    """

    def __init__(self, game: Game, is_bot_running: int, debug_mode: bool = False):
        super().__init__()

        self._game = game
        self._is_bot_running = is_bot_running
        self._debug_mode = debug_mode

        # Makes sure that the number of raids currently joined does not exceed 3.
        self._raids_joined = 0

    def _navigate_to_map(self, map_name: str, current_location: str):
        """Navigates the bot to the specified Map for Quest Farming Mode.

        Args:
            map_name (str): Name of the Map to navigate to.
            current_location (str): Name of the Map that the bot is currently at.

        Returns:
            (bool): Return True if the bot reached the Summon Selection screen. Otherwise, return False.
        """
        page_1_list = ["Zinkenstill, Port Breeze Archipelago", "Valtz Duchy", "Auguste Isles", "Lumacie Archipelago", "Albion Citadel"]
        page_2_list = ["Mist-Shrouded Isle", "Golonzo Island", "Amalthea Island", "Former Capital Mephorash", "Agastia"]

        # Phantagrande Skydom Page 1
        if page_1_list.__contains__(map_name):
            # Switch pages if needed.
            if page_2_list.__contains__(current_location):
                self._game.find_and_click_button("world_left_arrow")

            # Click on the Map to move to it.
            if not self._game.find_and_click_button(map_name.lower().replace(" ", "_")):
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
        elif page_2_list.__contains__(map_name):
            if page_1_list.__contains__(current_location):
                self._game.find_and_click_button("world_right_arrow")

            if not self._game.find_and_click_button(map_name.lower().replace(" ", "_")):
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

    def _navigate_to_quest(self, map_name: str, mission_name: str):
        """Navigates the bot to the specified Quest.

        Args:
            map_name (str): Name of the Map to look for the specified Mission.
            mission_name (str): Name of the Mission to farm.

        Returns:
            (bool): Return True if the bot reached the Summon Selection screen. Otherwise, return False.
        """
        # Go to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        current_location = ""

        # Check which island the bot is at.
        if self._game.image_tools.confirm_location(f"map_{map_name}", tries = 2):
            self._game.print_and_save(f"\n[INFO] Bot is currently on the correct island.")
            check_location = True
        else:
            self._game.print_and_save(f"\n[INFO] Bot is currently not on the correct island.")
            check_location = False

            location_list = ["Zinkenstill, Port Breeze Archipelago", "Valtz Duchy", "Auguste Isles", "Lumacie Archipelago", "Albion Citadel", "Mist-Shrouded Isle", "Golonzo Island", "Amalthea Island",
                             "Former Capital Mephorash", "Agastia"]

            while len(location_list) > 0:
                temp_map_location = location_list.pop(0)
                temp_formatted_map_location = temp_map_location.lower().replace(" ", "_")

                if self._game.image_tools.confirm_location(f"map_{temp_formatted_map_location}", tries = 1):
                    self._game.print_and_save(f"\n[INFO] Bot's current location is at {temp_map_location}. Now moving to {map_name}...")
                    current_location = temp_map_location
                    break

        # Once the bot has determined where it is, go to the Quest screen.
        self._game.find_and_click_button("quest", suppress_error = True)

        self._game.wait(1)

        # Check for the "You retreated from the raid battle" popup.
        if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 1):
            self._game.find_and_click_button("ok")

        if self._game.image_tools.confirm_location("quest"):
            # If the bot is currently not at the correct island, move to it.
            if not check_location:
                # Click the "World" button.
                self._game.find_and_click_button("world")

                # On the World screen, click the specified coordinates on the window to move to the island. If the island is on a different world page, switch pages as necessary.
                self._navigate_to_map(map_name, current_location)

                # Click "Go" on the popup after clicking on the map node.
                self._game.find_and_click_button("go")

            # Grab the location of the "World" button.
            world_location = self._game.image_tools.find_button("world", tries = 2)
            if world_location is None:
                world_location = self._game.image_tools.find_button("world2", tries = 2)

            # Now that the bot is on the correct island and is at the Quest screen, click the correct chapter node.
            if mission_name == "Scattered Cargo":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 1 (115) node at ({world_location[0] + 97}, {world_location[1] + 97})...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 97, world_location[1] + 97, "template_node")
            elif mission_name == "Lucky Charm Hunt":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 6 (122) node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 332, world_location[1] + 16, "template_node")
            elif mission_name == "Special Op's Request":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 8 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 258, world_location[1] + 151, "template_node")
            elif mission_name == "Threat to the Fisheries":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 9 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 216, world_location[1] + 113, "template_node")
            elif mission_name == "The Fruit of Lumacie" or mission_name == "Whiff of Danger":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 13 (39/52) node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 78, world_location[1] + 92, "template_node")
            elif mission_name == "I Challenge You!":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 17 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 119, world_location[1] + 121, "template_node")
            elif mission_name == "For Whom the Bell Tolls":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 22 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 178, world_location[1] + 33, "template_node")
            elif mission_name == "Golonzo's Battles of Old":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 25 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 196, world_location[1] + 5, "template_node")
            elif mission_name == "The Dungeon Diet":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 30 (44/65) node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 242, world_location[1] + 24, "template_node")
            elif mission_name == "Trust Busting Dustup":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 36 (123) node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 319, world_location[1] + 13, "template_node")
            elif mission_name == "Erste Kingdom Episode 4":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 70 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 253, world_location[1] + 136, "template_node")
            elif mission_name == "Imperial Wanderer's Soul":
                self._game.print_and_save(f"\n[INFO] Moving to Chapter 55 node...")
                self._game.mouse_tools.move_and_click_point(world_location[0] + 162, world_location[1] + 143, "template_node")

            # After being on the correct chapter node, scroll down the screen as far as possible and then click the mission to start.
            self._game.print_and_save(f"\n[INFO] Now bringing up Summon Selection screen for \"{mission_name}\"...")
            self._game.mouse_tools.scroll_screen(self._game.home_button_location[0], self._game.home_button_location[1] - 50, -1000)
            self._game.find_and_click_button(mission_name.replace(" ", "_"))

            # Apply special navigation for mission "Ch. 70 - Erste Kingdom".
            if mission_name == "Erste Kingdom Episode 4":
                self._game.find_and_click_button("episode_4")
                self._game.find_and_click_button("ok")

        return None

    def _navigate_to_special(self, map_name: str, mission_name: str, difficulty: str):
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

                    mission_select_button = self._game.image_tools.find_button(map_name.lower().replace(" ", "_"))
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
                                difficulty_play_button = (round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                difficulty_play_button = (round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            else:
                                difficulty_play_button = (round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        elif map_name == "Shiny Slime Search!":
                            # Start up the Shiny Slime Search! mission by selecting its difficulty.
                            self._game.print_and_save(f"[INFO] Selecting {difficulty} Shiny Slime Search!...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                difficulty_play_button = (round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                difficulty_play_button = (round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            else:
                                difficulty_play_button = (round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        elif map_name == "Six Dragon Trial":
                            # Start up the Six Dragon Trial mission by selecting its difficulty.
                            self._game.print_and_save(f"[INFO] Selecting {difficulty} Six Dragon Trial...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                difficulty_play_button = (round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                difficulty_play_button = (round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            else:
                                difficulty_play_button = (round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        elif map_name == "Elemental Treasure Quests":
                            # Start up the specified Elemental Treasure Quest mission.
                            self._game.print_and_save(f"[INFO] Selecting {mission_name}...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if formatted_mission_name == "The Hellfire Trial":
                                difficulty_play_button = (round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif formatted_mission_name == "The Deluge Trial":
                                difficulty_play_button = (round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            elif formatted_mission_name == "The Wasteland Trial":
                                difficulty_play_button = (round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")
                            elif formatted_mission_name == "The Typhoon Trial":
                                difficulty_play_button = (round_difficulty_play_button_locations[3][0], round_difficulty_play_button_locations[3][1], "play_round_button")
                            elif formatted_mission_name == "The Aurora Trial":
                                difficulty_play_button = (round_difficulty_play_button_locations[4][0], round_difficulty_play_button_locations[4][1], "play_round_button")
                            elif formatted_mission_name == "The Oblivion Trial":
                                difficulty_play_button = (round_difficulty_play_button_locations[5][0], round_difficulty_play_button_locations[5][1], "play_round_button")

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
                                difficulty_play_button = (round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Very Hard":
                                difficulty_play_button = (round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            elif difficulty == "Extreme":
                                difficulty_play_button = (round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        elif map_name == "Campaign-Exclusive Quest":
                            self._game.print_and_save(f"[INFO] Selecting Campaign-Exclusive Quest...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            # There is only one round "Play" button for this time-limited quest.
                            difficulty_play_button = round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1]

                        else:
                            # Start up the Angel Halo mission by selecting its difficulty.
                            self._game.print_and_save(f"[INFO] Selecting {difficulty} Angel Halo...")
                            round_difficulty_play_button_locations = self._game.image_tools.find_all("play_round_button")

                            if difficulty == "Normal":
                                difficulty_play_button = (round_difficulty_play_button_locations[0][0], round_difficulty_play_button_locations[0][1], "play_round_button")
                            elif difficulty == "Hard":
                                difficulty_play_button = (round_difficulty_play_button_locations[1][0], round_difficulty_play_button_locations[1][1], "play_round_button")
                            else:
                                difficulty_play_button = (round_difficulty_play_button_locations[2][0], round_difficulty_play_button_locations[2][1], "play_round_button")

                        # Finally, click the "Play" button and that should put the bot at the Summon Selection screen.
                        self._game.mouse_tools.move_and_click_point(difficulty_play_button[0], difficulty_play_button[1], "play_round_button")
                        break
                    else:
                        # Scroll the screen down more if on a smaller screen and it obscures the targeted mission.
                        self._game.mouse_tools.scroll_screen(self._game.home_button_location[0], self._game.home_button_location[1] - 50, -500)
                        tries -= 1

        return None

    def _navigate_to_coop(self, mission_name: str):
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
        if difficulty == "Normal":
            formatted_mission_name = mission_name[2:]
        elif difficulty == "Hard":
            formatted_mission_name = mission_name[2:]
        elif difficulty == "Very Hard":
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

                if formatted_mission_name == "Event Quest":
                    # Select the Event Quests. Additionally, offset the locations by 1 if there is a Nightmare available.
                    self._game.print_and_save(f"[INFO] Now hosting Event Quest...")
                    self._game.mouse_tools.move_and_click_point(select_button_locations[0 + nightmare_is_available][0], select_button_locations[0 + nightmare_is_available][1], "select")

                    self._game.wait(1)

                    # Find all the round "Play" buttons.
                    round_play_button_locations = self._game.image_tools.find_all("play_round_button")

                    if difficulty == "Very Hard":
                        self._game.mouse_tools.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "play_round_button")
                    elif difficulty == "Extreme":
                        self._game.mouse_tools.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "play_round_button")

                elif formatted_mission_name == "Event Raid":
                    # Select the Event Raids. Additionally, offset the locations by 1 if there is a Nightmare available.
                    self._game.print_and_save(f"[INFO] Now hosting Event Raid...")
                    self._game.mouse_tools.move_and_click_point(select_button_locations[1 + nightmare_is_available][0], select_button_locations[1 + nightmare_is_available][1], "play_round_button")

                    self._game.wait(1)

                    # Find all the round "Play" buttons.
                    round_play_button_locations = self._game.image_tools.find_all("play_round_button")

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

                if difficulty == "Normal":
                    self._game.mouse_tools.move_and_click_point(quest_play_locations[0][0], quest_play_locations[0][1], "play_round_button")
                elif difficulty == "Hard":
                    self._game.mouse_tools.move_and_click_point(quest_play_locations[1][0], quest_play_locations[1][1], "play_round_button")
                elif difficulty == "Very Hard":
                    self._game.mouse_tools.move_and_click_point(quest_play_locations[2][0], quest_play_locations[2][1], "play_round_button")
                elif difficulty == "Extreme":
                    self._game.mouse_tools.move_and_click_point(quest_play_locations[3][0], quest_play_locations[3][1], "play_round_button")

            elif formatted_mission_name == "Event Raid":
                # Bring up the "Raid Battle" popup. Then scroll down the screen a bit for screens less than 1440p to see the entire popup.
                self._game.print_and_save(f"[INFO] Now hosting Event Raid...")
                if not self._game.find_and_click_button("event_raid_battle"):
                    self._game.image_tools.generate_alert(
                        "Failed to detect Token Drawbox layout for this Event. Are you sure this Event has Token Drawboxes? If not, switch to \"Event\" Farming Mode.")
                    self._is_bot_running.value = 1
                    raise Exception("Failed to detect Token Drawbox layout for this Event. Are you sure this Event has Token Drawboxes? If not, switch to \"Event\" Farming Mode.")
                self._game.mouse_tools.scroll_screen_from_home_button(-400)

                if difficulty == "Very Hard":
                    self._game.find_and_click_button("event_raid_very_hard")
                elif difficulty == "Extreme":
                    self._game.find_and_click_button("event_raid_extreme")
                elif difficulty == "Impossible":
                    self._game.find_and_click_button("event_raid_impossible")

                # If the user does not have enough Treasures to host a Extreme or an Impossible Raid, host a Very Hard Raid instead.
                if (difficulty == "Extreme" and not self._game.image_tools.wait_vanish("event_raid_extreme", timeout = 3)) or (
                        difficulty == "Impossible" and not self._game.image_tools.wait_vanish("event_raid_impossible", timeout = 3)):
                    self._game.print_and_save(f"[INFO] Not enough materials to host ${difficulty}. Hosting Very Hard instead...")
                    self._game.find_and_click_button("event_raid_very_hard")

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
        if farming_mode == "Quest":
            self._navigate_to_quest(map_name, mission_name)
        elif farming_mode == "Special":
            self._navigate_to_special(map_name, mission_name, difficulty)
        elif farming_mode == "Coop":
            self._navigate_to_coop(map_name)
        elif farming_mode == "Event" or farming_mode == "Event (Token Drawboxes)":
            self._navigate_to_event(farming_mode, mission_name, difficulty)

elif map_mode.lower() == "dread barrage":
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

        self._game.print_and_save(
            f"\n[SUCCESS] Hosted Dread Barrage mission is now gone either because of timeout or someone else in the room killed it. Moving on...\n")

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

elif map_mode.lower() == "rise of the beasts":
# Go to the Home screen.
self._game.go_back_home(confirm_location_check = True)

# Go to the Event by clicking on the "Menu" button and then click the very first banner.
self._game.find_and_click_button("home_menu")
banner_locations = self._game.image_tools.find_all("event_banner")
if len(banner_locations) == 0:
    banner_locations = self._game.image_tools.find_all("event_banner_blue")
self._game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

self._game.wait(1)

if self._game.image_tools.confirm_location("rotb"):
    # Remove the difficulty prefix from the mission name.
    temp_mission_name = mission_name
    if difficulty == "Normal":
        temp_mission_name = mission_name[1:]
    elif difficulty == "Hard":
        temp_mission_name = mission_name[1:]
    elif difficulty == "Very Hard":
        temp_mission_name = mission_name[3:]
    elif difficulty == "Extreme":
        temp_mission_name = mission_name[3:]
    elif difficulty == "Impossible":
        temp_mission_name = mission_name[3:]

    # If the first character is a whitespace after processing the string, remove it.
    if temp_mission_name[0] == " ":
        temp_mission_name = temp_mission_name[1:]

    # Only Raids are marked with Extreme difficulty.
    if difficulty == "Extreme":
        # Click on the Raid banner.
        self._game.find_and_click_button("rotb_extreme")

        if self._game.image_tools.confirm_location("rotb_battle_the_beasts"):
            if temp_mission_name.lower() == "zhuque":
                self._game.find_and_click_button("rotb_raid_zhuque")
            elif temp_mission_name.lower() == "xuanwu":
                self._game.find_and_click_button("rotb_raid_xuanwu")
            elif temp_mission_name.lower() == "baihu":
                self._game.find_and_click_button("rotb_raid_baihu")
            elif temp_mission_name.lower() == "qinglong":
                self._game.find_and_click_button("rotb_raid_qinglong")
    else:
        # Scroll the screen down to make way for smaller screens.
        self._game.mouse_tools.scroll_screen_from_home_button(-400)

        # Find all instances of the "Select" button on the screen and click on the first instance.
        select_button_locations = self._game.image_tools.find_all("select")
        self._game.mouse_tools.move_and_click_point(select_button_locations[0][0], select_button_locations[0][1], "select")

        if self._game.image_tools.confirm_location("rotb_rising_beasts_showdown"):
            # Find all the round "Play" buttons.
            round_play_button_locations = self._game.image_tools.find_all("play_round_button")

            if temp_mission_name.lower() == "zhuque":
                self._game.mouse_tools.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "play_round_button")
            elif temp_mission_name.lower() == "xuanwu":
                self._game.mouse_tools.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "play_round_button")
            elif temp_mission_name.lower() == "baihu":
                self._game.mouse_tools.move_and_click_point(round_play_button_locations[2][0], round_play_button_locations[2][1], "play_round_button")
            elif temp_mission_name.lower() == "qinglong":
                self._game.mouse_tools.move_and_click_point(round_play_button_locations[3][0], round_play_button_locations[3][1], "play_round_button")

            self._game.wait(1)

            # Find all the round "Play" buttons again.
            round_play_button_locations = self._game.image_tools.find_all("play_round_button")

            if difficulty == "Normal":
                self._game.mouse_tools.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "play_round_button")
            elif difficulty == "Hard":
                self._game.mouse_tools.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "play_round_button")
            elif difficulty == "Very Hard":
                self._game.mouse_tools.move_and_click_point(round_play_button_locations[2][0], round_play_button_locations[2][1], "play_round_button")

# Check for available AP.
self._game.check_for_ap(use_full_elixir = self._game.use_full_elixir)

# Check to see if the bot is at the Summon Selection screen.
if map_mode.lower() != "coop":
    self._game.print_and_save(f"[INFO] Now checking if bot is currently at Summon Selection screen...")
    check = self._game.image_tools.confirm_location("select_summon", tries = 5)
    if check:
        self._game.print_and_save(f"[INFO] Bot is currently at Summon Selection screen.")
        return True
    else:
        self._game.print_and_save(f"[INFO] Bot is not at Summon Selection screen.")
        return False
else:
    # If its Coop, check to see if the bot is at the Party Selection screen.
    self._game.print_and_save(f"[INFO] Now checking if bot is currently at Coop Party Selection screen...")
    check = self._game.image_tools.confirm_location("coop_without_support_summon", tries = 5)
    if check:
        self._game.print_and_save(f"[INFO] Bot is currently at Coop Party Selection screen.")
        return True
    else:
        self._game.print_and_save(f"[INFO] Bot is not at Coop Party Selection screen.")
        return False
except Exception:
self._game.print_and_save(f"\n[ERROR] Bot encountered exception in MapSelection select_map(): \n{traceback.format_exc()}")
self._is_bot_running.value = 1


def _clear_pending_battle(self):
    """Process a Pending Battle.

    Returns:
        None
    """
    self._game.find_and_click_button("tap_here_to_see_rewards")
    self._game.wait(1)

    if self._game.image_tools.confirm_location("no_loot", tries = 1):
        self._game.print_and_save(f"[INFO] No loot can be collected.")

        # Navigate back to the Quests screen.
        self._game.find_and_click_button("quests", suppress_error = True)
        if self._raids_joined > 0:
            self._raids_joined -= 1
    else:
        # If there is loot available, start loot detection.
        self._game.collect_loot(is_pending_battle = True)

        if self._raids_joined > 0:
            self._raids_joined -= 1

    return None


def check_for_pending(self, map_mode: str):
    """Check and collect any pending rewards and free up slots for the bot to join more raids.

    Args:
        map_mode (str): The mode that will dictate what logic to follow next.

    Returns:
        (bool): Return True if Pending Battles were detected. Otherwise, return False.
    """
    try:
        self._game.wait(1)

        # Check for the "Check your Pending Battles" popup when navigating to the Quest screen or attempting to join a raid when there are 6 Pending Battles
        # or check if the "Play Again" button is covered by the "Pending Battles" button for any other Farming Mode.
        if (map_mode.lower() == "raid" and self._game.image_tools.confirm_location("check_your_pending_battles", tries = 1)) or (
                map_mode.lower() != "raid" and self._game.image_tools.find_button("quest_results_pending_battles", tries = 1, suppress_error = True)):
            self._game.print_and_save(f"\n[INFO] Found Pending Battles that need collecting from.")

            if map_mode.lower() == "raid":
                self._game.find_and_click_button("ok")
                self._game.wait(1)
            else:
                self._game.find_and_click_button("quest_results_pending_battles")
                self._game.wait(1)

            if self._game.image_tools.confirm_location("pending_battles", tries = 1):
                # Tap on a Pending Battle to collect it.
                while self._game.image_tools.find_button("tap_here_to_see_rewards", tries = 1):
                    self._clear_pending_battle()

                    # While on the Loot Collected screen, if there are more Pending Battles then head back to the Pending Battles screen.
                    if self._game.image_tools.find_button("quest_results_pending_battles", tries = 1):
                        self._game.find_and_click_button("quest_results_pending_battles")
                        self._game.wait(1)

                        # Close the Skyscope mission popup.
                        if self._game.enable_skyscope and self._game.image_tools.confirm_location("skyscope"):
                            self._game.find_and_click_button("close")
                            self._game.wait(1)

                        self._game.check_for_friend_request()
                        self._game.wait(1)
                    else:
                        # When there are no more Pending Battles, go back to the Quests screen.
                        self._game.find_and_click_button("quests", suppress_error = True)

                        # Close the Skyscope mission popup.
                        if self._game.enable_skyscope and self._game.image_tools.confirm_location("skyscope"):
                            self._game.find_and_click_button("close")
                            self._game.wait(1)

                        break

            self._game.print_and_save(f"[INFO] Pending battles have been cleared.")
            return True

        self._game.print_and_save(f"[INFO] No Pending Battles needed to be cleared.")
        return False
    except Exception:
        self._game.print_and_save(f"\n[ERROR] Bot encountered exception in MapSelection check_for_pending(): \n{traceback.format_exc()}")
        self._is_bot_running.value = 1


def _check_for_joined(self):
    """Check and update the number of raids currently joined.

    Returns:
        None
    """
    try:
        # Find out the number of currently joined raids.
        self._game.wait(1)
        joined_locations = self._game.image_tools.find_all("joined")
        if joined_locations is not None:
            self._raids_joined = len(joined_locations)
            self._game.print_and_save(f"\n[INFO] There are currently {self._raids_joined} raids joined.")

        return None
    except Exception:
        self._game.print_and_save(f"\n[ERROR] Bot encountered exception in MapSelection _check_for_joined(): \n{traceback.format_exc()}")
        self._is_bot_running.value = 1


def join_raid(self, item_name: str, mission_name: str):
    """Attempt to join the specified raid.

    Args:
        item_name (str): Name of the item to farm.
        mission_name (str): Name of the mission to farm the item in.

    Returns:
        (bool): Return True if the bot reached the Summon Selection screen. Otherwise, return False.
    """
    try:
        # Head to the Home screen.
        self._game.go_back_home(confirm_location_check = True)

        # Then navigate to the Quest screen.
        self._game.find_and_click_button("quest", suppress_error = True)

        # Check for the "You retreated from the raid battle" popup.
        self._game.wait(1)
        if self._game.image_tools.confirm_location("you_retreated_from_the_raid_battle", tries = 1):
            self._game.find_and_click_button("ok")

        self._game.image_tools.confirm_location("quest")

        self.check_for_pending("raid")

        # Now navigate to the Raid screen.
        self._game.find_and_click_button("raid", suppress_error = True)
        self._game.image_tools.confirm_location("raid")

        # Check for any joined raids.
        self._check_for_joined()

        if self._raids_joined >= 3:
            # If the maximum number of raids has been joined, collect any pending rewards with a interval of 60 seconds in between until the number of joined raids is below 3.
            while self._raids_joined >= 3:
                self._game.print_and_save(f"\n[INFO] Maximum raids of 3 has been joined. Waiting 60 seconds to see if any finish.")
                self._game.go_back_home(confirm_location_check = True)

                self._game.wait(60)

                self._game.find_and_click_button("quest", suppress_error = True)
                self.check_for_pending("raid")
        else:
            self.check_for_pending("raid")

        # Click on the "Enter ID" button.
        self._game.print_and_save(f"[INFO] Moving to the Enter ID screen.")
        self._game.find_and_click_button("enter_id")

        # Make preparations for farming raids by saving the location of the "Join Room" button and the "Room Code" textbox.
        join_room_button = self._game.image_tools.find_button("join_a_room")
        room_code_textbox = (join_room_button[0] - 185, join_room_button[1])

        # Loop and try to join a raid from a parsed list of room codes. If none of the room codes worked, wait 60 seconds before trying again with a new set of room codes for a maximum of 10 tries.
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
                if not self.check_for_pending("raid") and not self._game.image_tools.confirm_location("raid_already_ended", tries = 1) and not self._game.image_tools.confirm_location(
                        "already_taking_part", tries = 1) and not self._game.image_tools.confirm_location("invalid_code", tries = 1):
                    # Check for EP.
                    self._game.check_for_ep(use_soul_balm = self._game.use_soul_balm)

                    self._game.print_and_save(f"[SUCCESS] Joining {room_code} was successful.")
                    self._raids_joined += 1
                    return self._game.image_tools.confirm_location("select_summon")
                else:
                    self._game.print_and_save(f"[WARNING] {room_code} already ended or invalid.")
                    self._game.find_and_click_button("ok")

            tries -= 1
            self._game.print_and_save(
                f"\n[WARNING] Could not find any valid room codes. \nWaiting 60 seconds and then trying again with {tries} tries left before exiting.")
            self._game.wait(60)

        return False
    except Exception:
        self._game.print_and_save(f"\n[ERROR] Bot encountered exception in MapSelection join_raid(): \n{traceback.format_exc()}")
        self._is_bot_running.value = 1
