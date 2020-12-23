import game
class MapSelection:
    def  __init__(self, game: game.Game, debug_mode: bool = False):
        super().__init__()
        
        # Dictionary of supported farmable materials. Maps selected from recommendations in the GBF wiki website.
        self.farmable_materials = {
            "quest": {
                "map1": {
                    # Port Breeze Archipelago
                    "Satin Feather": "Scattered Cargo",
                    "Zephyr Feather": "Scattered Cargo",
                    "Flying Sprout": "Scattered Cargo",
                },
                "map2": {
                    # Valtz Duchy
                    "Fine Sand Bottle": "Lucky Charm Hunt",
                    "Untamed Flame": "Special Op's Request",
                    "Blistering Ore": ["Lucky Charm Hunt", "Special Op's Request"],
                },
                "map3": {
                    # Auguste Isles
                    "Fresh Water Jug": "Threat to the Fisheries",
                    "Soothing Splash": "Threat to the Fisheries",
                    "Glowing Coral": "Threat to the Fisheries",
                },
                "map4": {
                    # Lumacie Archipelago
                    "Rough Stone": "The Fruit of Lumacie",
                    "Coarse Alluvium": "Whiff of Danger",
                    "Swirling Amber": "The Fruit of Lumacie",
                },
                "map5": {
                    # Albion Citadel
                    "Falcon Feather": "I Challenge You!",
                    "Spring Water Jug": "I Challenge You!",
                    "Vermilion Stone": "I Challenge You!",
                },
                "map6": {
                    # Mist-Shrouded Isle
                    "Slimy Shroom": "For Whom the Bell Tolls",
                    "Hollow Soul": "For Whom the Bell Tolls",
                    "Lacrimosa": "For Whom the Bell Tolls",
                },
                "map7": {
                    # Golonzo Island
                    "Wheat Stalk": "Golonzo's Battle of Old",
                    "Iron Cluster": "Golonzo's Battle of Old",
                    "Olea Plant": "Golonzo's Battle of Old", 
                "Olea Plant": "Golonzo's Battle of Old",
                    "Olea Plant": "Golonzo's Battle of Old", 
                "Olea Plant": "Golonzo's Battle of Old",
                    "Olea Plant": "Golonzo's Battle of Old", 
                "Olea Plant": "Golonzo's Battle of Old",
                    "Olea Plant": "Golonzo's Battle of Old", 
                "Olea Plant": "Golonzo's Battle of Old",
                    "Olea Plant": "Golonzo's Battle of Old", 
                },
                "map8": {
                    # Amalthea Island
                    "Indigo Fruit": "The Dungeon Diet",
                    "Foreboding Clover": "The Dungeon Diet",
                    "Blood Amber": "The Dungeon Diet",
                },
                "map9": {
                    # Former Capital Mephorash
                    "Sand Brick": "Trust Busting Dustup",
                    "Native Reed": "Trust Busting Dustup",
                    "Antique Cloth": ["Trust Busting Dustup", "Erste Kingdom Episode 4"],
                },
                "map10": {
                    # Agastia
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
        
    def select_map(self, map_mode: str, map_name: str):
        if(self.farmable_materials[map_mode] == "quest"):
            # Go to the Quest Screen.
            self.my_game.go_back_home()
            quest_button_location = self.my_game.image_tools.find_button("quest")
            self.my_game.mouse_tools.move_and_click_point(quest_button_location[0], quest_button_location[1])
            self.my_game.image_tools.confirm_location("quest")
            
        elif(self.farmable_materials[map_mode] == "coop"):
            # Go to the Coop Screen.
            self.my_game.go_back_home()
            
        elif(self.farmable_materials[map_mode] == "special"):
            # Go to the Special Quest Screen.
            self.my_game.go_back_home()
            quest_button_location = self.my_game.image_tools.find_button("quest")
            self.my_game.mouse_tools.move_and_click_point(quest_button_location[0], quest_button_location[1])
            self.my_game.image_tools.confirm_location("quest")
            special_button_location = self.my_game.image_tools.find_button("special")
            self.my_game.mouse_tools.move_and_click_point(special_button_location[0], special_button_location[1])
            self.my_game.image_tools.confirm_location("special")
    
        return None
    
    
    