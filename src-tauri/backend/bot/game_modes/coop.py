from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class CoopException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Coop:
    """
    Provides the navigation and any necessary utility functions to handle the Coop game mode.
    """

    # The 2nd element of the list of EX1 missions is designated "empty" because it is used to navigate properly to "Lost in the Dark" from "Corridor of Puzzles".
    _coop_ex1_list = ["EX1-1 Corridor of Puzzles", "empty", "EX1-3 Lost in the Dark"]
    _coop_ex2_list = ["EX2-2 Time of Judgement", "EX2-3 Time of Revelation", "EX2-4 Time of Eminence"]
    _coop_ex3_list = ["EX3-2 Rule of the Tundra", "EX3-3 Rule of the Plains", "EX3-4 Rule of the Twilight"]
    _coop_ex4_list = ["EX4-2 Amidst the Waves", "EX4-3 Amidst the Petals", "EX4-4 Amidst Severe Cliffs", "EX4-5 Amidst the Flames"]
    _coop_ex5_list = ["EX5-1 Throes of Sorcery", "EX5-2 Throes of Spears", "EX5-3 Throes of Wings", "EX5-4 Throes of Calamity"]
    _coop_ex_final_list = ["EX6-1 Throes of Dark Steel", "EX6-2 Throes of Death"]

    @staticmethod
    def _navigate():
        """Navigates to the specified Coop mission.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[COOP] Beginning process to navigate to the mission: {Settings.mission_name}...")

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        # Click the "Menu" button on the Home screen and then go to the Coop screen.
        Game.find_and_click_button("home_menu")
        Game.wait(1.0)
        Game.find_and_click_button("coop")

        if ImageUtils.confirm_location("coop"):
            # Scroll down the screen to see more of the Coop missions on smaller screens.
            MouseUtils.scroll_screen_from_home_button(-400)

            # Select the difficulty of the mission that it is under.
            if Settings.mission_name == "H3-1 In a Dusk Dream":
                # Check if Hard difficulty is already selected. If not, make it active.
                if ImageUtils.find_button("coop_hard_selected") is None:
                    Game.find_and_click_button("coop_hard")

                MessageLog.print_message(f"\n[COOP] Hard difficulty for Coop is now selected.")

                # Find the locations of all of the "Host Quest" buttons.
                host_quest_button_locations = ImageUtils.find_all("coop_host_quest")

                # Select the category, "Save the Oceans", which should be the 3rd category.
                MessageLog.print_message(f"[COOP] Now navigating to \"{Settings.mission_name}\" for Hard difficulty.")
                MouseUtils.move_and_click_point(host_quest_button_locations[2][0], host_quest_button_locations[2][1], "coop_host_quest")

                if ImageUtils.confirm_location("coop_save_the_oceans"):
                    # Now click "In a Dusk Dream".
                    host_quests_circle_buttons = ImageUtils.find_all("coop_host_quest_circle")
                    MouseUtils.move_and_click_point(host_quests_circle_buttons[0][0], host_quests_circle_buttons[0][1], "coop_host_quest")

            else:
                # Check if Extra difficulty is already selected. If not, make it active.
                if ImageUtils.find_button("coop_extra_selected") is None:
                    Game.find_and_click_button("coop_extra")

                MessageLog.print_message(f"\n[COOP] Extra difficulty for Coop is now selected.")

                # Find the locations of all of the "Host Quest" buttons.
                host_quest_button_locations = ImageUtils.find_all("coop_host_quest")

                # Make the specified EX category active. Then click the mission's button while making sure that the first mission in each category is skipped.
                if Settings.mission_name in Coop._coop_ex1_list:
                    MessageLog.print_message(f"\n[COOP] Now navigating to \"{Settings.mission_name}\" from EX1...")
                    MouseUtils.move_and_click_point(host_quest_button_locations[0][0], host_quest_button_locations[0][1], "coop_host_quest")

                    if ImageUtils.confirm_location("coop_ex1"):
                        MessageLog.print_message(f"\n[COOP] Now selecting Coop mission: \"{Settings.mission_name}\"")
                        coop_host_locations = ImageUtils.find_all("coop_host_quest_circle")
                        MouseUtils.move_and_click_point(coop_host_locations[Coop._coop_ex1_list.index(Settings.mission_name)][0],
                                                        coop_host_locations[Coop._coop_ex1_list.index(Settings.mission_name)][1],
                                                        "coop_host_quest")

                elif Settings.mission_name in Coop._coop_ex2_list:
                    MessageLog.print_message(f"\n[COOP] Now navigating to \"{Settings.mission_name}\" from EX2...")
                    MouseUtils.move_and_click_point(host_quest_button_locations[1][0], host_quest_button_locations[1][1], "coop_host_quest")

                    if ImageUtils.confirm_location("coop_ex2"):
                        MessageLog.print_message(f"\n[COOP] Now selecting Coop mission: \"{Settings.mission_name}\"")
                        coop_host_locations = ImageUtils.find_all("coop_host_quest_circle")
                        MouseUtils.move_and_click_point(coop_host_locations[Coop._coop_ex2_list.index(Settings.mission_name) + 1][0],
                                                        coop_host_locations[Coop._coop_ex2_list.index(Settings.mission_name) + 1][1],
                                                        "coop_host_quest")

                elif Settings.mission_name in Coop._coop_ex3_list:
                    MessageLog.print_message(f"\n[COOP] Now navigating to \"{Settings.mission_name}\" from EX3.")
                    MouseUtils.move_and_click_point(host_quest_button_locations[2][0], host_quest_button_locations[2][1], "coop_host_quest")

                    if ImageUtils.confirm_location("coop_ex3"):
                        MessageLog.print_message(f"\n[COOP] Now selecting Coop mission: \"{Settings.mission_name}\"")
                        coop_host_locations = ImageUtils.find_all("coop_host_quest_circle")
                        MouseUtils.move_and_click_point(coop_host_locations[Coop._coop_ex3_list.index(Settings.mission_name) + 1][0],
                                                        coop_host_locations[Coop._coop_ex3_list.index(Settings.mission_name) + 1][1],
                                                        "coop_host_quest")

                elif Settings.mission_name in Coop._coop_ex4_list:
                    MessageLog.print_message(f"\n[COOP] Now navigating to \"{Settings.mission_name}\" from EX4.")
                    MouseUtils.move_and_click_point(host_quest_button_locations[3][0], host_quest_button_locations[3][1], "coop_host_quest")

                    if ImageUtils.confirm_location("coop_ex4"):
                        MessageLog.print_message(f"\n[COOP] Now selecting Coop mission: \"{Settings.mission_name}\"")
                        coop_host_locations = ImageUtils.find_all("coop_host_quest_circle")
                        MouseUtils.move_and_click_point(coop_host_locations[Coop._coop_ex4_list.index(Settings.mission_name) + 1][0],
                                                        coop_host_locations[Coop._coop_ex4_list.index(Settings.mission_name) + 1][1],
                                                        "coop_host_quest")

                elif Settings.mission_name in Coop._coop_ex5_list:
                    MessageLog.print_message(f"\n[COOP] Now navigating to \"{Settings.mission_name}\" from EX5.")
                    MouseUtils.move_and_click_point(host_quest_button_locations[4][0], host_quest_button_locations[4][1], "coop_host_quest")

                    if ImageUtils.confirm_location("coop_ex5"):
                        MessageLog.print_message(f"\n[COOP] Now selecting Coop mission: \"{Settings.mission_name}\"")
                        coop_host_locations = ImageUtils.find_all("coop_host_quest_circle")
                        MouseUtils.move_and_click_point(coop_host_locations[Coop._coop_ex5_list.index(Settings.mission_name)][0],
                                                        coop_host_locations[Coop._coop_ex5_list.index(Settings.mission_name)][1],
                                                        "coop_host_quest")

                elif Settings.mission_name in Coop._coop_ex_final_list:
                    MessageLog.print_message(f"\n[COOP] Now navigating to \"{Settings.mission_name}\" from EX Final Tier.")
                    MouseUtils.move_and_click_point(host_quest_button_locations[5][0], host_quest_button_locations[5][1], "coop_host_quest")

                    if ImageUtils.confirm_location("coop_ex_final"):
                        MessageLog.print_message(f"\n[COOP] Now selecting Coop mission: \"{Settings.mission_name}\"")
                        coop_host_locations = ImageUtils.find_all("coop_host_quest_circle")
                        MouseUtils.move_and_click_point(coop_host_locations[Coop._coop_ex_final_list.index(Settings.mission_name)][0],
                                                        coop_host_locations[Coop._coop_ex_final_list.index(Settings.mission_name)][1],
                                                        "coop_host_quest")

            # After clicking on the Coop mission, create a new Room.
            MessageLog.print_message(f"\n[COOP] Opening up a new Coop room...")
            Game.find_and_click_button("coop_post_to_crew_chat")

            # Scroll down the screen to see the "OK" button just in case of smaller screens.
            MouseUtils.scroll_screen_from_home_button(-400)
            Game.find_and_click_button("ok")

            Game.wait(3.0)

            # Just in case, check for the "You retreated from the raid battle" popup.
            if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
                Game.find_and_click_button("ok")

            MessageLog.print_message(f"\n[COOP] Selecting a Party for Coop mission: \"{Settings.mission_name}\".")
            Game.find_and_click_button("coop_select_party")
        else:
            raise CoopException("Failed to arrive at Coop page.")

        return None

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Coop Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            Coop._navigate()
        else:
            MessageLog.print_message("\n[COOP] Starting Coop Mission again.")

            # Head back to the Coop Room.
            Game.find_and_click_button("coop_room")
            Game.wait(1.0)

            # Check for "Daily Missions" popup for Coop.
            if ImageUtils.confirm_location("coop_daily_missions"):
                Game.find_and_click_button("close")

            Game.wait(2.0)

            # Now that the bot is back at the Coop Room/Lobby, check if it closed due to time running out.
            if ImageUtils.confirm_location("coop_room_closed"):
                MessageLog.print_message("\n[COOP] Coop room has closed due to time running out.")
                return None

            # Start the Coop Mission again.
            Game.find_and_click_button("coop_start")
            Game.wait(3.0)

        # Check for AP.
        Game.check_for_ap()

        # Check if the bot is at the Party Selection screen. Note that the bot is hosting solo so no support summon selection.
        if first_run and ImageUtils.confirm_location("coop_without_support_summon", tries = 30):
            # Select the Party.
            Game.find_party_and_start_mission(Settings.group_number, Settings.party_number)

            # Now click the "Start" button to start the Coop Mission.
            Game.find_and_click_button("coop_start")
            Game.wait(3.0)

            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)
        elif first_run is False:
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)
        else:
            raise CoopException("Failed to arrive at the Summon Selection screen.")

        return None
