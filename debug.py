from game import Game
import pyautogui


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

    def test_combat_mode(self):
        """Tests almost all of the bot's functionality by starting the Normal difficulty Angel Halo Special Battle and completing it. This assumes that Angel Halo is at the very bottom of the Special missions list.

        Returns:
            None
        """
        print("\n############################################################")
        print(
            "[TEST] Testing Combat Mode on Normal Difficulty Angel Halo mission now...")
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

            list_of_select_button_locations = self.game.image_tools.find_all("select", custom_region=(
                self.game.image_tools.window_left, self.game.image_tools.window_top, self.game.image_tools.window_width, self.game.image_tools.window_height))

            print("\n############################################################")
            print("[TEST] Now selecting and moving to Normal Difficulty Angel Halo...")
            print("############################################################")
            # Bring up the Difficulty Screen for Angel Halo.
            angel_halo_mission = pyautogui.center(
                list_of_select_button_locations.pop())
            self.game.mouse_tools.move_and_click_point(
                angel_halo_mission[0], angel_halo_mission[1])

            self.game.wait_for_ping(1)
            self.game.image_tools.confirm_location("angelHalo")

            # Select the center of the first "Play" Button which would be the Normal Difficulty Angel Halo mission.
            list_of_special_play_button_locations = self.game.image_tools.find_all("specialPlay", custom_region=(
                self.game.image_tools.window_left, self.game.image_tools.window_top, self.game.image_tools.window_width, self.game.image_tools.window_height))
            normal_difficulty_mission = pyautogui.center(list_of_special_play_button_locations.pop(
                0))

            # Then click the mission and confirm the location for the Summon Selection Screen.
            self.game.mouse_tools.move_and_click_point(
                normal_difficulty_mission[0], normal_difficulty_mission[1])
            self.game.image_tools.confirm_location("selectSummon")

            # Locate Dark summons and click on the specified Summon.
            print("\n############################################################")
            print("[TEST] Selecting the first found FLB Hades Summon...")
            print("############################################################")
            self.game.find_summon_element("dark")
            summon_check = self.game.find_summon("hadesFLB")
            if (summon_check == False):
                tries -= 1
                if (tries <= 0):
                    sys.exit(
                        "[ERROR] Could not find summon after multiple refreshes. Exiting application...")

        # Select first Group, second Party.
        print("\n############################################################")
        print("[TEST] Selecting First Group, Second Party...")
        print("############################################################")
        self.game.find_party_and_start_mission(1, 2)

        # Start the Combat Mode.
        self.game.start_combat_mode("test_combat_mode")

        return None
