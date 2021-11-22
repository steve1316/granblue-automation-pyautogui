from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class QuestException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Quest:
    """
    Provides the navigation and any necessary utility functions to handle the Quest game mode.
    """

    _page_1_list = ["Zinkenstill", "Port Breeze Archipelago", "Valtz Duchy", "Auguste Isles", "Lumacie Archipelago", "Albion Citadel"]
    _page_2_list = ["Mist-Shrouded Isle", "Golonzo Island", "Amalthea Island", "Former Capital Mephorash", "Agastia"]

    @staticmethod
    def _navigate_to_map(map_name: str, current_location: str) -> bool:
        """Navigates the bot to the specified Map for Quest Farming Mode.

        Args:
            map_name (str): Name of the Map to navigate to.
            current_location (str): Name of the Map that the bot is currently at.

        Returns:
            (bool): Return True if the bot reached the Summon Selection screen. Otherwise, return False.
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[QUEST] Beginning process to navigate to the island: {map_name}...")

        # Phantagrande Skydom Page 1
        if Quest._page_1_list.__contains__(map_name):
            # Switch pages if needed.
            if Quest._page_2_list.__contains__(current_location):
                Game.find_and_click_button("world_left_arrow")

            # Click on the Map to move to it.
            if not Game.find_and_click_button(map_name.lower().replace(" ", "_").replace("-", "_")):
                # If the name of the island is obscured, like by the "Next" text indicating that the user's next quest is there, fallback to a manual method.
                arrow_location = ImageUtils.find_button("world_right_arrow")

                if map_name == "Port Breeze Archipelago":
                    MouseUtils.move_and_click_point(arrow_location[0] - 320, arrow_location[1] - 159, "world_right_arrow")
                elif map_name == "Valtz Duchy":
                    MouseUtils.move_and_click_point(arrow_location[0] - 150, arrow_location[1] - 85, "world_right_arrow")
                elif map_name == "Auguste Isles":
                    MouseUtils.move_and_click_point(arrow_location[0] - 374, arrow_location[1] - 5, "world_right_arrow")
                elif map_name == "Lumacie Archipelago":
                    MouseUtils.move_and_click_point(arrow_location[0] - 84, arrow_location[1] + 39, "world_right_arrow")
                elif map_name == "Albion Citadel":
                    MouseUtils.move_and_click_point(arrow_location[0] - 267, arrow_location[1] + 121, "world_right_arrow")

            return True

        # Phantagrande Skydom Page 2
        elif Quest._page_2_list.__contains__(map_name):
            if Quest._page_1_list.__contains__(current_location):
                Game.find_and_click_button("world_right_arrow")

            if not Game.find_and_click_button(map_name.lower().replace(" ", "_").replace("-", "_")):
                arrow_location = ImageUtils.find_button("world_left_arrow")

                if map_name == "Mist-Shrouded Isle":
                    MouseUtils.move_and_click_point(arrow_location[0] + 162, arrow_location[1] + 114, "world_left_arrow")
                elif map_name == "Golonzo Island":
                    MouseUtils.move_and_click_point(arrow_location[0] + 362, arrow_location[1] + 85, "world_left_arrow")
                elif map_name == "Amalthea Island":
                    MouseUtils.move_and_click_point(arrow_location[0] + 127, arrow_location[1] - 14, "world_left_arrow")
                elif map_name == "Former Capital Mephorash":
                    MouseUtils.move_and_click_point(arrow_location[0] + 352, arrow_location[1] - 51, "world_left_arrow")
                elif map_name == "Agastia":
                    MouseUtils.move_and_click_point(arrow_location[0] + 190, arrow_location[1] - 148, "world_left_arrow")

            return True

        return False

    @staticmethod
    def _navigate():
        """Navigates to the specified Quest mission.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[QUEST] Beginning process to navigate to the mission: {Settings.mission_name}...")

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        current_location = ""
        formatted_map_name = Settings.map_name.lower().replace(" ", "_").replace("-", "_")

        # Check which island the bot is at.
        if ImageUtils.confirm_location(f"map_{formatted_map_name}", tries = 3):
            MessageLog.print_message(f"[QUEST] Bot is currently on the correct island.")
            check_location = True
        else:
            MessageLog.print_message(f"[QUEST] Bot is currently not on the correct island.")
            check_location = False

            location_list = ["Zinkenstill", "Port Breeze Archipelago", "Valtz Duchy", "Auguste Isles", "Lumacie Archipelago", "Albion Citadel",
                             "Mist-Shrouded Isle", "Golonzo Island", "Amalthea Island", "Former Capital Mephorash", "Agastia"]

            while len(location_list) > 0:
                temp_map_location = location_list.pop(0)
                temp_formatted_map_location = temp_map_location.lower().replace(" ", "_").replace("-", "_")

                if ImageUtils.confirm_location(f"map_{temp_formatted_map_location}", tries = 1):
                    MessageLog.print_message(f"[QUEST] Bot's current location is at {temp_map_location}. Now moving to {Settings.map_name}...")
                    current_location = temp_map_location
                    break

        # Once the bot has determined where it is, go to the Quest screen.
        Game.find_and_click_button("quest")

        Game.wait(1)

        # Check for the "You retreated from the raid battle" popup.
        if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
            Game.find_and_click_button("ok")

        if ImageUtils.confirm_location("quest"):
            # If the bot is currently not at the correct island, move to it.
            if not check_location:
                # Click the "World" button.
                Game.find_and_click_button("world")

                # On the World screen, click the specified coordinates on the window to move to the island. If the island is on a different world page, switch pages as necessary.
                Quest._navigate_to_map(Settings.map_name, current_location)

                # Click "Go" on the popup after clicking on the map node.
                Game.find_and_click_button("go")

            # Grab the location of the "World" button.
            world_location = ImageUtils.find_button("world", tries = 5)
            if world_location is None:
                world_location = ImageUtils.find_button("world2", tries = 5)

            # Now that the bot is on the correct island and is at the Quest screen, click the correct chapter node.
            if Settings.mission_name == "Scattered Cargo":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 1 (115) node at ({world_location[0] + 97}, {world_location[1] + 97})...")
                MouseUtils.move_and_click_point(world_location[0] + 97, world_location[1] + 97, "template_node")
            elif Settings.mission_name == "Lucky Charm Hunt":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 6 (122) node...")
                MouseUtils.move_and_click_point(world_location[0] + 332, world_location[1] + 16, "template_node")
            elif Settings.mission_name == "Special Op's Request":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 8 node...")
                MouseUtils.move_and_click_point(world_location[0] + 258, world_location[1] + 151, "template_node")
            elif Settings.mission_name == "Threat to the Fisheries":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 9 node...")
                MouseUtils.move_and_click_point(world_location[0] + 216, world_location[1] + 113, "template_node")
            elif Settings.mission_name == "The Fruit of Lumacie" or Settings.mission_name == "Whiff of Danger":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 13 (39/52) node...")
                MouseUtils.move_and_click_point(world_location[0] + 78, world_location[1] + 92, "template_node")
            elif Settings.mission_name == "I Challenge You!":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 17 node...")
                MouseUtils.move_and_click_point(world_location[0] + 119, world_location[1] + 121, "template_node")
            elif Settings.mission_name == "For Whom the Bell Tolls":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 22 node...")
                MouseUtils.move_and_click_point(world_location[0] + 178, world_location[1] + 33, "template_node")
            elif Settings.mission_name == "Golonzo's Battles of Old":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 25 node...")
                MouseUtils.move_and_click_point(world_location[0] + 196, world_location[1] + 5, "template_node")
            elif Settings.mission_name == "The Dungeon Diet":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 30 (44/65) node...")
                MouseUtils.move_and_click_point(world_location[0] + 242, world_location[1] + 24, "template_node")
            elif Settings.mission_name == "Trust Busting Dustup":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 36 (123) node...")
                MouseUtils.move_and_click_point(world_location[0] + 319, world_location[1] + 13, "template_node")
            elif Settings.mission_name == "Erste Kingdom Episode 4":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 70 node...")
                MouseUtils.move_and_click_point(world_location[0] + 253, world_location[1] + 136, "template_node")
            elif Settings.mission_name == "Imperial Wanderer's Soul":
                MessageLog.print_message(f"\n[QUEST] Moving to Chapter 55 node...")
                MouseUtils.move_and_click_point(world_location[0] + 162, world_location[1] + 143, "template_node")

            # After being on the correct chapter node, scroll down the screen as far as possible and then click the mission to start.
            MouseUtils.scroll_screen(Settings.home_button_location[0], Settings.home_button_location[1] - 50, -1000)
            Game.find_and_click_button(Settings.mission_name.replace(" ", "_"))

            # Apply special navigation for mission "Ch. 70 - Erste Kingdom".
            if Settings.mission_name == "Erste Kingdom Episode 4":
                Game.find_and_click_button("episode_4")
                Game.find_and_click_button("ok")

        return None

    @staticmethod
    def start(first_run: bool) -> int:
        """Starts the process to complete a run for Quest Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of items detected.
        """
        from bot.game import Game

        number_of_items_dropped: int = 0

        # Start the navigation process.
        if first_run:
            Quest._navigate()
        elif Game.find_and_click_button("play_again"):
            Game.check_for_popups()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            Quest._navigate()

        # Check for AP.
        Game.check_for_ap()

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
            if summon_check:
                # Select the Party.
                Game.find_party_and_start_mission(Settings.group_number, Settings.party_number)

                # Close the "Item Picked Up" popup.
                if ImageUtils.confirm_location("items_picked_up"):
                    Game.find_and_click_button("ok")

                # Now start Combat Mode and detect any item drops.
                if CombatMode.start_combat_mode():
                    number_of_items_dropped = Game.collect_loot(is_completed = True)
        else:
            raise QuestException("Failed to arrive at the Summon Selection screen.")

        return number_of_items_dropped
