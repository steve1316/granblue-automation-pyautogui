class Debug:
    """
    Test driver for most bot functionality.

    Attributes
    ----------
    game (game.Game): The Game object to test with.
    
    isBotRunning (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
    
    combat_script (str): The combat script to test with.

    """

    def __init__(self, game, is_bot_running: int, combat_script: str = ""):
        super().__init__()

        self._game = game
        self._is_bot_running = is_bot_running
        self._combat_script = combat_script

    def test_twitter_listener(self):
        """Tests finding 10 most recent Grimnir room codes from EN.
        
        Args:
            None
            
        Return:
            None
        """
        self._game.print_and_save("\n################################################################################")
        self._game.print_and_save(f"{self._game.printtime()} [TEST] Testing Finding 10 Most Recent Grimnir Room Codes...")
        self._game.print_and_save("################################################################################")

        tweets = self._game.room_finder.find_most_recent("Lvl 120 Grimnir")
        room_codes = self._game.room_finder.clean_tweets(tweets)
        self._game.print_and_save(f"\n{self._game.printtime()} [TEST_INFO] # of Tweets found: {len(tweets)}")
        self._game.print_and_save(f"{self._game.printtime()} [TEST_INFO] # of Room Codes detected: {len(room_codes)}")
        for i, room_code in enumerate(room_codes):
            self._game.print_and_save(f"\n{self._game.printtime()} [TEST] {tweets[i].lang.upper()} Tweet created at {tweets[i].created_at}: \n" + tweets[i].text)
            self._game.print_and_save(f"{self._game.printtime()} [TEST] Detected Room Code is: {room_codes[i]}")

        self._game.print_and_save(f"\n{self._game.printtime()} [TEST_SUCCESS] Testing Finding 10 Most Recent Grimnir Room Codes was successful.")
        self._is_bot_running.value = 1
        return None

    def test_farming_mode(self):
        """Tests the Farming Mode by navigating to the Special Op's Request and farm 10 Fine Sand Bottles with the specified party and summon.
            
        Return:
            None
        """
        self._game.print_and_save("\n################################################################################")
        self._game.print_and_save(f"{self._game.printtime()} [TEST] Testing Farming Mode for 10x Fine Sand Bottles from Special Op's Request on Valtz Duchy...")
        self._game.print_and_save("################################################################################")

        self._game.start_farming_mode(summon_element_name = "water", summon_name = "leviathan_omega", group_number = 1, party_number = 3, map_mode = "quest", map_name = "Valtz Duchy",
                                      item_name = "Fine Sand Bottle", item_amount_to_farm = 10, mission_name = "Special Op's Request")

        self._game.print_and_save(f"\n{self._game.printtime()} [TEST_SUCCESS] Testing Farming Mode was successful.")
        self._is_bot_running.value = 1
        return None

    def test_item_detection(self, items_to_test: int):
        """Test finding amounts of all items on the screen.

        Args:
            items_to_test (int): The index of the item_list inside this method that you want to test text detection against.
            
        Return:
            None
        """
        self._game.print_and_save("\n################################################################################")
        self._game.print_and_save(f"{self._game.printtime()} [TEST] Testing finding amounts of all items on screen...")
        self._game.print_and_save("################################################################################")

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
            18: ["Twilight Cloth Strip", "Shadow Silver", "Phantom Demon Jewel", "Diablo Anima", "Diablo Omega Anima"],
            19: ["Tiamat Anima", "Tiamat Omega Anima", "Colossus Anima", "Colossus Omega Anima", "Leviathan Anima", "Leviathan Omega Anima",
                 "Yggdrasil Anima", "Yggdrasil Omega Anima", "Luminiera Anima", "Luminiera Omega Anima", "Celeste Anima", "Celeste Omega Anima"],
            20: ["Gladiator Distinction", "Guardian Distinction", "Pilgrim Distinction", "Mage Distinction", "Bandit Distinction",
                 "Fencer Distinction", "Combatant Distinction",
                 "Sharpshooter Distinction", "Troubadour Distinction", "Cavalryman Distinction", "Alchemist Distinction", "Samurai Distinction",
                 "Ninja Distinction", "Sword Master Distinction",
                 "Gunslinger Distinction", "Mystic Distinction", "Assassin Distinction", "Dual Wielder Distinction", "Shredder Distinction",
                 "Forester's Distinction", "Dragoon's Distinction",
                 "Monk's Distinction", "Longstrider's Distinction"],
            21: ["Avenger Replica", "Skofnung Replica", "Oliver Replica", "Aschallon Replica", "Nirvana Replica", "Keraunos Replica",
                 "Hellion Gauntlet Replica",
                 "Ipetam Replica", "Rosenbogen Replica", "Langeleik Replica", "Romulus Spear Replica", "Proximo Replica", "Murakumo Replica",
                 "Nebuchad Replica",
                 "Misericorde Replica", "Faust Replica", "Muramasa Replica", "Kapilavastu Replica", "Practice Drum"],
            22: ["Rusted Sword", "Rusted Dagger", "Rusted Lance", "Rusted Axe", "Rusted Staff", "Rusted Gun", "Rusted Gauntlet", "Rusted Bow",
                 "Rusted Harp", "Rusted Katana"],
            23: ["Warrior Creed", "Mage Creed"],
        }

        for item in item_list[items_to_test]:
            result = self._game.image_tools.find_farmed_items([item])
            self._game.print_and_save(f"\n{self._game.printtime()} [TEST] {item} farmed: {result}")

        self._game.print_and_save(f"\n{self._game.printtime()} [TEST_SUCCESS] Testing Item Detection was successful.")
        self._is_bot_running.value = 1
        return None

    def test_combat_mode2(self):
        """Tests almost all of the bot's functionality via navigation and combat by starting the Old Lignoid Trial Battle and fighting it. The combat mode will go on indefinitely until stopped.

        Returns:
            None
        """
        self._game.print_and_save("\n################################################################################")
        self._game.print_and_save(f"{self._game.printtime()} [TEST] Testing Combat Mode on the Old Lignoid trial battle mission now...")
        self._game.print_and_save("################################################################################")

        self._game.go_back_home(confirm_location_check = True, display_info_check = True)
        self._game.mouse_tools.scroll_screen_from_home_button(-600)

        list_of_steps_in_order = ["gameplay_extras", "trial_battles", "trial_battles_old_lignoid", "play_round_button", "choose_a_summon", "party_selection_ok", "close"]

        # Go through each step in order from left to right from the list of steps.
        while len(list_of_steps_in_order) > 0:
            step = list_of_steps_in_order.pop(0)
            if step == "trial_battles_old_lignoid":
                self._game.image_tools.confirm_location("trial_battles")
            elif step == "close":
                self._game.wait(2)
                self._game.image_tools.confirm_location("trial_battles_description")

            image_location = self._game.image_tools.find_button(step)
            if step == "choose_a_summon":
                self._game.mouse_tools.move_and_click_point(image_location[0], image_location[1] + 187, step)
            else:
                self._game.mouse_tools.move_and_click_point(image_location[0], image_location[1], step)

        self._game.start_combat_mode(self._combat_script)

        self._is_bot_running.value = 1
        return None

    def test_combat_mode(self):
        """Tests almost all of the functionality of the bot via navigation and combat by starting the Very Hard difficulty Angel Halo Special Battle and completing it.

        Returns:
            None
        """
        self._game.print_and_save("\n################################################################################")
        self._game.print_and_save(f"{self._game.printtime()} [TEST] Testing Combat Mode on Very Hard Difficulty Angel Halo mission now...")
        self._game.print_and_save("################################################################################")

        self._game.start_farming_mode("dark", "Celeste Omega", 6, 1, "special", "Angel Halo", "EXP", 1, "VH Angel Halo")

        self._game.print_and_save(f"\n{self._game.printtime()} [TEST_SUCCESS] Testing Combat Mode was successful.")

        self._is_bot_running.value = 1
        return None
