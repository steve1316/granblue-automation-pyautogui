import multiprocessing
import os
import unittest

from bot.game import Game


class Test(unittest.TestCase):
    def __init__(self, bot: Game):
        super().__init__()
        self.game_object = bot

    def test_quest_navigation1(self):
        self.assertTrue(self.game_object.start_farming_mode())

    def test_special_navigation(self):
        self.assertTrue(self.game_object.start_farming_mode())

    def test_raid_navigation(self):
        self.assertTrue(self.game_object.start_farming_mode())

    def test_coop_navigation(self):
        self.assertTrue(self.game_object.start_farming_mode())

    def test_item_detection1(self):
        self.assertTrue(self.game_object.image_tools.confirm_location("loot_collected"))
        result = self.game_object.image_tools.find_farmed_items("Horseman's Plate", take_screenshot = False)
        self.assertEqual(result, 3)

    def test_item_detection2(self):
        self.assertTrue(self.game_object.image_tools.confirm_location("loot_collected"))
        result = self.game_object.image_tools.find_farmed_items("Wind Orb", take_screenshot = False)
        self.assertEqual(result, 1)

    def test_item_detection3(self):
        self.assertTrue(self.game_object.image_tools.confirm_location("loot_collected"))
        result = self.game_object.image_tools.find_farmed_items("Sagittarius Omega Anima", take_screenshot = False)
        self.assertEqual(result, 4)

    def test_twitter_functionality(self):
        self.game_object.wait(5)

        tries = 30
        room_codes = []
        while tries > 0:
            code = self.game_object.room_finder.get_room_code()
            if code != "":
                room_codes.append(code)
                if len(room_codes) >= 5:
                    break

            tries -= 1
            self.game_object.wait(1)

        self.game_object.room_finder.disconnect()
        print(f"\nFound room codes: {room_codes}")
        self.assertGreaterEqual(len(room_codes), 5)

    def test_combat_mode_old_lignoid(self):
        # Make sure the bot is at the Home screen and go to the Trial Battles screen.
        self.game_object.go_back_home(confirm_location_check = True)
        self.game_object.mouse_tools.scroll_screen_from_home_button(-600)
        self.game_object.find_and_click_button("gameplay_extras")

        while self.game_object.find_and_click_button("trial_battles") is False:
            self.game_object.mouse_tools.scroll_screen_from_home_button(-300)

        self.assertTrue(self.game_object.image_tools.confirm_location("trial_battles"))
        # Click on the "Old Lignoid" button.
        self.game_object.find_and_click_button("trial_battles_old_lignoid")

        # Select any detected "Play" button.
        self.game_object.find_and_click_button("play_round_button")

        # Now select the first Summon.
        choose_a_summon_location = self.game_object.image_tools.find_button("choose_a_summon")
        self.game_object.mouse_tools.move_and_click_point(choose_a_summon_location[0], choose_a_summon_location[1] + 187, "choose_a_summon")

        # Now start the Old Lignoid Trial Battle right away and then wait a few seconds.
        self.game_object.find_and_click_button("party_selection_ok")
        self.game_object.wait(3)

        if self.game_object.image_tools.confirm_location("trial_battles_description"):
            self.game_object.find_and_click_button("close")

        os.chdir("tests/")

        self.assertFalse(self.game_object.combat_mode.start_combat_mode(os.path.abspath("test_combat_mode.txt")))
        self.assertTrue(self.game_object.image_tools.confirm_location("home"))


if __name__ == "__main__":

    option: int = -1
    option_selected = ""

    while option != 0:
        check = False

        print("\n########################################")
        print("Unit and Integration Tests")
        print("\n1. Test \"The Fruit of Lumacie\" for Quest Farming Mode")
        print("2. Test \"VH Slimy Slime Search!\" for Special Farming Mode")
        print("3. Test \"Lvl 120 Grimnir\" for Raid Farming Mode")
        print("4. Test \"Time of Revelation\" for Coop Farming Mode")
        print("5. Test item detection for \"Horseman's Plate\"")
        print("6. Test item detection for \"Wind Orb\"")
        print("7. Test item detection for \"Sagittarius Omega Anima\"")
        print("8. Test Twitter functionality searching for \"Lvl 120 Avatar\" room codes")
        print("9. Test Combat Mode functionality for \"Old Lignoid\"")
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

        item_name = ""
        amount = 1
        mode = ""
        map_name = ""
        mission_name = ""
        summon_element_list = ["Fire"]
        summon_list = ["Colossus Omega"]
        group = 1
        party = 1
        combat_script = ""

        if check:
            if option == 1:
                item_name = "Rough Stone"
                mode = "Quest"
                map_name = "Lumacie Archipelago"
                mission_name = "The Fruit of Lumacie"
            elif option == 2:
                item_name = "EXP"
                mode = "Special"
                map_name = "Shiny Slime Search!"
                mission_name = "VH Shiny Slime Search!"
            elif option == 3:
                item_name = "Grimnir Anima"
                mode = "Raid"
                mission_name = "Lvl 120 Grimnir"
            elif option == 4:
                item_name = "Gladiator Distinction"
                mode = "Coop"
                mission_name = "Time of Revelation"
            elif option == 5:
                item_name = "Horseman's Plate"
            elif option == 6:
                item_name = "Wind Orb"
            elif option == 7:
                item_name = "Sagittarius Omega Anima"
            elif option == 8:
                mission_name = "Lvl 120 Avatar"

            try:
                game = Game(queue = multiprocessing.Queue(), discord_queue = multiprocessing.Queue(), is_bot_running = multiprocessing.Value("i", 0), item_name = item_name,
                            item_amount_to_farm = amount,
                            farming_mode = mode, map_name = map_name, mission_name = mission_name, summon_element_list = summon_element_list, summon_list = summon_list, group_number = group,
                            party_number = party, combat_script = combat_script)
                test = Test(game)

                if option == 1:
                    test.test_quest_navigation1()
                elif option == 2:
                    test.test_special_navigation()
                elif option == 3:
                    test.test_raid_navigation()
                elif option == 4:
                    test.test_coop_navigation()
                elif option == 5:
                    input("Please have the Quest Results screen visible for loot detection to work. Press any button to proceed...")
                    test.test_item_detection1()
                elif option == 6:
                    input("Please have the Quest Results screen visible for loot detection to work. Press any button to proceed...")
                    test.test_item_detection2()
                elif option == 7:
                    input("Please have the Quest Results screen visible for loot detection to work. Press any button to proceed...")
                    test.test_item_detection3()
                elif option == 8:
                    test.test_twitter_functionality()
                elif option == 9:
                    test.test_combat_mode_old_lignoid()

                print("\nTest successfully completed.")
            except Exception as e:
                print(f"\nTest failed. Error message: {e}")
