import multiprocessing
import os
import signal
import sys
import unittest

from utils.settings import Settings
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode
from bot.game import Game
from utils.twitter_room_finder import TwitterRoomFinder
from utils import discord_utils


class Test(unittest.TestCase):
    def __init__(self, bot: Game):
        super().__init__()
        self.game_object = bot

        self.old_settings = {
            "item_name": Settings.item_name,
            "farming_mode": Settings.farming_mode,
            "map_name": Settings.map_name,
            "mission_name": Settings.mission_name,
            "item_amount": Settings.item_amount_to_farm
        }

    def _reset_settings(self):
        Settings.item_name = self.old_settings["item_name"]
        Settings.farming_mode = self.old_settings["farming_mode"]
        Settings.map_name = self.old_settings["map_name"]
        Settings.mission_name = self.old_settings["mission_name"]
        Settings.item_amount_to_farm = self.old_settings["item_amount"]

    def test_quest(self):
        Settings.item_name = "Rough Stone"
        Settings.farming_mode = "Quest"
        Settings.map_name = "Lumacie Archipelago"
        Settings.mission_name = "The Fruit of Lumacie"
        Settings.item_amount_to_farm = 1

        self.assertTrue(self.game_object.start_farming_mode())
        self._reset_settings()
        return None

    def test_special(self):
        Settings.item_name = "EXP"
        Settings.farming_mode = "Special"
        Settings.map_name = "Shiny Slime Search!"
        Settings.mission_name = "VH Slimy Slime Search!"
        Settings.item_amount_to_farm = 1

        self.assertTrue(self.game_object.start_farming_mode())
        self._reset_settings()
        return None

    def test_raid(self):
        Settings.item_name = "Grimnir Anima"
        Settings.farming_mode = "Raid"
        Settings.mission_name = "Lvl 120 Grimnir"
        Settings.item_amount_to_farm = 1

        self.assertTrue(self.game_object.start_farming_mode())
        self._reset_settings()
        return None

    def test_coop(self):
        Settings.item_name = "Grimnir Anima"
        Settings.farming_mode = "Raid"
        Settings.mission_name = "Lvl 120 Grimnir"
        Settings.item_amount_to_farm = 1

        self.assertTrue(self.game_object.start_farming_mode())
        self._reset_settings()
        return None

    def test_item_detection1(self):
        self.assertTrue(ImageUtils.confirm_location("loot_collected"))
        result = ImageUtils.find_farmed_items("Horseman's Plate", take_screenshot = False)
        self.assertEqual(result, 3)
        return None

    def test_item_detection2(self):
        self.assertTrue(ImageUtils.confirm_location("loot_collected"))
        result = ImageUtils.find_farmed_items("Wind Orb", take_screenshot = False)
        self.assertEqual(result, 1)
        return None

    def test_item_detection3(self):
        self.assertTrue(ImageUtils.confirm_location("loot_collected"))
        result = ImageUtils.find_farmed_items("Sagittarius Omega Anima", take_screenshot = False)
        self.assertEqual(result, 4)
        return None

    def test_twitter_functionality(self):
        Settings.farming_mode = "Raid"
        Settings.mission_name = "Lvl 120 Avatar"

        TwitterRoomFinder.connect()

        Game.wait(5)

        tries = 10
        room_codes = []
        while tries > 0:
            code = TwitterRoomFinder.get_room_code()
            if code != "":
                room_codes.append(code)
                if len(room_codes) >= 1:
                    break

            tries -= 1
            Game.wait(1)

        TwitterRoomFinder.disconnect()
        print(f"\nFound room codes: {room_codes}")
        self.assertGreaterEqual(len(room_codes), 1)
        self._reset_settings()
        return None

    def test_twitter_connection(self):
        result: bool = TwitterRoomFinder.test_connection()
        Game.wait(5)
        self.assertTrue(result)
        TwitterRoomFinder.disconnect()
        return None

    def test_discord_connection(self):
        print("\n[DISCORD] Starting Discord process on a new Thread...")
        discord_queue = multiprocessing.Queue()
        test_queue = multiprocessing.Queue()
        self._discord_process = multiprocessing.Process(target = discord_utils.start_now, args = (Settings.discord_token, Settings.user_id, discord_queue, test_queue))
        self._discord_process.start()
        Game.wait(8.0)
        discord_queue.put("Testing 1 2 3")

        while not test_queue.empty():
            message: str = test_queue.get(block = True, timeout = 10)
            if message.__contains__("Successful connection."):
                break
            elif message.__contains__("Failed to find user using provided user ID."):
                self._discord_process.terminate()
                raise Exception("Failed to find user using provided user ID.")
            elif message.__contains__("Failed to connect to Discord API using provided token."):
                self._discord_process.terminate()
                raise Exception("Failed to connect to Discord API using provided token.")
            else:
                print("Test queue received: " + message)

        discord_queue.put(f"```diff\n- Terminated connection to Discord API for Granblue Automation\n```")

        Game.wait(1.0)

        os.kill(self._discord_process.pid, signal.Signals.SIGTERM)

        Game.wait(3.0)

        self.assertTrue(discord_queue.empty())
        return None

    def test_combat_mode_old_lignoid(self):
        # Make sure the bot is at the Home screen and go to the Trial Battles screen.
        self.game_object.go_back_home(confirm_location_check = True)
        MouseUtils.scroll_screen_from_home_button(-600)
        self.game_object.find_and_click_button("gameplay_extras")

        while self.game_object.find_and_click_button("trial_battles") is False:
            MouseUtils.scroll_screen_from_home_button(-300)

        self.assertTrue(ImageUtils.confirm_location("trial_battles"))
        # Click on the "Old Lignoid" button.
        self.game_object.find_and_click_button("trial_battles_old_lignoid")

        # Select any detected "Play" button.
        self.game_object.find_and_click_button("play_round_button")

        # Now select the first Summon.
        choose_a_summon_location = ImageUtils.find_button("choose_a_summon")
        MouseUtils.move_and_click_point(choose_a_summon_location[0], choose_a_summon_location[1] + 187, "choose_a_summon")

        # Now start the Old Lignoid Trial Battle right away and then wait a few seconds.
        self.game_object.find_and_click_button("party_selection_ok")
        Game.wait(3)

        if ImageUtils.confirm_location("trial_battles_description"):
            self.game_object.find_and_click_button("close")

        self.assertFalse(CombatMode.start_combat_mode(script_commands = ["Turn 1:",
                                                                         "\tsummon(6)",
                                                                         "\tcharacter1.useSkill(1)",
                                                                         "end",
                                                                         "",
                                                                         "Turn 5:",
                                                                         "\texit",
                                                                         "end"]))
        self.assertTrue(ImageUtils.confirm_location("home"))
        return None


if __name__ == "__main__":

    try:
        if len(sys.argv[1]) != "":
            arg: str = sys.argv[1]

            option: int = -1
            try:
                option: int = int(arg)
            except ValueError:
                print("Invalid argument passed in for a option number.", flush = True)

            if option not in range(1, 11):
                raise (ValueError("Argument passed in was for a option number that does not exist."))

            try:
                game = Game()
                test = Test(game)

                if option == 1:
                    test.test_quest()
                elif option == 2:
                    test.test_special()
                elif option == 3:
                    test.test_raid()
                elif option == 4:
                    test.test_coop()
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
                    test.test_twitter_connection()
                elif option == 10:
                    test.test_discord_connection()
                elif option == 11:
                    test.test_combat_mode_old_lignoid()

                print("\nTest successfully completed.")
            except Exception as e:
                print(f"\nTest failed. Error message: {e}")
            finally:
                sys.exit(0)
    except IndexError:
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
            print("9. Test Twitter Connection using saved API keys and tokens.")
            print("10. Test Discord functionality using saved API key.")
            print("11. Test Combat Mode functionality for \"Old Lignoid\"")
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
                sys.exit(0)

            if check:
                try:
                    game = Game()
                    test = Test(game)

                    if option == 1:
                        test.test_quest()
                    elif option == 2:
                        test.test_special()
                    elif option == 3:
                        test.test_raid()
                    elif option == 4:
                        test.test_coop()
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
                        test.test_twitter_connection()
                    elif option == 10:
                        test.test_discord_connection()
                    elif option == 11:
                        test.test_combat_mode_old_lignoid()

                    print("\nTest successfully completed.")
                except Exception as e:
                    print(f"\nTest failed. Error message: {e}")
