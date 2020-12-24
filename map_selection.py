import game


class MapSelection:
    def  __init__(self, game: game.Game, isBotRunning: int, debug_mode: bool = False):
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
        self.game.calibrate_game_window(display_info_check=True)
        
        # TODO: Keep track of attempts desired or item amount desired.
        
        # print(f"Home Button Coordinates: {self.game.home_button_location[0]}, {self.game.home_button_location[1]}")
        
        self.isBotRunning = isBotRunning
        
        self.debug_mode = debug_mode
        
    def select_map(self, map_mode: str, map_name: str, item_name: str, mission_name: str):
        try:
            check_location = False
            
            # Prepare the map name string to be used to look for the correct image file.
            temp_map_name = map_name.replace(" ", "_")
    
            # Example: map_mode = "quest", map_name: "map1", item_name: "Satin Feather", mission_name: "Scattered Cargo"
            if(map_mode.lower() == "quest"):
                self.game.print_and_save("\n********************************************************************************")
                self.game.print_and_save(f"{self.game.printtime()} [INFO] Mode: Quest")
                self.game.print_and_save(f"{self.game.printtime()} [INFO] Map: {map_name}")
                self.game.print_and_save(f"{self.game.printtime()} [INFO] Material to farm: {item_name}")
                self.game.print_and_save(f"{self.game.printtime()} [INFO] Mission: {mission_name}")
                self.game.print_and_save("********************************************************************************\n")
                
                # Go to the Home Screen and check if the bot is already at the correct island or not.
                self.game.go_back_home()
                if(self.game.image_tools.confirm_location(temp_map_name, tries=2)):
                    check_location = True
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot is currently on the correct island.")
                else:
                    check_location = False
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Bot is currently not on the correct island.")
                
                # Go to the Quest Screen.
                self.game.mouse_tools.move_and_click_point(self.game.home_button_location[0] - 37, self.game.home_button_location[1] - 758)
                
                # If the bot is currently not at the correct island, move to it.
                if(check_location == False):
                    location = self.game.image_tools.find_button("world")
                    self.game.mouse_tools.move_and_click_point(location[0], location[1])
                    
                    # TODO: Check for correct Skydom here before proceeding.
                    
                    # On the World Screen, click the specified coordinates on the window to move to the island.
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to {map_name}...")
                    if(map_name == "Port Breeze Archipelago"):
                        location = (self.game.home_button_location[0] - 293, self.game.home_button_location[1] - 1044)
                        self.game.mouse_tools.move_and_click_point(location[0], location[1])
                    elif(map_name == "Valtz Duchy"):
                        location = (self.game.home_button_location[0] - 121, self.game.home_button_location[1] - 973)
                        self.game.mouse_tools.move_and_click_point(location[0], location[1])
                    elif(map_name == "Auguste Isles"):
                        location = (self.game.home_button_location[0] - 345, self.game.home_button_location[1] - 893)
                        self.game.mouse_tools.move_and_click_point(location[0], location[1])
                    elif(map_name == "Lumacie Archipelago"):
                        location = (self.game.home_button_location[0] - 55, self.game.home_button_location[1] - 841)
                        self.game.mouse_tools.move_and_click_point(location[0], location[1])
                        
                    location = self.game.image_tools.find_button("go")
                    self.game.mouse_tools.move_and_click_point(location[0], location[1])
                    self.game.image_tools.confirm_location("quest")

                # Now that the bot is on the correct island and is on the Quest Screen, click the correct chapter node.
                if(mission_name == "Scattered Cargo"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 1 (115) node...")
                    location = (self.game.home_button_location[0] - 280, self.game.home_button_location[1] - 1001)
                    self.game.mouse_tools.move_and_click_point(location[0], location[1])
                elif(mission_name == "Lucky Charm Hunt"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 6 (122) node...")
                    location = (self.game.home_button_location[0] - 41, self.game.home_button_location[1] - 1076)
                    self.game.mouse_tools.move_and_click_point(location[0], location[1])
                elif(mission_name == "Special Op's Request"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 8 node...")
                    location = (self.game.home_button_location[0] - 118, self.game.home_button_location[1] - 940)
                    self.game.mouse_tools.move_and_click_point(location[0], location[1])
                elif(mission_name == "Threat to the Fisheries"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 9 node...")
                    location = (self.game.home_button_location[0] - 158, self.game.home_button_location[1] - 980)
                    self.game.mouse_tools.move_and_click_point(location[0], location[1])
                elif(mission_name == "The Fruit of Lumacie" or mission_name == "Whiff of Danger"):
                    self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Moving to Chapter 13 (39/52) node...")
                    location = (self.game.home_button_location[0] - 296, self.game.home_button_location[1] - 1003)
                    self.game.mouse_tools.move_and_click_point(location[0], location[1])
                elif(mission_name == "I Challenge You!"):
                    pass
                elif(mission_name == "For Whom the Bell Tolls"):
                    pass
                elif(mission_name == "Golonzo's Battle of Old"):
                    pass
                elif(mission_name == "The Dungeon Diet"):
                    pass
                elif(mission_name == "Trust Busting Dustup"):
                    pass
                elif(mission_name == "Erste Kingdom Episode 4"):
                    pass
                elif(mission_name == "Imperial Wanderer's Soul"):
                    pass
                
                # After being on the correct chapter node, scroll down the screen as far as possible and then click the mission to start.
                self.game.print_and_save(f"\n{self.game.printtime()} [INFO] Now bringing up Summon Selection Screen for \"{mission_name}\"...")
                self.game.mouse_tools.scroll_screen(self.game.home_button_location[0], self.game.home_button_location[1] - 50, -1000)
                temp_mission_name = mission_name.replace(" ", "_")
                location = self.game.image_tools.find_button(temp_mission_name)
                self.game.mouse_tools.move_and_click_point(location[0], location[1])  
            # elif(self.farmable_materials[map_mode] == "coop"):
            #     # Go to the Coop Screen.
            #     self.game.go_back_home()
                
            # elif(self.farmable_materials[map_mode] == "special"):
            #     # Go to the Special Quest Screen.
            #     self.game.go_back_home()
            #     quest_button_location = self.game.image_tools.find_button("quest")
            #     self.game.mouse_tools.move_and_click_point(quest_button_location[0], quest_button_location[1])
            #     self.game.image_tools.confirm_location("quest")
            #     special_button_location = self.game.image_tools.find_button("special")
            #     self.game.mouse_tools.move_and_click_point(special_button_location[0], special_button_location[1])
            #     self.game.image_tools.confirm_location("special")
            
            # TODO: Start Summon and Party selection and then start Combat Mode.
        
            self.game.image_tools.confirm_location("select_summon")
        except Exception as e:
            self.game.print_and_save(f"\n{self.game.printtime()} [ERROR] Bot encountered exception on MapSelection select_map(): \n{e}")
        
        return None
    
    
    