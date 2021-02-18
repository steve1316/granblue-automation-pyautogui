import traceback


class MapSelection:
    """Provides the utility functions needed to perform navigation across the game.

    Attributes
    ----------
    game (game.Game): The Game object.
    
    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.
    """
    def  __init__(self, game, debug_mode: bool = False):
        super().__init__()
        
        self.game = game
        
        self.debug_mode = debug_mode
        
        # Makes sure that the number of raids currently joined does not exceed 3.
        self.raids_joined = 0
        
    def select_map(self, map_mode: str, map_name: str, item_name: str, mission_name: str, difficulty: str):
        """Navigates the bot to the specified map and preps the bot for Summon/Party selection.

        Args:
            map_mode (str): Mode to look for the specified item and map in.
            map_name (str): Name of the map to look for the specified mission in.
            item_name (str): Name of the item to farm.
            mission_name (str): Name of the mission to farm the item in.
            difficulty (str): Selected difficulty for Special missions.

        Returns:
            (bool): Return True if the bot reached the Summon Selection Screen. Otherwise, return False.
        """
        try:
            check_location = False
            
            # Prepare the map name string to be used to look for the correct image file.
            current_location = ""
            temp_map_name = map_name.replace(" ", "_")
            temp_map_name = temp_map_name.replace("-", "_")

            if(map_mode.lower() == "quest"):
                # Go to the Home Screen and check if the bot is already at the correct island or not.
                self.game.go_back_home(confirm_location_check=True)
                
                if(self.game.image_tools.confirm_location(f"map_{temp_map_name}", tries=2)):
                    check_location = True
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot is currently on the correct island.")
                else:
                    check_location = False
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot is currently not on the correct island.")
                    
                    # Attempt to see which island the bot is currently at.
                    if(self.game.image_tools.confirm_location("map_port_breeze_archipelago", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Port Breeze Archipelago. Now moving to {map_name}...")
                        current_location = "Port Breeze Archipelago"
                    elif(self.game.image_tools.confirm_location("map_valtz_duchy", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Valtz Duchy. Now moving to {map_name}...")
                        current_location = "Valtz Duchy"
                    elif(self.game.image_tools.confirm_location("map_auguste_isles", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Auguste Isles. Now moving to {map_name}...")
                        current_location = "Auguste Isles"
                    elif(self.game.image_tools.confirm_location("map_lumacie_archipelago", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Lumacie Archipelago. Now moving to {map_name}...")
                        current_location = "Lumacie Archipelago"
                    elif(self.game.image_tools.confirm_location("map_albion_citadel", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Albion Citadel. Now moving to {map_name}...")
                        current_location = "Albion Citadel"
                    elif(self.game.image_tools.confirm_location("map_mist_shrouded_isle", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Mist-Shrouded Isle. Now moving to {map_name}...")
                        current_location = "Mist-Shrouded Isle"
                    elif(self.game.image_tools.confirm_location("map_golonzo_island", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Golonzo Island. Now moving to {map_name}...")
                        current_location = "Golonzo Island"
                    elif(self.game.image_tools.confirm_location("map_amalthea_island", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Amalthea Island. Now moving to {map_name}...")
                        current_location = "Amalthea Island"
                    elif(self.game.image_tools.confirm_location("map_former_capital_mephorash", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Former Capital Mephorash. Now moving to {map_name}...")
                        current_location = "Former Capital Mephorash"
                    elif(self.game.image_tools.confirm_location("map_agastia", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at Agastia. Now moving to {map_name}...")
                        current_location = "Agastia"    
                
                # Go to the Quest Screen and confirm if the bot arrived.
                self.game.find_and_click_button("quest", suppress_error=True)
                self.game.image_tools.confirm_location("quest")
                
                # If the bot is currently not at the correct island, move to it.
                if(check_location == False):
                    # Click the World button.
                    world_location = self.game.image_tools.find_button("world", tries=2)
                    if(world_location == None):
                        world_location = self.game.image_tools.find_button("world2", tries=2)
                    self.game.mouse_tools.move_and_click_point(world_location[0], world_location[1])
                    
                    # On the World Screen, click the specified coordinates on the window to move to the island. 
                    # If the island is on a different world page, switch pages as necessary.
                    if(map_name == "Port Breeze Archipelago"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash" or current_location == "Agastia"):
                            self.game.find_and_click_button("world_left_arrow")
                        
                        if(self.game.image_tools.find_button("port_breeze_archipelago", tries=2) != None):
                            self.game.find_and_click_button("port_breeze_archipelago")
                        else:
                            # If the name of the island is obscured, like by the "Next" text indicating that the user's next quest is there, fallback to a manual method.
                            arrow_location = self.game.image_tools.find_button("world_right_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] - 320, arrow_location[1] - 159)
                    elif(map_name == "Valtz Duchy"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash" or current_location == "Agastia"):
                            self.game.find_and_click_button("world_left_arrow")
                        
                        if(self.game.image_tools.find_button("valtz_duchy", tries=2) != None):
                            self.game.find_and_click_button("valtz_duchy")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_right_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] - 150, arrow_location[1] - 85)
                    elif(map_name == "Auguste Isles"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash" or current_location == "Agastia"):
                            self.game.find_and_click_button("world_left_arrow")
                        
                        if(self.game.image_tools.find_button("auguste_isles", tries=2) != None):
                            self.game.find_and_click_button("auguste_isles")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_right_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] - 374, arrow_location[1] - 5)
                    elif(map_name == "Lumacie Archipelago"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash" or current_location == "Agastia"):
                            self.game.find_and_click_button("world_left_arrow")
                        
                        if(self.game.image_tools.find_button("lumacie_archipelago", tries=2) != None):
                            self.game.find_and_click_button("lumacie_archipelago")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_right_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] - 84, arrow_location[1] + 39)
                    elif(map_name == "Albion Citadel"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash" or current_location == "Agastia"):
                            self.game.find_and_click_button("world_left_arrow")
                        
                        if(self.game.image_tools.find_button("albion_citadel", tries=2) != None):
                            self.game.find_and_click_button("albion_citadel")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_right_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] - 267, arrow_location[1] + 121)
                    elif(map_name == "Mist-Shrouded Isle"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        
                        if(self.game.image_tools.find_button("mist_shrouded_isle", tries=2) != None):
                            self.game.find_and_click_button("mist_shrouded_isle")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_left_arrow") # 88, 476
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] + 162, arrow_location[1] + 114)
                    elif(map_name == "Golonzo Island"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        
                        if(self.game.image_tools.find_button("golonzo_island", tries=2) != None):
                            self.game.find_and_click_button("golonzo_island")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_left_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] + 362, arrow_location[1] + 85)
                    elif(map_name == "Amalthea Island"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        
                        if(self.game.image_tools.find_button("amalthea_island", tries=2) != None):
                            self.game.find_and_click_button("amalthea_island")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_left_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] + 127, arrow_location[1] - 14)
                    elif(map_name == "Former Capital Mephorash"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        
                        if(self.game.image_tools.find_button("former_capital_mephorash", tries=2) != None):
                            self.game.find_and_click_button("former_capital_mephorash")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_left_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] + 352, arrow_location[1] - 51)
                    elif(map_name == "Agastia"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        
                        if(self.game.image_tools.find_button("agastia", tries=2) != None):
                            self.game.find_and_click_button("agastia")
                        else:
                            arrow_location = self.game.image_tools.find_button("world_left_arrow")
                            self.game.mouse_tools.move_and_click_point(arrow_location[0] + 190, arrow_location[1] - 148)
                        
                    self.game.find_and_click_button("go")
                    self.game.image_tools.confirm_location("quest")

                # Now that the bot is on the correct island and is on the Quest Screen, click the correct chapter node.
                world_location = self.game.image_tools.find_button("world", tries=2)
                if(world_location == None):
                    world_location = self.game.image_tools.find_button("world2", tries=2)
                
                if(mission_name == "Scattered Cargo"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 1 (115) node at ({world_location[0] + 97}, {world_location[1] + 97})...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 97, world_location[1] + 97)
                elif(mission_name == "Lucky Charm Hunt"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 6 (122) node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 332, world_location[1] + 16)
                elif(mission_name == "Special Op's Request"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 8 node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 258, world_location[1] + 151)
                elif(mission_name == "Threat to the Fisheries"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 9 node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 216, world_location[1] + 113)
                elif(mission_name == "The Fruit of Lumacie" or mission_name == "Whiff of Danger"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 13 (39/52) node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 78, world_location[1] + 92)
                elif(mission_name == "I Challenge You!"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 17 node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 119, world_location[1] + 121)
                elif(mission_name == "For Whom the Bell Tolls"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 22 node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 178, world_location[1] + 33)
                elif(mission_name == "Golonzo's Battles of Old"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 25 node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 196, world_location[1] + 5)
                elif(mission_name == "The Dungeon Diet"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 30 (44/65) node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 242, world_location[1] + 24)
                elif(mission_name == "Trust Busting Dustup"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 36 (123) node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 319, world_location[1] + 13)
                elif(mission_name == "Erste Kingdom Episode 4"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 70 node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 253, world_location[1] + 136)
                elif(mission_name == "Imperial Wanderer's Soul"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 55 node...")
                    self.game.mouse_tools.move_and_click_point(world_location[0] + 162, world_location[1] + 143)
                
                # After being on the correct chapter node, scroll down the screen as far as possible and then click the mission to start.
                self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now bringing up Summon Selection Screen for \"{mission_name}\"...")
                self.game.mouse_tools.scroll_screen(self.game.home_button_location[0], self.game.home_button_location[1] - 50, -1000)
                temp_mission_name = mission_name.replace(" ", "_")
                
                self.game.find_and_click_button(temp_mission_name)
                
                # Navigate to Episode 4 for the mission "Ch. 70 - Erste Kingdom".
                if(mission_name == "Erste Kingdom Episode 4"):
                    self.game.find_and_click_button("episode_4")
                    self.game.find_and_click_button("ok")
                
            elif(map_mode.lower() == "coop"):
                # Go to the Home Screen.
                self.game.go_back_home(confirm_location_check=True)
                
                # Click the Menu button on the Home Screen, go to Coop Screen, and then confirm that the bot arrived.
                self.game.find_and_click_button("home_menu")
                self.game.find_and_click_button("coop")
                self.game.image_tools.confirm_location("coop")
                
                self.game.mouse_tools.scroll_screen_from_home_button(-400)
                
                # Select the difficulty of the mission that it is under.
                if(mission_name == "In a Dusk Dream"):
                    # Check if the difficulty is already selected. If not, make it active.
                    if(self.game.image_tools.find_button("coop_hard_selected") == None):
                        self.game.find_and_click_button("coop_hard")
                        
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Hard difficulty for Coop is now selected.")
                    
                    # Select the category, "Save the Oceans", which should be the 3rd category.
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Now navigating to \"{mission_name}\" for Hard difficulty.")
                    host_quests_buttons = self.game.image_tools.find_all("coop_host_quest")
                    self.game.mouse_tools.move_and_click_point(host_quests_buttons[2][0], host_quests_buttons[2][1])
                    
                    self.game.image_tools.confirm_location("coop_save_the_oceans")
                    
                    # Now click "In a Dusk Dream".
                    host_quests_circle_buttons = self.game.image_tools.find_all("coop_host_quest_circle")
                    self.game.mouse_tools.move_and_click_point(host_quests_circle_buttons[0][0], host_quests_circle_buttons[0][1])
                else:
                    # Check if the difficulty is already selected. If not, make it active.
                    if(self.game.image_tools.find_button("coop_extra_selected") == None):
                        self.game.find_and_click_button("coop_extra")
                        
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Extra difficulty for Coop is now selected.")
                    
                    coop_ex1_list = ["Corridor of Puzzles", "empty", "Lost in the Dark"]
                    coop_ex2_list = ["Time of Judgement", "Time of Revelation", "Time of Eminence"]
                    coop_ex3_list = ["Rule of the Tundra", "Rule of the Plains", "Rule of the Twilight"]
                    coop_ex4_list = ["Amidst the Waves", "Amidst the Petals", "Amidst Severe Cliffs", "Amidst the Flames"]
                    
                    # Make the specified EX category active. Then click the mission's button while making sure that the first mission in each category is skipped.
                    if(mission_name in coop_ex1_list):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now navigating to \"{mission_name}\" from EX1...")
                        host_quests_buttons = self.game.image_tools.find_all("coop_host_quest")
                        self.game.mouse_tools.move_and_click_point(host_quests_buttons[0][0], host_quests_buttons[0][1])
                        
                        self.game.image_tools.confirm_location("coop_ex1")

                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now selecting \"{mission_name}\"...")
                        host_quests_circle_buttons = self.game.image_tools.find_all("coop_host_quest_circle")
                        self.game.mouse_tools.move_and_click_point(host_quests_circle_buttons[coop_ex1_list.index(mission_name)][0], host_quests_circle_buttons[coop_ex1_list.index(mission_name)][1])
                    elif(mission_name in coop_ex2_list):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now navigating to \"{mission_name}\" from EX2...")
                        host_quests_buttons = self.game.image_tools.find_all("coop_host_quest")
                        self.game.mouse_tools.move_and_click_point(host_quests_buttons[1][0], host_quests_buttons[1][1])
                        
                        self.game.image_tools.confirm_location("coop_ex2")

                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now selecting \"{mission_name}\"...")
                        host_quests_circle_buttons = self.game.image_tools.find_all("coop_host_quest_circle")
                        self.game.mouse_tools.move_and_click_point(host_quests_circle_buttons[coop_ex2_list.index(mission_name) + 1][0], host_quests_circle_buttons[coop_ex2_list.index(mission_name) + 1][1])
                    elif(mission_name in coop_ex3_list):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now navigating to \"{mission_name}\" from EX3.")
                        host_quests_buttons = self.game.image_tools.find_all("coop_host_quest")
                        self.game.mouse_tools.move_and_click_point(host_quests_buttons[2][0], host_quests_buttons[2][1])
                        
                        self.game.image_tools.confirm_location("coop_ex3")

                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now selecting \"{mission_name}\"...")
                        host_quests_circle_buttons = self.game.image_tools.find_all("coop_host_quest_circle")
                        self.game.mouse_tools.move_and_click_point(host_quests_circle_buttons[coop_ex3_list.index(mission_name) + 1][0], host_quests_circle_buttons[coop_ex3_list.index(mission_name) + 1][1])
                    elif(mission_name in coop_ex4_list):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now navigating to \"{mission_name}\" from EX4.")
                        host_quests_buttons = self.game.image_tools.find_all("coop_host_quest")
                        self.game.mouse_tools.move_and_click_point(host_quests_buttons[3][0], host_quests_buttons[3][1])
                        
                        self.game.image_tools.confirm_location("coop_ex4")

                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now selecting \"{mission_name}\"...")
                        host_quests_circle_buttons = self.game.image_tools.find_all("coop_host_quest_circle")
                        self.game.mouse_tools.move_and_click_point(host_quests_circle_buttons[coop_ex4_list.index(mission_name) + 1][0], host_quests_circle_buttons[coop_ex4_list.index(mission_name) + 1][1])
                
                # After clicking on the mission, create a new Room.
                self.game.print_and_save(f"{self.game.printtime()} [INFO] Opening up a new Coop room...")
                self.game.find_and_click_button("coop_post_to_crew_chat")
                self.game.find_and_click_button("ok")
                
                # Finally, click "Select Party".
                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting a Party for \"{mission_name}\".")
                self.game.find_and_click_button("coop_select_party")

            elif(map_mode.lower() == "special"):
                # Go to the Home Screen.
                self.game.go_back_home(confirm_location_check=True)
                
                # Go to the Quest Screen and then to the Special Screen.
                self.game.find_and_click_button("quest", suppress_error=True)
                self.game.find_and_click_button("special")
                
                # Process the strings to eventually be used later.
                temp_map_name = map_name.lower().replace(" ", "_")
                temp_mission_name = mission_name
                if(difficulty == "Normal"):
                    temp_mission_name = mission_name[1:]
                elif(difficulty == "Hard"):
                    temp_mission_name = mission_name[1:]
                elif(difficulty == "Very Hard"):
                    temp_mission_name = mission_name[3:]
                elif(difficulty == "Extreme"):
                    temp_mission_name = mission_name[3:]
                    
                # If the first character is a whitespace after processing the string, remove it.
                if(temp_mission_name[0] == " "):
                    temp_mission_name = temp_mission_name[1:]

                if(self.game.image_tools.confirm_location("special")):
                    tries = 2
                    while(tries != 0):
                        # Bring up the mission's difficulty screen. If it cannot find it, loop for a maximum of 2 times while 
                        # scrolling the screen down to see more in order to find the Special mission.
                        mission_select_button = self.game.image_tools.find_button(temp_map_name)
                        if(mission_select_button != None):
                            self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Navigating to {map_name}...")
                            
                            # Move to the specified Special location by clicking its Select button.
                            special_quest_select_button = (mission_select_button[0] + 145, mission_select_button[1] + 75)
                            self.game.mouse_tools.move_and_click_point(special_quest_select_button[0], special_quest_select_button[1])
                            self.game.wait(1)
                            
                            if(map_name == "Basic Treasure Quests"):
                                if(temp_mission_name == "Scarlet Trial"):
                                    # Navigate to Scarlet Trial.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Scarlet Trial...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[0][0], trial_buttons[0][1])
                                elif(temp_mission_name == "Cerulean Trial"):
                                    # Navigate to Cerulean Trial.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Cerulean Trial...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[1][0], trial_buttons[1][1])
                                elif(temp_mission_name == "Violet Trial"):
                                    # Navigate to Violet Trial.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Violet Trial...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[2][0], trial_buttons[2][1])
                                    
                                # Now start the Trial with the specified difficulty.
                                self.game.wait(1)
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Now navigating to {difficulty}...")
                                difficulty_play_buttons = self.game.image_tools.find_all("play_round_button")
                                
                                if(difficulty == "Normal"):
                                    difficulty_play_button = (difficulty_play_buttons[0][0], difficulty_play_buttons[0][1])
                                elif(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                else:
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                            elif(map_name == "Shiny Slime Search!"):
                                # Start up the Shiny Slime Search! mission by selecting its difficulty.
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting {difficulty} Shiny Slime Search!...")
                                difficulty_play_buttons = self.game.image_tools.find_all("play_round_button")
                                if(difficulty == "Normal"):
                                    difficulty_play_button = (difficulty_play_buttons[0][0], difficulty_play_buttons[0][1])
                                elif(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                else:
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                            elif(map_name == "Six Dragon Trial"):
                                # Start up the Six Dragon Trial mission by selecting its difficulty.
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting {difficulty} Six Dragon Trial...")
                                difficulty_play_buttons = self.game.image_tools.find_all("play_round_button")
                                if(difficulty == "Normal"):
                                    difficulty_play_button = (difficulty_play_buttons[0][0], difficulty_play_buttons[0][1])
                                elif(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                else:
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                            elif(map_name == "Elemental Treasure Quests"):
                                # Start up the specified Elemental Treasure Quest mission.
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting {mission_name}...")
                                difficulty_play_buttons = self.game.image_tools.find_all("play_round_button")
                                if(temp_mission_name == "The Hellfire Trial"):
                                    difficulty_play_button = (difficulty_play_buttons[0][0], difficulty_play_buttons[0][1])
                                elif(temp_mission_name == "The Deluge Trial"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                elif(temp_mission_name == "The Wasteland Trial"):
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                                elif(temp_mission_name == "The Typhoon Trial"):
                                    difficulty_play_button = (difficulty_play_buttons[3][0], difficulty_play_buttons[3][1])
                                elif(temp_mission_name == "The Aurora Trial"):
                                    difficulty_play_button = (difficulty_play_buttons[4][0], difficulty_play_buttons[4][1])
                                elif(temp_mission_name == "The Oblivion Trial"):
                                    difficulty_play_button = (difficulty_play_buttons[5][0], difficulty_play_buttons[5][1])
                            elif(map_name == "Showdowns"):          
                                if(temp_mission_name == "Ifrit Showdown"):
                                    # Navigate to Ifrit Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Ifrit Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[0][0], trial_buttons[0][1])
                                elif(temp_mission_name == "Cocytus Showdown"):
                                    # Navigate to Cocytus Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Cocytus Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[1][0], trial_buttons[1][1])
                                elif(temp_mission_name == "Vohu Manah Showdown"):
                                    # Navigate to Vohu Manah Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Vohu Manah Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[2][0], trial_buttons[2][1])
                                elif(temp_mission_name == "Sagittarius Showdown"):
                                    # Navigate to Sagittarius Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Sagittarius Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[3][0], trial_buttons[3][1])
                                elif(temp_mission_name == "Corow Showdown"):
                                    # Navigate to Corow Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Corow Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[4][0], trial_buttons[4][1])
                                elif(temp_mission_name == "Diablo Showdown"):
                                    # Navigate to Diablo Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Diablo Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("play_round_button")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[5][0], trial_buttons[5][1])
                                    
                                # Now start the Showdown with the specified difficulty.
                                self.game.wait(1)
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Now navigating to {difficulty}...")
                                difficulty_play_buttons = self.game.image_tools.find_all("play_round_button")
                                
                                if(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                elif(difficulty == "Very Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                                elif(difficulty == "Extreme"):
                                    difficulty_play_button = (difficulty_play_buttons[3][0], difficulty_play_buttons[3][1])
                                
                            else:
                                # Start up the Angel Halo mission by selecting its difficulty.
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting {difficulty} Angel Halo...")
                                difficulty_play_buttons = self.game.image_tools.find_all("play_round_button")
                                if(difficulty == "Normal"):
                                    difficulty_play_button = (difficulty_play_buttons[0][0], difficulty_play_buttons[0][1])
                                elif(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                else:
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])

                            # Now click the Play button for the specified difficulty and that should put the bot at the Summon Selection Screen.
                            self.game.mouse_tools.move_and_click_point(difficulty_play_button[0], difficulty_play_button[1])
                            break
                        else:
                            self.game.mouse_tools.scroll_screen(self.game.home_button_location[0], self.game.home_button_location[1] - 50, -500)
                            tries -= 1    
                else:
                    raise Exception("Cannot find the Special Missions.")
            elif(map_mode.lower() == "event"):
                # Go to the Home Screen.
                self.game.go_back_home(confirm_location_check=True)
                
                # Go to the Event by clicking on the Menu button and then click the very first banner.
                self.game.find_and_click_button("home_menu")
                banner_locations = self.game.image_tools.find_all("event_banner")
                self.game.mouse_tools.move_and_click_point(banner_locations[0][0], banner_locations[0][1])
                
                # Check and click away the Daily Missions popup.
                self.game.wait(1)
                if(self.game.image_tools.confirm_location("event_daily_missions", tries=1)):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Detected Daily Missions popup. Clicking it away...")
                    self.game.find_and_click_button("cancel")
                
                # Remove the difficulty prefix from the mission name.
                temp_mission_name = mission_name
                if(difficulty == "Normal"):
                    temp_mission_name = mission_name[1:]
                elif(difficulty == "Hard"):
                    temp_mission_name = mission_name[1:]
                elif(difficulty == "Very Hard"):
                    temp_mission_name = mission_name[3:]
                elif(difficulty == "Extreme"):
                    temp_mission_name = mission_name[3:]
                
                # If the first character is a whitespace after processing the string, remove it.
                if(temp_mission_name[0] == " "):
                    temp_mission_name = temp_mission_name[1:]
                
                # Scroll down the screen a little bit.
                self.game.mouse_tools.scroll_screen_from_home_button(-200)
                
                if(temp_mission_name.lower() == "event raid"):
                    # Bring up the Raid Battle popup. Then scroll down the screen a bit for screens less than 1440p to see the entire popup.
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Now hosting Event Raid...")
                    self.game.find_and_click_button("event_raid_battle")
                    self.game.mouse_tools.scroll_screen_from_home_button(-400)
                    
                    if(difficulty == "Very Hard"):
                        self.game.find_and_click_button("event_very_hard_raid")
                    elif(difficulty == "Extreme"):
                        self.game.find_and_click_button("event_extreme_raid")
                        
                        # If the user does not have enough Treasures to host a Extreme Raid, host a Very Hard Raid instead.
                        if(not self.game.image_tools.wait_vanish("event_extreme_raid", timeout=3)):
                            self.game.print_and_save(f"{self.game.printtime()} [INFO] Not enough materials to host Extreme. Hosting Very Hard instead...")
                            self.game.find_and_click_button("event_very_hard_raid")
                elif(temp_mission_name.lower() == "event quest"):
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Now hosting Event Quest...")
                    self.game.find_and_click_button("event_quests")
                    self.game.wait(1)
                    quest_play_locations = self.game.image_tools.find_all("play_round_button")
                    
                    if(difficulty == "Normal"):
                        self.game.mouse_tools.move_and_click_point(quest_play_locations[0][0], quest_play_locations[0][1])
                    elif(difficulty == "Hard"):
                        self.game.mouse_tools.move_and_click_point(quest_play_locations[1][0], quest_play_locations[1][1])
                    elif(difficulty == "Very Hard"):
                        self.game.mouse_tools.move_and_click_point(quest_play_locations[2][0], quest_play_locations[2][1])
                    elif(difficulty == "Extreme"):
                        self.game.mouse_tools.move_and_click_point(quest_play_locations[3][0], quest_play_locations[3][1])
            elif(map_mode.lower() == "dread barrage"):
                # Go to the Home Screen.
                self.game.go_back_home(confirm_location_check=True)
                
                # Scroll down the screen a little bit and then click the Dread Barrage banner.
                self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now navigating to Dread Barrage...")
                self.game.mouse_tools.scroll_screen_from_home_button(-400)
                self.game.find_and_click_button("dread_barrage")
                self.game.wait(2)
                
                if(self.game.image_tools.confirm_location("dread_barrage")):
                    # Check if there is already a hosted Dread Barrage mission.
                    if(self.game.image_tools.confirm_location("resume_quests", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [WARNING] Detected that there is already a hosted Dread Barrage mission.")
                        expiry_time_in_seconds = 0
                        
                        while(self.game.image_tools.confirm_location("resume_quests", tries=1)):
                            # If there is already a hosted Dread Barrage mission, the bot will wait for a total of 1 hour and 30 minutes 
                            # for either the raid to expire or for anyone in the room to clear it.
                            self.game.print_and_save(f"\n{self.game.printtime()} [WARNING] The bot will now either wait for the expiry time of 1 hour and 30 minutes or for someone else in the room to clear it.")
                            self.game.print_and_save(f"{self.game.printtime()} [WARNING] The bot will now refresh the page every 30 seconds to check if it is still there before proceeding.")
                            self.game.print_and_save(f"{self.game.printtime()} [WARNING] User can either wait it out, revive and fight it to completion, or retreat from the mission manually.")
                            self.game.wait(30)
                            
                            self.game.find_and_click_button("reload")
                            self.game.wait(2)
                            
                            expiry_time_in_seconds += 30
                            if(expiry_time_in_seconds >= 5400):
                                break
                        
                        self.game.print_and_save(f"\n{self.game.printtime()} [SUCCESS] Hosted Dread Barrage mission is now gone either because of timeout or someone else in the room killed it. Moving on...\n")
                    
                    # Find all the Play buttons at the top of the window.
                    dread_barrage_play_button_locations = self.game.image_tools.find_all("dread_barrage_play")
                    
                    # Navigate to the specified difficulty.
                    if(difficulty == "1 Star"):
                        self.game.print_and_save(f"{self.game.printtime()} [INFO] Now starting 1 Star Dread Barrage Raid...")
                        self.game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[0][0], dread_barrage_play_button_locations[0][1])
                    elif(difficulty == "2 Star"):
                        self.game.print_and_save(f"{self.game.printtime()} [INFO] Now starting 2 Star Dread Barrage Raid...")
                        self.game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[1][0], dread_barrage_play_button_locations[1][1])
                    elif(difficulty == "3 Star"):
                        self.game.print_and_save(f"{self.game.printtime()} [INFO] Now starting 3 Star Dread Barrage Raid...")
                        self.game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[2][0], dread_barrage_play_button_locations[2][1])
                    elif(difficulty == "4 Star"):
                        self.game.print_and_save(f"{self.game.printtime()} [INFO] Now starting 4 Star Dread Barrage Raid...")
                        self.game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[3][0], dread_barrage_play_button_locations[3][1])
                    elif(difficulty == "5 Star"):
                        self.game.print_and_save(f"{self.game.printtime()} [INFO] Now starting 5 Star Dread Barrage Raid...")
                        self.game.mouse_tools.move_and_click_point(dread_barrage_play_button_locations[4][0], dread_barrage_play_button_locations[4][1])
                    
                    self.game.wait(2)
                
            # Check for available AP.
            self.game.check_for_ap(use_full_elixirs=self.game.quest_refill)
            
            if(map_mode.lower() != "coop"):
                self.game.print_and_save(f"{self.game.printtime()} [INFO] Now checking if bot is currently at Summon Selection screen...")
                check = self.game.image_tools.confirm_location("select_summon", tries=5)
                if(check):
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Bot is currently at Summon Selection screen.")
                    return True
                else:
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Bot is not at Summon Selection screen.")
                    return False
            else:
                self.game.print_and_save(f"{self.game.printtime()} [INFO] Now checking if bot is currently at Coop Party Selection screen...")
                check = self.game.image_tools.confirm_location("coop_without_support_summon", tries=5)
                if(check):
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Bot is currently at Coop Party Selection screen.")
                    return True
                else:
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Bot is not at Coop Party Selection screen.")
                    return False
        except Exception:
            self.game.print_and_save(f"\n{self.game.printtime()} [ERROR] Bot encountered exception in MapSelection select_map(): \n{traceback.format_exc()}")
            self.game.isBotRunning.value = 1
            
    def check_for_pending(self, map_mode: str, tries: int = 2):
        """Check and collect any pending rewards and free up slots for the bot to join more raids. After this entire process is completed, the bot should end up at the Quest Screen.

        Args:
            map_mode (str): The mode that will dictate what logic to follow next.
            tries (int): Number of tries of checking for Pending Battles.

        Returns:
            (bool): Return True if Pending Battles were detected. Otherwise, return False.
        """
        self.game.wait(1)
        
        try:
            raid_pending_battle_check = False
            if(map_mode.lower() == "raid"):
                while(self.game.image_tools.confirm_location("check_your_pending_battles", tries=tries)):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Found some pending battles that need collecting from.")
                    
                    self.game.find_and_click_button("ok")
                    self.game.wait(1)
                    
                    if(self.game.image_tools.find_button("tap_here_to_see_rewards", tries=2)):
                        self.game.find_and_click_button("tap_here_to_see_rewards")
                        self.game.wait(1)
                        
                        if(self.game.image_tools.confirm_location("no_loot", tries=1)):
                            self.game.print_and_save(f"{self.game.printtime()} [INFO] No loot can be collected.")
                            self.game.find_and_click_button("quests", suppress_error=True)
                            if(self.raids_joined > 0):
                                self.raids_joined -= 1
                            raid_pending_battle_check = True
                        else:
                            self.game.collect_loot(isPendingBattle=True)
                            if(self.raids_joined > 0):
                                self.raids_joined -= 1
                            raid_pending_battle_check = True
                
                # Check if there are any additional Pending Battles.
                if(self.game.image_tools.find_button("quest_results_pending_battles", tries=tries, suppress_error=True)):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Found some additional pending battles that need collecting from.")
                    self.game.find_and_click_button("quest_results_pending_battles")
                    if(self.game.image_tools.confirm_location("pending_battles", tries=2)):
                        while(self.game.image_tools.find_button("tap_here_to_see_rewards", tries=2)):
                            self.game.find_and_click_button("tap_here_to_see_rewards")
                            self.game.wait(1)
                            
                            if(self.game.image_tools.confirm_location("no_loot", tries=1)):
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] No loot can be collected.")
                                self.game.find_and_click_button("quests", suppress_error=True)
                                if(self.raids_joined > 0):
                                    self.raids_joined -= 1
                            else:
                                self.game.collect_loot(isPendingBattle=True)
                                if(self.raids_joined > 0):
                                    self.raids_joined -= 1
                                
                            if(self.game.image_tools.find_button("quest_results_pending_battles", tries=1)):
                                self.game.find_and_click_button("quest_results_pending_battles")
                                while(self.game.image_tools.find_button("tap_here_to_see_rewards", tries=2)):
                                    self.game.find_and_click_button("tap_here_to_see_rewards")
                                    self.game.wait(1)
                                    
                                    if(self.game.image_tools.confirm_location("no_loot", tries=1)):
                                        self.game.print_and_save(f"{self.game.printtime()} [INFO] No loot can be collected.")
                                        self.game.find_and_click_button("quests", suppress_error=True)
                                    else:
                                        self.game.collect_loot(isPendingBattle=True)
                                        
                                    if(self.game.image_tools.find_button("quest_results_pending_battles", tries=1)):
                                        self.game.find_and_click_button("quest_results_pending_battles")
                                    else:
                                        # When there are no more Pending Battles, go back to the Quest Screen.
                                        self.game.find_and_click_button("quests", suppress_error=True)
                                        break
                
                        self.game.print_and_save(f"{self.game.printtime()} [INFO] Pending battles have been cleared for Raids.")
                        return True
                elif(raid_pending_battle_check):
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Pending battles have been collected from for Raids.")
                    return True
            else:
                # Check if the Play Again button is covered by the Pending Battles button.
                if(self.game.image_tools.find_button("quest_results_pending_battles", tries=tries, suppress_error=True)):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Found pending battles that need collecting from.")
                    self.game.find_and_click_button("quest_results_pending_battles")
                    self.game.wait(1)
                    if(self.game.image_tools.confirm_location("pending_battles", tries=1)):
                        while(self.game.image_tools.find_button("tap_here_to_see_rewards", tries=2)):
                            self.game.find_and_click_button("tap_here_to_see_rewards")
                            self.game.wait(1)
                            
                            if(self.game.image_tools.confirm_location("no_loot", tries=1)):
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] No loot can be collected.")
                                self.game.find_and_click_button("quests", suppress_error=True)
                            else:
                                self.game.collect_loot(isPendingBattle=True)
                                
                            if(self.game.image_tools.find_button("quest_results_pending_battles", tries=1)):
                                self.game.find_and_click_button("quest_results_pending_battles")
                            else:
                                # When there are no more Pending Battles, go back to the Quest Screen.
                                self.game.find_and_click_button("quests", suppress_error=True)
                                break
                        
                        self.game.print_and_save(f"{self.game.printtime()} [INFO] Pending battles have been cleared.")
                        return True
                    
            self.game.print_and_save(f"{self.game.printtime()} [INFO] No Pending Battles needed to be cleared.")
            return False
        except Exception:
            self.game.print_and_save(f"\n{self.game.printtime()} [ERROR] Bot encountered exception in MapSelection check_for_pending(): \n{traceback.format_exc()}")
            self.game.isBotRunning.value = 1
    
    def check_for_joined(self):
        """Check and update the number of raids currently joined.

        Returns:
            None
        """
        try:
            self.game.wait(1)
            joined_locations = self.game.image_tools.find_all("joined")
            
            if(joined_locations != None):
                self.raids_joined = len(joined_locations)
                self.game.print_and_save(f"\n{self.game.printtime()} [INFO] There are currently {self.raids_joined} raids joined.")
        
            return None
        except Exception:
            self.game.print_and_save(f"\n{self.game.printtime()} [ERROR] Bot encountered exception in MapSelection check_for_joined(): \n{traceback.format_exc()}")
            self.game.isBotRunning.value = 1
            
    def join_raid(self, item_name: str, mission_name: str):
        """Attempt to join the specified raid.

        Args:
            item_name (str): Name of the item to farm.
            mission_name (str): Name of the mission to farm the item in.

        Returns:
            (bool): Return True if the bot reached the Summon Selection Screen. Otherwise, return False.
        """
        try:
            self.game.go_back_home(confirm_location_check=True)
            self.game.find_and_click_button("quest", suppress_error=True)
            self.check_for_pending("raid")
            self.game.find_and_click_button("raid", suppress_error=True)
            self.check_for_joined()
            
            if(self.raids_joined >= 3):
                # If the maximum number of raids has been joined, collect any pending rewards with a interval of 60 seconds in between until the number is below 3.
                while(self.raids_joined >= 3):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Maximum raids of 3 has been joined. Waiting 60 seconds to see if any finish.")
                    self.game.go_back_home(confirm_location_check=True)

                    self.game.wait(60)
                    self.game.find_and_click_button("quest", suppress_error=True)
                    self.check_for_pending("raid")
            else:
                self.check_for_pending("raid")
            
            self.game.print_and_save(f"{self.game.printtime()} [INFO] Moving to the Enter ID Screen.")
            self.game.find_and_click_button("enter_id")
            
            # Make preparations for farming raids by saving the location of the Join Room button and the Room Code textbox.
            join_room_button = self.game.image_tools.find_button("join_a_room")
            room_code_textbox = (join_room_button[0] - 185, join_room_button[1])

            tries = 10
            while(tries > 0):
                # Find 5 most recent tweets for the specified raid.
                tweets = self.game.room_finder.find_most_recent(mission_name, 5)
                room_codes = self.game.room_finder.clean_tweets(tweets)
                
                # Loop through each acquired room code and try to join one by copying and pasting each code into the textbox.
                for room_code in room_codes:
                    self.game.mouse_tools.click_point_instantly(room_code_textbox[0], room_code_textbox[1])
                    self.game.mouse_tools.clear_textbox()
                    self.game.mouse_tools.copy_to_clipboard(room_code)
                    self.game.mouse_tools.paste_from_clipboard()
                    self.game.mouse_tools.click_point_instantly(join_room_button[0], join_room_button[1])

                    # If the raid is still able to be joined, break out and head to the Summon Selection Screen.
                    if(not self.check_for_pending("raid", tries=1) and not self.game.image_tools.confirm_location("raid_already_ended", tries=1) and not self.game.image_tools.confirm_location("invalid_code", tries=1)):
                        # Check for EP.
                        self.game.check_for_ep(use_soul_balm=self.game.raid_refill)
                        
                        self.game.print_and_save(f"{self.game.printtime()} [SUCCESS] Joining {room_code} was successful.")
                        self.raids_joined += 1
                        return self.game.image_tools.confirm_location("select_summon")
                    else:
                        self.game.print_and_save(f"{self.game.printtime()} [WARNING] {room_code} already ended or invalid.")
                        self.game.find_and_click_button("ok")
                
                tries -= 1
                self.game.print_and_save(f"\n{self.game.printtime()} [WARNING] Could not find any valid room codes. \nWaiting 60 seconds and then trying again with {tries} tries left before exiting.")
                self.game.wait(60)
                
            return False
        except Exception:
            self.game.print_and_save(f"\n{self.game.printtime()} [ERROR] Bot encountered exception in MapSelection join_raid(): \n{traceback.format_exc()}")
            self.game.isBotRunning.value = 1
