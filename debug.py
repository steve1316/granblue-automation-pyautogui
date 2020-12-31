import sys

import pyautogui


class Debug:
    """
    Test driver for most bot functionality.

    Attributes
    ----------
    game (game.Game): The Game object to test with.
    
    isBotRunning (int): Flag in shared memory that signals the frontend that the bot has finished/exited.

    """

    def __init__(self, game, isBotRunning: int, combat_script: str = ""):
        super().__init__()

        self.game = game
        self.isBotRunning = isBotRunning
        self.combat_script = combat_script
        
    def test_farming_mode(self):
        """Tests the Farming Mode by navigating to the Special Op's Request and farm 10 Fine Sand Bottles with the specified party and summon.
        
        Args:
            None
            
        Return:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing Farming Mode for 10x Fine Sand Bottles from Special Op's Request on Valtz Duchy...")
        self.game.print_and_save("################################################################################")
        
        self.game.start_farming_mode(summon_element_name="water", summon_name="leviathan_omega_ulb", group_number=1, party_number=3, 
                                     map_mode="quest", map_name="Valtz Duchy", item_name="Fine Sand Bottle", item_amount_to_farm=10, 
                                     mission_name="Special Op's Request")
        
        self.isBotRunning.value = 1
        
    def test_item_detection(self, items_to_test: int):
        """Test finding amounts of all items on the screen.

        Args:
            items_to_test (int): The island number that the items belong to. Refer to MapSelection's farmable_materials dictionary 
            for each island's position as a key to their respective item values.
            
        Return:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing finding amounts of all items on screen...")
        self.game.print_and_save("################################################################################")
        
        item_list = {1: ["Satin Feather", "Zephyr Feather", "Flying Sprout"],
                     2: ["Fine Sand Bottle", "Untamed Flame", "Blistering Ore"],
                     3: ["Fresh Water Jug", "Soothing Splash", "Glowing Coral"],
                     4: ["Rough Stone", "Coarse Alluvium", "Swirling Amber"]
                     }
        
        for item in item_list[items_to_test]:
            result = self.game.image_tools.find_farmed_items([item])
            self.game.print_and_save(f"\n{self.game.printtime()} [TEST] {item} farmed: {result}")
            
        self.isBotRunning.value = 1
        
    def test_map_selection(self):
        """Tests navigating to each map that is supported by MapSelection.
        
        Returns:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing navigating to all maps supported by MapSelection...")
        self.game.print_and_save("################################################################################")
        
        self.game.map_selection.select_map(map_mode="quest", map_name="Port Breeze Archipelago", item_name="Satin Feather", mission_name="Scattered Cargo")
        
        self.game.map_selection.select_map(map_mode="quest", map_name="Valtz Duchy", item_name="Fine Sand Bottle", mission_name="Lucky Charm Hunt")
        self.game.map_selection.select_map(map_mode="quest", map_name="Valtz Duchy", item_name="Untamed Flame", mission_name="Special Op's Request")
        
        self.game.map_selection.select_map(map_mode="quest", map_name="Auguste Isles", item_name="Fresh Water Jug", mission_name="Threat to the Fisheries")
        
        self.game.map_selection.select_map(map_mode="quest", map_name="Lumacie Archipelago", item_name="Rough Stone", mission_name="The Fruit of Lumacie")
        self.game.map_selection.select_map(map_mode="quest", map_name="Lumacie Archipelago", item_name="Coarse Alluvium", mission_name="Whiff of Danger")
        
        self.game.print_and_save(f"\n{self.game.printtime()} [TEST_SUCCESS] Testing Map Selection was successful.")
        self.isBotRunning.value = 1
        

    def test_find_summon_element_tabs(self):
        """Tests finding each summon element tab on the Summon Selection Screen by navigating to the Fire Old Lignoid trial battle.

        Returns:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing finding all Summon Element tabs on the Summon Selection screen...")
        self.game.print_and_save("################################################################################")

        # Reset the bot's current position by heading back to the Home Screen.
        self.game.go_back_home(confirm_location_check=True, display_info_check=True)

        # Scroll the Home Screen down and find and click the Gameplay Extras button.
        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Finding and selecting the Gameplay Extras Button...")
        self.game.mouse_tools.scroll_screen_from_home_button(-400)

        self.game.find_and_click_button("gameplay_extras")

        # Now attempt to find the Trial Battles Button in a loop. It will scroll the screen down to show more if there are too many in-game event banners clogging up the screen.
        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Finding and selecting the Trial Battles Button...")
        tries = 3
        while(True):
            trial_battles_location = self.game.image_tools.find_button("trial_battles", tries=1)
            if(trial_battles_location == None):
                self.game.mouse_tools.scroll_screen_from_home_button(-400)
            else:
                self.game.mouse_tools.move_and_click_point(trial_battles_location[0], trial_battles_location[1])
                break

            tries -= 1
            if(tries <= 0):
                sys.exit(f"\n{self.game.printtime()} [TEST_FAILED] Failed to find the Trial Battles button inside the Gameplay Extras dropdown menu. Stopping bot...")

        # Next, start up the Old Lignoid Trial Battle.
        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Starting the Old Lignoid Trial Battle...")
        
        self.game.find_and_click_button("trial_battles_old_lignoid")
        self.game.find_and_click_button("trial_battles_play")

        # Test Successful if the bot is able to find all 7 summon element tabs on the Summon Selection Screen. Otherwise, the test fails.
        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now finding all 7 summon element tabs on the Summon Selection Screen...")
        if(self.game.image_tools.confirm_location("select_summon")):
            if(self.game.find_summon_element("fire") and self.game.find_summon_element("water") and self.game.find_summon_element("earth") and self.game.find_summon_element("wind") and self.game.find_summon_element("light") and self.game.find_summon_element("dark") and self.game.find_summon_element("misc")):
                self.game.print_and_save(f"\n{self.game.printtime()} [TEST_SUCCESS] Finding all summon element tabs was successful.")
                self.isBotRunning.value = 1
            else:
                self.isBotRunning.value = 1
                sys.exit(f"\n{self.game.printtime()} [TEST_FAILED] Failed to find one or more summon element tabs. Stopping bot...")
        else:
            self.isBotRunning.value = 1
            sys.exit(f"\n{self.game.printtime()} [TEST_FAILED] Bot is not at the Summon Selection Screen. Stopping bot...")

    def test_combat_mode2(self):
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing Combat Mode on the Old Lignoid trial battle mission now...")
        self.game.print_and_save("################################################################################")
        
        self.game.go_back_home(confirm_location_check=True, display_info_check=True)
        
        self.game.mouse_tools.scroll_screen_from_home_button(-600)
        
        list_of_steps_in_order = ["gameplay_extras", "trial_battles",
                                  "trial_battles_old_lignoid", "trial_battles_play",
                                  "wind", "party_selection_ok", "trial_battles_close"]
        
        temp_location = None

        # Go through each step in order from left to right.
        while (len(list_of_steps_in_order) > 0):
            image_name = list_of_steps_in_order.pop(0)
            
            if(image_name != "wind"):
                temp_location = self.game.image_tools.find_button(image_name)
                self.game.mouse_tools.move_and_click_point(temp_location[0], temp_location[1])
            else:
                self.game.find_summon_element(image_name)

                # This will use the temp_location coordinates of the last location which was the Play button for the Trial Battle.
                self.game.mouse_tools.move_and_click_point(temp_location[0], temp_location[1] + 140)
        
        self.game.start_combat_mode(self.combat_script)
        
        self.isBotRunning.value = 1
    
    def test_combat_mode(self):
        """Tests almost all of the bot's functionality by starting the Very Hard difficulty Angel Halo Special Battle and completing it. This assumes that Angel Halo is at the very bottom of the Special missions list.

        Returns:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing Combat Mode on Very Hard Difficulty Angel Halo mission now...")
        self.game.print_and_save("################################################################################")

        summon_check = False
        tries = 2
        while(summon_check == False):
            # First go to the Home Screen and calibrate the dimensions of the game window. Then navigation will be as follows: Home Screen -> Quest Screen -> Special Screen.
            self.game.go_back_home(confirm_location_check=True, display_info_check=True)

            list_of_button_names = ["quest", "special"]
            for button_name in list_of_button_names:
                if(button_name == "quest"):
                    self.game.mouse_tools.move_and_click_point(self.game.home_button_location[0] - 37, self.game.home_button_location[1] - 758)
                else:
                    self.game.find_and_click_button(button_name)

            # Attempt to fit all the "Select" buttons into the current view and then find all "Select" Buttons.
            self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Finding all Special Select Buttons...")
            self.game.image_tools.confirm_location("special")
            self.game.mouse_tools.scroll_screen_from_home_button(-400)
            self.game.wait_for_ping(1)

            special_quests = self.game.image_tools.find_all("select", custom_region=(self.game.image_tools.window_left, self.game.image_tools.window_top, 
                                                                                     self.game.image_tools.window_width, self.game.image_tools.window_height))

            # Bring up the Difficulty Screen for Angel Halo and select "Very Hard".
            self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now selecting and moving to Very Hard Difficulty Angel Halo...")
            angel_halo_special_quest = pyautogui.center(special_quests.pop())
            self.game.mouse_tools.move_and_click_point(angel_halo_special_quest[0], angel_halo_special_quest[1])
            self.game.wait_for_ping(1)
            self.game.image_tools.confirm_location("angel_halo")

            # Select the center of the last "Play" Button which would be the Very Hard Difficulty Angel Halo mission.
            list_of_special_play_button_locations = self.game.image_tools.find_all("special_play", custom_region=(self.game.image_tools.window_left, self.game.image_tools.window_top, 
                                                                                                                  self.game.image_tools.window_width, self.game.image_tools.window_height))

            angel_halo_VH = pyautogui.center(list_of_special_play_button_locations.pop())

            # Then click the mission and confirm the location for the Summon Selection Screen.
            self.game.mouse_tools.move_and_click_point(angel_halo_VH[0], angel_halo_VH[1])
            self.game.image_tools.confirm_location("select_summon")

            # Locate Dark summons and click on the specified Summon.
            self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Selecting the first found FLB Hades Summon...")
            self.game.find_summon_element("dark")
            summon_check = self.game.find_summon("hades_flb")

            if (summon_check == False):
                # Repeat trying to find the specified summon until tries run out.
                tries -= 1
                if (tries <= 0):
                    sys.exit(f"\n{self.game.printtime()} [TEST_FAILED] Could not find summon after multiple refreshes. Stopping bot...")

        # Select first Group, second Party and then start the Combat Mode.
        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Selecting First Group, Second Party...")
        self.game.find_party_and_start_mission(1, 2)
        self.game.start_combat_mode(self.combat_script)

        self.game.print_and_save(f"\n{self.game.printtime()} [TEST_SUCCESS] Testing Combat Mode was successful.")
        
        self.isBotRunning.value = 1

        return None
