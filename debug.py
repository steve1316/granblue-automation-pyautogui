import datetime
import sys

import pyautogui
import tweepy


class Debug:
    """
    Test driver for most bot functionality.

    Attributes
    ----------
    game (game.Game): The Game object to test with.
    
    isBotRunning (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
    
    combat_script (str): The combat script to test with.

    """

    def __init__(self, game, isBotRunning: int, combat_script: str = ""):
        super().__init__()

        self.game = game
        self.isBotRunning = isBotRunning
        self.combat_script = combat_script
        
    def test_twitter_listener(self):
        """Tests finding 10 most recent Grimnir room codes from EN.
        
        Args:
            None
            
        Return:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing Finding 10 Most Recent Grimnir Room Codes...")
        self.game.print_and_save("################################################################################")
        
        tweets = self.game.room_finder.find_most_recent("Lvl 120 Grimnir")
        room_codes = self.game.room_finder.clean_tweets(tweets)
        self.game.print_and_save(f"\n{self.game.printtime()} [TEST_INFO] {len(tweets)}")
        self.game.print_and_save(f"\n{self.game.printtime()} [TEST_INFO] {len(room_codes)}")
        for i, room_code in enumerate(room_codes):
            self.game.print_and_save(f"\n{self.game.printtime()} [TEST] {tweets[i].lang.upper()} Tweet created at {tweets[i].created_at}: \n" + tweets[i].text)
            self.game.print_and_save(f"{self.game.printtime()} [TEST] Detected Room Code is: {room_codes[i]}")
            
        self.game.print_and_save(f"\n{self.game.printtime()} [TEST_SUCCESS] Testing Finding 10 Most Recent Grimnir Room Codes from EN was successful.")
        self.isBotRunning.value = 1
        return None
        
    def test_farming_mode(self):
        """Tests the Farming Mode by navigating to the Special Op's Request and farm 10 Fine Sand Bottles with the specified party and summon.
            
        Return:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing Farming Mode for 10x Fine Sand Bottles from Special Op's Request on Valtz Duchy...")
        self.game.print_and_save("################################################################################")
        
        self.game.start_farming_mode(summon_element_name="water", summon_name="leviathan_omega", group_number=1, party_number=3, 
                                     map_mode="quest", map_name="Valtz Duchy", item_name="Fine Sand Bottle", item_amount_to_farm=10, 
                                     mission_name="Special Op's Request")
        
        self.game.print_and_save(f"\n{self.game.printtime()} [TEST_SUCCESS] Testing Farming Mode was successful.")
        self.isBotRunning.value = 1
        return None
        
    def test_item_detection(self, items_to_test: int):
        """Test finding amounts of all items on the screen.

        Args:
            items_to_test (int): The index of the item_list inside this method that you want to test text detection against.
            
        Return:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing finding amounts of all items on screen...")
        self.game.print_and_save("################################################################################")
        
        item_list = {
            1: ["Satin Feather", "Zephyr Feather", "Flying Sprout"],
            2: ["Fine Sand Bottle", "Untamed Flame", "Blistering Ore"],
            3: ["Fresh Water Jug", "Soothing Splash", "Glowing Coral"],
            4: ["Rough Stone", "Coarse Alluvium", "Swirling Amber"],
            5: ["Fire Orb", "Water Orb", "Earth Orb", "Wind Orb", "Light Orb", "Dark Orb"],
            6: ["Inferno Orb", "Frost Orb", "Rumbling Orb", "Cyclone Orb", "Shining Orb", "Abysm Orb"],
            7: ["Red Tome", "Blue Tome", "Brown Tome", "Green Tome", "White Tome", "Black Tome"],
            8: ["Hellfire Scroll", "Flood Scroll", "Thunder Scroll", "Gale Scroll", "Skylight Scroll", "Chasm Scroll"],
            9: ["Infernal Whorl", "Tidal Whorl", "Seismic Whorl", "Tempest Whorl", "Radiant Whorl", "Umbral Whorl"],
            10: ["Prism Chip", "Flawed Prism", "Flawless Prism", "Rainbow Prism"],
            11: ["Red Dragon Scale", "Blue Dragon Scale", "Brown Dragon Scale", "Green Dragon Scale", "White Dragon Scale", "Black Dragon Scale"],
            12: ["Hellfire Fragment", "Deluge Fragment", "Wasteland Fragment", "Typhoon Fragment"],
            13: ["Jasper Scale", "Scorching Peak", "Infernal Garnet", "Ifrit Anima", "Ifrit Omega Anima", "Fire Grimoire"],
            14: ["Mourning Stone", "Crystal Spirit", "Frozen Hell Prism", "Cocytus Anima", "Cocytus Omega Anima", "Water Grimoire"],
            15: ["Scrutiny Stone", "Luminous Judgment", "Evil Judge Crystal", "Vohu Manah Anima", "Vohu Manah Omega Anima", "Earth Grimoire"],
            16: ["Sagittarius Arrowhead", "Sagittarius Rune", "Horseman's Plate", "Sagittarius Anima", "Sagittarius Omega Anima", "Wind Grimoire"],
            17: ["Solar Ring", "Sunlight Quartz", "Halo Light Quartz", "Corow Anima", "Corow Omega Anima"],
            18: ["Twilight Cloth Strip", "Shadow Silver", "Phantom Demon Jewel", "Diablo Anima", "Diablo Omega Anima"]
        }
        
        for item in item_list[items_to_test]:
            result = self.game.image_tools.find_farmed_items([item])
            self.game.print_and_save(f"\n{self.game.printtime()} [TEST] {item} farmed: {result}")
            
        self.game.print_and_save(f"\n{self.game.printtime()} [TEST_SUCCESS] Testing Item Detection was successful.")
        self.isBotRunning.value = 1
        return None
        
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
        return None

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
        return None

    def test_combat_mode2(self):
        """Tests almost all of the bot's functionality via navigation and combat by starting the Old Lignoid Trial Battle and fighting it. The combat mode will go on indefinitely until stopped.

        Returns:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing Combat Mode on the Old Lignoid trial battle mission now...")
        self.game.print_and_save("################################################################################")
        
        self.game.go_back_home(confirm_location_check=True, display_info_check=True)
        self.mouse_tools.scroll_screen_from_home_button(-600)

        list_of_steps_in_order = ["gameplay_extras", "trial_battles",
                                  "trial_battles_old_lignoid", "trial_battles_play",
                                  "choose_a_summon", "party_selection_ok", "trial_battles_close"]

        # Go through each step in order from left to right from the list of steps.
        while (len(list_of_steps_in_order) > 0):
            step = list_of_steps_in_order.pop(0)
            
            if(step == "trial_battles_old_lignoid"):
                self.image_tools.confirm_location("trial_battles")
            
            image_location = self.image_tools.find_button(step)
            
            if(step == "choose_a_summon"):
                self.mouse_tools.move_and_click_point(image_location[0], image_location[1] + 187)
            else:
                self.mouse_tools.move_and_click_point(image_location[0], image_location[1])
        
        self.game.start_combat_mode(self.combat_script)
        
        self.isBotRunning.value = 1
        return None
    
    def test_combat_mode(self):
        """Tests almost all of the bot's functionality via navigation and combat by starting the Very Hard difficulty Angel Halo Special Battle and completing it.

        Returns:
            None
        """
        self.game.print_and_save("\n################################################################################")
        self.game.print_and_save(f"{self.game.printtime()} [TEST] Testing Combat Mode on Very Hard Difficulty Angel Halo mission now...")
        self.game.print_and_save("################################################################################")

        self.game.start_farming_mode("dark", "Celeste Omega", 6, 1, "special", "Angel Halo", "EXP", 1, "VH Angel Halo")

        self.game.print_and_save(f"\n{self.game.printtime()} [TEST_SUCCESS] Testing Combat Mode was successful.")
        
        self.isBotRunning.value = 1
        return None
