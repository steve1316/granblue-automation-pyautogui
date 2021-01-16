
class MapSelection:
    def  __init__(self, game, debug_mode: bool = False):
        super().__init__()
        
        # Dictionary of supported farmable materials. Maps selected from recommendations in the GBF wiki website.
        self.farmable_materials = {
            "quest": {
                "Port Breeze Archipelago": {
                    "Satin Feather": "Scattered Cargo",
                    "Zephyr Feather": "Scattered Cargo",
                    "Flying Sprout": "Scattered Cargo",
                },
                "Valtz Duchy": {
                    "Fine Sand Bottle": "Lucky Charm Hunt",
                    "Untamed Flame": "Special Op's Request",
                    "Blistering Ore": ["Lucky Charm Hunt", "Special Op's Request"],
                },
                "Auguste Isles": {
                    "Fresh Water Jug": "Threat to the Fisheries",
                    "Soothing Splash": "Threat to the Fisheries",
                    "Glowing Coral": "Threat to the Fisheries",
                },
                "Lumacie Archipelago": {
                    "Rough Stone": "The Fruit of Lumacie",
                    "Coarse Alluvium": "Whiff of Danger",
                    "Swirling Amber": "The Fruit of Lumacie",
                },
                "Albion Citadel": {
                    "Falcon Feather": "I Challenge You!",
                    "Spring Water Jug": "I Challenge You!",
                    "Vermilion Stone": "I Challenge You!",
                },
                "Mist-Shrouded Isle": {
                    "Slimy Shroom": "For Whom the Bell Tolls",
                    "Hollow Soul": "For Whom the Bell Tolls",
                    "Lacrimosa": "For Whom the Bell Tolls",
                },
                "Golonzo Island": {
                    "Wheat Stalk": "Golonzo's Battle of Old",
                    "Iron Cluster": "Golonzo's Battle of Old",
                    "Olea Plant": "Golonzo's Battle of Old", 
                },
                "Amalthea Island": {
                    "Indigo Fruit": "The Dungeon Diet",
                    "Foreboding Clover": "The Dungeon Diet",
                    "Blood Amber": "The Dungeon Diet",
                },
                "Former Capital Mephorash": {
                    "Sand Brick": "Trust Busting Dustup",
                    "Native Reed": "Trust Busting Dustup",
                    "Antique Cloth": ["Trust Busting Dustup", "Erste Kingdom Episode 4"],
                },
                "Agastia": {
                    "Prosperity Flame": "Imperial Wanderer's Soul",
                    "Explosive Material": "Imperial Wanderer's Soul",
                    "Steel Liquid": "Imperial Wanderer's Soul"
                }
            },
            "coop": {
                "Infernal Garnet": "EX2-3",
                "Frozen Hell Prism": "EX3-2",
                "Halo Light Quartz": "EX2-4",
                "Evil Judge Crystal": "EX2-2",
                "Horseman's Plate": "EX3-3",
                "Phantom Demon Jewel": "EX3-4",
                "Gladiator Distinction": ["EX2-3", "EX4-4"],
                "Guardian Distinction": ["EX3-2", "EX4-5"],
                "Pilgrim Distinction": ["EX2-2", "EX4-2"],
                "Mage Distinction": ["EX2-2", "EX4-2"],
                "Bandit Distinction": ["EX2-4", "EX4-5"],
                "Fencer Distinction": ["EX2-3", "EX4-4"],
                "Combatant Distinction": ["EX3-2", "EX4-4"],
                "Sharpshooter Distinction": ["EX3-3", "EX4-3"],
                "Troubadour Distinction": ["EX2-4", "EX4-5"],
                "Cavalryman Distinction": ["EX3-3", "EX4-5"],
                "Alchemist Distinction": ["EX2-2", "EX4-2"],
                "Samurai Distinction": ["EX3-4", "EX4-3"],
                "Ninja Distinction": ["EX3-4", "EX4-3"],
                "Sword Master Distinction": ["EX3-2", "EX4-4"],
                "Gunslinger Distinction": ["EX3-3", "EX4-3"],
                "Mystic Distinction": ["EX2-4", "EX4-2"],
                "Assassin Distinction": ["EX3-4", "EX4-3"],
                "Dual Wielder Distinction": "EX2-3",
                "Shredder Distinction": "EX2-4",
                "Forester's Distinction": "EX2-3",
                "Dragoon's Distinction": ["EX3-2", "EX4-5"],
                "Monk's Distinction": ["EX2-2", "EX4-2"],
                "Longstrider's Distinction": None,
                "Fire Grimoire": "EX4-5",
                "Water Grimoire": "EX4-2",
                "Earth Grimoire": "EX4-4",
                "Wind Grimoire": "EX4-3"
            },
            "special": {
                "Fire Orb": ["Scarlet Trial", "Hellfire Trial"],
                "Water Orb": ["Scarlet Trial", "Deluge Trial"],
                "Earth Orb": ["Scarlet Trial", "Wasteland Trial"],
                "Wind Orb": ["Scarlet Trial", "Typhoon Trial"],
                "Light Orb": ["Scarlet Trial", "Aurora Trial"],
                "Dark Orb": ["Scarlet Trial", "Oblivion Trial"],
                "Inferno Orb": ["Scarlet Trial", "Hellfire Trial"],
                "Frost Orb": ["Scarlet Trial", "Deluge Trial"],
                "Rumbling Orb": ["Scarlet Trial", "Wasteland Trial"],
                "Cyclone Orb": ["Scarlet Trial", "Typhoon Trial"],
                "Shining Orb": ["Scarlet Trial", "Aurora Trial"],
                "Abysm Orb": ["Scarlet Trial", "Oblivion Trial"],
                "Red Tome": ["Cerulean Trial", "Hellfire Trial"],
                "Blue Tome": ["Cerulean Trial", "Deluge Trial"],
                "Brown Tome": ["Cerulean Trial", "Wasteland Trial"],
                "Green Tome": ["Cerulean Trial", "Typhoon Trial"],
                "White Tome": ["Cerulean Trial", "Aurora Trial"],
                "Black Tome": ["Cerulean Trial", "Oblivion Trial"],
                "Hellfire Scroll": ["Cerulean Trial", "Hellfire Trial"],
                "Flood Scroll": ["Cerulean Trial", "Deluge Trial"],
                "Thunder Scroll": ["Cerulean Trial", "Wasteland Trial"],
                "Gale Scroll": ["Cerulean Trial", "Typhoon Trial"],
                "Skylight Scroll": ["Cerulean Trial", "Aurora Trial"],
                "Chasm Scroll": ["Cerulean Trial", "Oblivion Trial"],
                "Infernal Whorl": ["Cerulean Trial", "Angel Halo", "Hellfire Trial"],
                "Tidal Whorl": ["Cerulean Trial", "Angel Halo", "Deluge Trial"],
                "Seismic Whorl": ["Cerulean Trial", "Angel Halo", "Wasteland Trial"],
                "Tempest Whorl": ["Cerulean Trial", "Angel Halo", "Typhoon Trial"],
                "Radiant Whorl": ["Cerulean Trial", "Angel Halo", "Aurora Trial"],
                "Umbral Whorl": ["Cerulean Trial", "Angel Halo"],
                "Prism Chip": ["Violet Trial"],
                "Flawed Prism": ["Violet Trial"],
                "Flawless Prism": ["Violet Trial"],
                "Rainbow Prism": ["Violet Trial"],
                "Red Dragon Scale": ["Six Dragon Trial", "Hellfire Trial"],
                "Blue Dragon Scale": ["Six Dragon Trial", "Deluge Trial"],
                "Brown Dragon Scale": ["Six Dragon Trial", "Wasteland Trial"],
                "Green Dragon Scale": ["Six Dragon Trial", "Typhoon Trial"],
                "White Dragon Scale": ["Six Dragon Trial", "Aurora Trial"],
                "Black Dragon Scale": ["Six Dragon Trial", "Oblivion Trial"]
            }
        }

        self.game = game
        
        self.debug_mode = debug_mode
        
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
            current_location = ""
            
            # Prepare the map name string to be used to look for the correct image file.
            temp_map_name = map_name.replace(" ", "_")
            temp_map_name = temp_map_name.replace("-", "_")
    
            # Example: map_mode = "quest", map_name: "map1", item_name: "Satin Feather", mission_name: "Scattered Cargo"
            if(map_mode.lower() == "quest"):
                # Go to the Home Screen and check if the bot is already at the correct island or not.
                self.game.go_back_home(confirm_location_check=True, display_info_check=True)
                if(self.game.image_tools.confirm_location(temp_map_name, tries=2)):
                    check_location = True
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot is currently on the correct island.")
                else:
                    check_location = False
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot is currently not on the correct island.")
                    
                    # Attempt to see which island the bot is currently at.
                    if(self.game.image_tools.confirm_location("port_breeze_archipelago", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at the Port Breeze Archipelago. Now moving to {map_name}...")
                        current_location = "Port Breeze Archipelago"
                    elif(self.game.image_tools.confirm_location("valtz_duchy", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at the Valtz Duchy. Now moving to {map_name}...")
                        current_location = "Valtz Duchy"
                    elif(self.game.image_tools.confirm_location("auguste_isles", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at the Auguste Isles. Now moving to {map_name}...")
                        current_location = "Auguste Isles"
                    elif(self.game.image_tools.confirm_location("lumacie_archipelago", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at the Lumacie Archipelago. Now moving to {map_name}...")
                        current_location = "Lumacie Archipelago"
                    elif(self.game.image_tools.confirm_location("albion_citadel", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at the Albion Citadel. Now moving to {map_name}...")
                        current_location = "Albion Citadel"
                    elif(self.game.image_tools.confirm_location("mist_shrouded_isle", tries=1)):
                        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot's current location is at the Mist-Shrouded Isle. Now moving to {map_name}...")
                        current_location = "Mist-Shrouded Isle"
                
                # Go to the Quest Screen.
                self.game.find_and_click_button("quest")
                
                # If the bot is currently not at the correct island, move to it.
                if(check_location == False):
                    world_location = self.game.image_tools.find_button("world")
                    self.game.mouse_tools.move_and_click_point(world_location[0], world_location[1])
                    
                    # TODO: Check for correct Skydom here before proceeding.
                    
                    # On the World Screen, click the specified coordinates on the window to move to the island. 
                    # If the island is on a different world page, switch pages as necessary.
                    # TODO: Eventually fill this out with every island. Same thing with the farmable missions below.
                    if(map_name == "Port Breeze Archipelago"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash"):
                            self.game.find_and_click_button("world_left_arrow")
                        self.game.find_and_click_button("port_breeze_archipelago")
                    elif(map_name == "Valtz Duchy"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash"):
                            self.game.find_and_click_button("world_left_arrow")
                        self.game.find_and_click_button("valtz_duchy")
                    elif(map_name == "Auguste Isles"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash"):
                            self.game.find_and_click_button("world_left_arrow")
                        self.game.find_and_click_button("auguste_isles")
                    elif(map_name == "Lumacie Archipelago"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash"):
                            self.game.find_and_click_button("world_left_arrow")
                        self.game.find_and_click_button("lumacie_archipelago")
                    elif(map_name == "Albion Citadel"):
                        if(current_location == "Mist-Shrouded Isle" or current_location == "Golonzo Island" or current_location == "Amalthea Island" or current_location == "Former Capital Mephorash"):
                            self.game.find_and_click_button("world_left_arrow")
                        self.game.find_and_click_button("albion_citadel")
                    elif(map_name == "Mist-Shrouded Isle"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        self.game.find_and_click_button("mist_shrouded_isle")
                    elif(map_name == "Golonzo Island"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        self.game.find_and_click_button("golonzo_island")
                    elif(map_name == "Amalthea Island"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        self.game.find_and_click_button("amalthea_island")
                    elif(map_name == "Former Capital Mephorash"):
                        if(current_location == "Port Breeze Archipelago" or current_location == "Valtz Duchy" or current_location == "Auguste Isles" or current_location == "Lumacie Archipelago"or current_location == "Albion Citadel"):
                            self.game.find_and_click_button("world_right_arrow")
                        self.game.find_and_click_button("former_capital_mephorash")
                        
                    location = self.game.image_tools.find_button("go")
                    self.game.mouse_tools.move_and_click_point(location[0], location[1])
                    self.game.image_tools.confirm_location("quest")

                # Now that the bot is on the correct island and is on the Quest Screen, click the correct chapter node. 126,268
                world_location = self.game.image_tools.find_button("world")
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
                elif(mission_name == "Golonzo's Battle of Old"):
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
                    raise Exception("Erste Kingdom Episode 4 is not supported yet.")
                elif(mission_name == "Imperial Wanderer's Soul"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 55 node...")
                    raise Exception("Imperial Wanderer's Soul is not supported yet.")
                
                # After being on the correct chapter node, scroll down the screen as far as possible and then click the mission to start.
                self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now bringing up Summon Selection Screen for \"{mission_name}\"...")
                self.game.mouse_tools.scroll_screen(self.game.home_button_location[0], self.game.home_button_location[1] - 50, -1000)
                temp_mission_name = mission_name.replace(" ", "_")
                
                mission_location = self.game.image_tools.find_button(temp_mission_name)
                self.game.mouse_tools.move_and_click_point(mission_location[0], mission_location[1])
                
                # Check for available AP.
                self.game.check_for_ap(use_full_elixirs=False)
                
            # elif(self.farmable_materials[map_mode] == "coop"):
            #     # Go to the Coop Screen.
            #     self.game.go_back_home()
                
            elif(map_mode.lower() == "special"):
                # Go to the Home Screen.
                self.game.go_back_home(confirm_location_check=True, display_info_check=True)
                
                # Go to the Quest Screen and then to the Special Screen.
                self.game.find_and_click_button("quest")
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
                            self.game.print_and_save(f"{self.game.printtime()} [INFO] Navigating to {map_name}...")
                            
                            # Move to the specified Special location by clicking its Select button.
                            special_quest_select_button = (mission_select_button[0] + 145, mission_select_button[1] + 75)
                            self.game.mouse_tools.move_and_click_point(special_quest_select_button[0], special_quest_select_button[1])
                            self.game.wait_for_ping(1)
                            
                            if(map_name == "Basic Treasure Quests"):
                                if(temp_mission_name == "Scarlet Trial"):
                                    # Navigate to Scarlet Trial.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Scarlet Trial...")
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[0][0], trial_buttons[0][1])
                                elif(temp_mission_name == "Cerulean Trial"):
                                    # Navigate to Cerulean Trial.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Cerulean Trial...")
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[1][0], trial_buttons[1][1])
                                elif(temp_mission_name == "Violet Trial"):
                                    # Navigate to Violet Trial.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Violet Trial...")
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[2][0], trial_buttons[2][1])
                                    
                                # Now start the Trial with the specified difficulty.
                                self.game.wait_for_ping(1)
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Now navigating to {difficulty}...")
                                difficulty_play_buttons = self.game.image_tools.find_all("special_play")
                                
                                if(difficulty == "Normal"):
                                    difficulty_play_button = (difficulty_play_buttons[0][0], difficulty_play_buttons[0][1])
                                elif(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                else:
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                            elif(map_name == "Shiny Slime Search!"):
                                # Start up the Shiny Slime Search! mission by selecting its difficulty.
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting {difficulty} Shiny Slime Search!...")
                                difficulty_play_buttons = self.game.image_tools.find_all("special_play")
                                if(difficulty == "Normal"):
                                    difficulty_play_button = (difficulty_play_buttons[0][0], difficulty_play_buttons[0][1])
                                elif(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                else:
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                            elif(map_name == "Six Dragon Trial"):
                                # Start up the Six Dragon Trial mission by selecting its difficulty.
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting {difficulty} Six Dragon Trial...")
                                difficulty_play_buttons = self.game.image_tools.find_all("special_play")
                                if(difficulty == "Normal"):
                                    difficulty_play_button = (difficulty_play_buttons[0][0], difficulty_play_buttons[0][1])
                                elif(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                else:
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                            elif(map_name == "Elemental Treasure Quests"):
                                # Start up the specified Elemental Treasure Quest mission.
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting {mission_name}...")
                                difficulty_play_buttons = self.game.image_tools.find_all("special_play")
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
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[0][0], trial_buttons[0][1])
                                elif(temp_mission_name == "Cocytus Showdown"):
                                    # Navigate to Cocytus Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Cocytus Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[1][0], trial_buttons[1][1])
                                elif(temp_mission_name == "Vohu Manah Showdown"):
                                    # Navigate to Vohu Manah Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Vohu Manah Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[2][0], trial_buttons[2][1])
                                elif(temp_mission_name == "Sagittarius Showdown"):
                                    # Navigate to Sagittarius Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Sagittarius Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[3][0], trial_buttons[3][1])
                                elif(temp_mission_name == "Corow Showdown"):
                                    # Navigate to Corow Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Corow Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[4][0], trial_buttons[4][1])
                                elif(temp_mission_name == "Diablo Showdown"):
                                    # Navigate to Diablo Showdown.
                                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting Diablo Showdown...")
                                    trial_buttons = self.game.image_tools.find_all("special_play")
                                    self.game.mouse_tools.move_and_click_point(trial_buttons[5][0], trial_buttons[5][1])
                                    
                                # Now start the Showdown with the specified difficulty.
                                self.game.wait_for_ping(1)
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Now navigating to {difficulty}...")
                                difficulty_play_buttons = self.game.image_tools.find_all("special_play")
                                
                                if(difficulty == "Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[1][0], difficulty_play_buttons[1][1])
                                elif(difficulty == "Very Hard"):
                                    difficulty_play_button = (difficulty_play_buttons[2][0], difficulty_play_buttons[2][1])
                                elif(difficulty == "Extreme"):
                                    difficulty_play_button = (difficulty_play_buttons[3][0], difficulty_play_buttons[3][1])
                                
                            else:
                                # Start up the Angel Halo mission by selecting its difficulty.
                                self.game.print_and_save(f"{self.game.printtime()} [INFO] Selecting {difficulty} Angel Halo...")
                                difficulty_play_buttons = self.game.image_tools.find_all("special_play")
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
            return self.game.image_tools.confirm_location("select_summon")
        except Exception as e:
            self.game.print_and_save(f"\n{self.game.printtime()} [ERROR] Bot encountered exception on MapSelection select_map(): \n{e}")
            
    def check_for_pending(self):
        """Check and collect any pending rewards and free up slots for the bot to join more raids. After this entire process is completed, the bot should end up at the Quest Screen.

        Returns:
            None
        """
        while(self.game.image_tools.confirm_location("check_your_pending_battles", tries=2)):
            self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Found some pending battles that need collecting from.")
            
            self.game.find_and_click_button("ok")
            self.game.wait_for_ping(1)
            
            if(self.game.image_tools.find_button("pending_battle_sidebar", tries=1)):
                self.game.find_and_click_button("pending_battle_sidebar")
                self.game.wait_for_ping(1)
                
                if(self.game.image_tools.confirm_location("no_loot", tries=1)):
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] No loot can be collected.")
                    self.game.find_and_click_button("raid_quests")
                    self.raids_joined -= 1
                else:
                    self.game.collect_loot()
                    self.raids_joined -= 1
        
        self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Pending battles have been cleared. Continuing to the Backup Requests Screen...")
        return None
            
    def join_raid(self, item_name: str, mission_name: str):
        """Attempt to join the specified raid.

        Args:
            item_name (str): Name of the item to farm.
            mission_name (str): Name of the mission to farm the item in.

        Returns:
            (bool): Return True if the bot reached the Summon Selection Screen. Otherwise, return False.
        """
        if(not self.game.image_tools.confirm_location("raid", tries=1)):
            if(self.raids_joined >= 3):
                # If the maximum number of raids has been joined, collect any pending rewards with a interval of 60 seconds in between until the number is below 3.
                while(self.raids_joined >= 3):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Maximum raids of 3 has been joined. Waiting 60 seconds to see if any finish.")
                    self.game.go_back_home(confirm_location_check=True)

                    self.game.wait_for_ping(60)
                    self.game.find_and_click_button("quest", suppress_error=True)
                    self.check_for_pending()
            else:
                # Navigate to the Quest Screen -> Backup Requests Screen -> Enter ID Screen.
                self.game.find_and_click_button("quest", suppress_error=True)
                self.check_for_pending()
            
            self.game.find_and_click_button("raid", suppress_error=True)
        
        self.game.print_and_save(f"{self.game.printtime()} [INFO] Moving to the Enter ID Screen.")
        self.game.find_and_click_button("enter_id")
        
        # Make preparations for farming raids by saving the location of the Join Room button and the Room Code textbox.
        join_room_button = self.game.image_tools.find_button("join_a_room")
        room_code_textbox = (join_room_button[0] - 185, join_room_button[1])

        tries = 5
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
                
                # Check for pending rewards popup.
                self.check_for_pending()
                
                # If the raid is still able to be joined, break out and head to the Summon Selection Screen.
                self.game.wait_for_ping(1)
                if(not self.game.image_tools.confirm_location("raid_already_ended", tries=1) and not self.game.image_tools.confirm_location("invalid_code", tries=1)):
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] Joining {room_code} was successful.")
                    self.raids_joined += 1
                    return self.game.image_tools.confirm_location("select_summon")
                else:
                    self.game.print_and_save(f"{self.game.printtime()} [INFO] {room_code} already ended or invalid.")
                    self.game.find_and_click_button("ok")
            
            tries -= 1
            self.game.print_and_save(f"\n{self.game.printtime()} [WARNING] Could not find any valid room codes. \nWaiting 60 seconds and then trying again with {tries} tries left before exiting.")
            self.game.wait_for_ping(60)
            
        return False