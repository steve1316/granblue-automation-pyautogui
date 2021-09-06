import multiprocessing
import os
import unittest

from bot import game


class Test(unittest.TestCase):
    queue = multiprocessing.Queue()
    discord_queue = multiprocessing.Queue()
    is_bot_running = multiprocessing.Value("i", 0)

    def test_navigation1(self):
        print("Running test for navigation to Scattered Cargo.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.map_selection.select_map("Quest", "Port Breeze Archipelago", "Scattered Cargo", ""))

    def test_navigation2(self):
        print("Running test for navigation to The Dungeon Diet.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.map_selection.select_map("Quest", "Amalthea Island", "The Dungeon Diet", ""))

    def test_navigation3(self):
        print("Running test for navigation to I Challenge You!")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.map_selection.select_map("Quest", "Albion Citadel", "I Challenge You!", ""))

    def test_navigation4(self):
        print("Running test for navigation to VH Slimy Slime Search!")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.map_selection.select_map("Special", "Shiny Slime Search!", "VH Slimy Slime Search!", "Very Hard"))

    def test_navigation5(self):
        print("Running test for navigation to Lvl 120 Grimnir.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.map_selection.select_map("Raid", "", "Lvl 120 Grimnir", ""))

    def test_navigation6(self):
        print("Running test for navigation to Time of Revelation.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.map_selection.select_map("Coop", "", "Time of Revelation", ""))

    def test_item_detection1(self):
        print("Running test for item detection of Horseman's Plate.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.image_tools.confirm_location("loot_collected"))
        amount = game_object.image_tools.find_farmed_items("Horseman's Plate", take_screenshot = False)
        self.assertEqual(amount, 3)

    def test_item_detection2(self):
        print("Running test for item detection of Wind Orb.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.image_tools.confirm_location("loot_collected"))
        amount = game_object.image_tools.find_farmed_items("Wind Orb", take_screenshot = False)
        self.assertEqual(amount, 1)

    def test_item_detection3(self):
        print("Running test for item detection of Sagittarius Omega Anima.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.image_tools.confirm_location("loot_collected"))
        amount = game_object.image_tools.find_farmed_items("Sagittarius Omega Anima", take_screenshot = False)
        self.assertEqual(amount, 4)

    def test_item_detection4(self):
        print("Running test for item detection of Tiamat Malice Anima.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)
        self.assertTrue(game_object.image_tools.confirm_location("loot_collected"))
        amount = game_object.image_tools.find_farmed_items("Tiamat Malice Anima", take_screenshot = False)
        self.assertEqual(amount, 0)

    def test_avatar_detection(self):
        print("Running Twitter functionality by finding 5 Lvl 120 Avatar room codes.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)

        tweets = game_object.room_finder.find_most_recent("Lvl 120 Avatar", 5)
        print(f"Found tweets: {tweets}")

        self.assertGreaterEqual(len(tweets), 1)

    def test_combat_mode1(self):
        print("Running test for Combat Mode in Old Lignoid.")
        game_object = game.Game(self.queue, self.discord_queue, self.is_bot_running, test_mode = True)

        # Make sure the bot is at the Home screen and go to the Trial Battles screen.
        game_object.go_back_home(confirm_location_check = True)
        game_object.mouse_tools.scroll_screen_from_home_button(-600)
        game_object.find_and_click_button("gameplay_extras")

        while game_object.find_and_click_button("trial_battles") is False:
            game_object.mouse_tools.scroll_screen_from_home_button(-300)

        self.assertTrue(game_object.image_tools.confirm_location("trial_battles"))
        # Click on the "Old Lignoid" button.
        game_object.find_and_click_button("trial_battles_old_lignoid")

        # Select any detected "Play" button.
        game_object.find_and_click_button("play_round_button")

        # Now select the first Summon.
        choose_a_summon_location = game_object.image_tools.find_button("choose_a_summon")
        game_object.mouse_tools.move_and_click_point(choose_a_summon_location[0], choose_a_summon_location[1] + 187, "choose_a_summon")

        # Now start the Old Lignoid Trial Battle right away and then wait a few seconds.
        game_object.find_and_click_button("party_selection_ok")
        game_object.wait(3)

        if game_object.image_tools.confirm_location("trial_battles_description"):
            game_object.find_and_click_button("close")

        os.chdir("tests/")

        self.assertFalse(game_object.combat_mode.start_combat_mode(os.path.abspath("test_combat_mode.txt")))
        self.assertTrue(game_object.image_tools.confirm_location("home"))


if __name__ == "__main__":

    option: int = -1
    option_selected = ""

    while option != 0:
        check = False

        print("\n########################################")
        print("Unit and Integration Tests")
        print("\n1. Test navigation to \"Scattered Cargo\" on Port Breeze Archipelago")
        print("2. Test navigation to \"The Dungeon Diet\" on Amalthea Island")
        print("3. Test navigation to \"I Challenge You!\" on Albion Citadel")
        print("4. Test navigation to \"VH Slimy Slime Search!\" for Special Farming Mode")
        print("5. Test navigation to \"Lvl 120 Grimnir\" for Raid Farming Mode")
        print("6. Test navigation to \"Time of Revelation\" for Coop Farming Mode")
        print("7. Test item detection for \"Horseman's Plate\"")
        print("8. Test item detection for \"Wind Orb\"")
        print("9. Test item detection for \"Sagittarius Omega Anima\"")
        print("10. Test item detection for \"Tiamat Malice Anima\"")
        print("11. Test Twitter functionality searching for \"Lvl 120 Avatar\" room codes")
        print("12. Test Combat Mode functionality for \"Old Lignoid\"")
        print("\n0. Exit")
        print("\n########################################")

        option_selected = input("\nEnter the option number to begin that specific test: ")

        option: int = -1
        try:
            option: int = int(option_selected)
            check = True
        except ValueError:
            print("Invalid option entered. Please try again.")

        if option == 0:
            break

        if check:
            test = Test()

            try:
                if option == 1:
                    test.test_navigation1()
                elif option == 2:
                    test.test_navigation2()
                elif option == 3:
                    test.test_navigation3()
                elif option == 4:
                    test.test_navigation4()
                elif option == 5:
                    test.test_navigation5()
                elif option == 6:
                    test.test_navigation6()
                elif option == 7:
                    input("Please have the Quest Results screen visible for loot detection to work. Press any button to proceed...")
                    test.test_item_detection1()
                elif option == 8:
                    input("Please have the Quest Results screen visible for loot detection to work. Press any button to proceed...")
                    test.test_item_detection2()
                elif option == 9:
                    input("Please have the Quest Results screen visible for loot detection to work. Press any button to proceed...")
                    test.test_item_detection3()
                elif option == 10:
                    input("Please have the Quest Results screen visible for loot detection to work. Press any button to proceed...")
                    test.test_item_detection4()
                elif option == 11:
                    test.test_avatar_detection()
                elif option == 12:
                    test.test_combat_mode1()

                print("\nTest successfully completed.")
            except Exception as e:
                print(f"\nTest failed. Error message: {e}")
