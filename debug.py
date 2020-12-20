import sys

import pyautogui
from guibot.fileresolver import FileResolver
from guibot.guibot import GuiBot

from game import Game


class Debug:
    """
    Test driver for most bot functionality.

    Attributes
    ----------
    my_game (Game): The Game object to test with.

    """

    def __init__(self, my_game: Game):
        super().__init__()

        self.game = my_game

    def test_find_summon_element_tabs(self):
        """Tests finding each summon element tab on the Summon Selection Screen by navigating to the Fire Old Lignoid trial battle.

        Returns:
            None
        """
        print("\n############################################################")
        print(
            "[TEST] Testing finding all summon element tabs on the Summon Selection screen...")
        print("############################################################")

        # Head to the Trial Battles and use GuiBot to navigate to the Fire Old Lignoid prep screen.
        self.guibot = GuiBot()
        self.fileresolver = FileResolver()
        self.fileresolver.add_path("images/buttons/")

        self.game.go_back_home()
        self.game.mouse_tools.move_and_click_point(
            self.game.home_button_location[0], self.game.home_button_location[1] - 50, mouse_clicks=0)
        self.game.mouse_tools.scroll_screen(
            self.game.home_button_location[0], self.game.home_button_location[1] - 50, -400)

        self.guibot.click("gameplay_extras").idle(1)
        self.guibot.click("trial_battles").idle(2)
        self.guibot.click("trial_battles_old_lignoid").idle(1)
        self.guibot.click("trial_battles_play").idle(2)

        if(self.game.image_tools.confirm_location("select_summon")):
            if(self.game.find_summon_element("fire") and self.game.find_summon_element("water") and self.game.find_summon_element("earth") and self.game.find_summon_element("wind") and self.game.find_summon_element("light") and self.game.find_summon_element("dark") and self.game.find_summon_element("misc")):
                print(
                    "\n[TEST_SUCCESS] Finding all summon element tabs was successful.")
            else:
                print(
                    "\n[TEST_ERROR] Failed to find one or more summon element tabs.")
        else:
            print("\n[TEST_ERROR] Bot is not at the Summon Selection Screen.")

    def test_combat_mode(self):
        """Tests almost all of the bot's functionality by starting the Very Hard difficulty Angel Halo Special Battle and completing it. This assumes that Angel Halo is at the very bottom of the Special missions list.

        Returns:
            None
        """
        print("\n############################################################")
        print(
            "[TEST] Testing Combat Mode on Very Hard Difficulty Angel Halo mission now...")
        print("############################################################")

        summon_check = False
        tries = 2
        while(summon_check == False):
            # First go to the Home Screen and calibrate the dimensions of the game window. Then navigation will be as follows: Home Screen -> Quest Screen -> Special Screen.
            self.game.go_back_home(confirm_location_check=True,
                                   display_info_check=True)

            list_of_button_names = ["quest", "special"]

            for button_name in list_of_button_names:
                x, y = self.game.image_tools.find_button(button_name)
                self.game.mouse_tools.move_and_click_point(x, y)

            # Attempt to fit all the "Select" buttons into the current view and then find all "Select" Buttons.
            print("\n############################################################")
            print("[TEST] Finding all Special Select Buttons...")
            print("############################################################")
            self.game.image_tools.confirm_location("special")

            self.game.mouse_tools.scroll_screen(
                self.game.home_button_location[0], self.game.home_button_location[1] - 50, -300)

            self.game.wait_for_ping(1)

            special_quests = self.game.image_tools.find_all("select", custom_region=(
                self.game.image_tools.window_left, self.game.image_tools.window_top, self.game.image_tools.window_width, self.game.image_tools.window_height))

            print("\n############################################################")
            print(
                "[TEST] Now selecting and moving to Very Hard Difficulty Angel Halo...")
            print("############################################################")
            # Bring up the Difficulty Screen for Angel Halo.
            angel_halo_special_quest = pyautogui.center(
                special_quests.pop())

            self.game.mouse_tools.move_and_click_point(
                angel_halo_special_quest[0], angel_halo_special_quest[1])

            self.game.wait_for_ping(1)
            self.game.image_tools.confirm_location("angel_halo")

            # Select the center of the last "Play" Button which would be the Very Hard Difficulty Angel Halo mission.
            list_of_special_play_button_locations = self.game.image_tools.find_all("special_play", custom_region=(
                self.game.image_tools.window_left, self.game.image_tools.window_top, self.game.image_tools.window_width, self.game.image_tools.window_height))

            angel_halo_VH = pyautogui.center(
                list_of_special_play_button_locations.pop())

            # Then click the mission and confirm the location for the Summon Selection Screen.
            self.game.mouse_tools.move_and_click_point(
                angel_halo_VH[0], angel_halo_VH[1])

            self.game.image_tools.confirm_location("select_summon")

            # Locate Dark summons and click on the specified Summon.
            print("\n############################################################")
            print("[TEST] Selecting the first found FLB Hades Summon...")
            print("############################################################")
            self.game.find_summon_element("dark")
            summon_check = self.game.find_summon("hades_flb")

            if (summon_check == False):
                tries -= 1
                if (tries <= 0):
                    sys.exit(
                        "[TEST_ERROR] Could not find summon after multiple refreshes. Exiting application...")

        # Select first Group, second Party.
        print("\n############################################################")
        print("[TEST] Selecting First Group, Second Party...")
        print("############################################################")
        self.game.find_party_and_start_mission(1, 2)

        # Start the Combat Mode.
        self.game.start_combat_mode("test_combat_mode")

        print("\n[TEST_SUCCESS] Finding all summon element tabs was successful.")

        return None
