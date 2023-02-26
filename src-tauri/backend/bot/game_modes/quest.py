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

    _phantagrande_page_1_islands = ["Zinkenstill", "Port Breeze Archipelago", "Valtz Duchy", "Auguste Isles", "Lumacie Archipelago", "Albion Citadel"]
    _phantagrande_page_2_islands = ["Mist-Shrouded Isle", "Golonzo Island", "Amalthea Island", "Former Capital Mephorash", "Agastia"]
    _nalhegrande_page_1_islands = ["Merkmal Island", "Groz Island", "Kluger Island", "The Edgelands"]
    _nalhegrande_page_2_islands = ["Bestia Island", "Reiche Island", "Starke Island"]
    _oarlyegrande_page_1_islands = ["New Utopia"]

    @staticmethod
    def _exit_skydom(current_skydom: str):
        """Exit out of the current skydom onto the world map.

        Args:
            current_skydom (str): Name of the skydom that the bot is currently at.

        Returns:
            None
        """
        from bot.game import Game

        if current_skydom.__contains__("Phantagrande"):
            # Attempt to move to the right-most section of the skydom.
            Game.find_and_click_button("world_right_arrow", suppress_error = True)

            if Game.find_and_click_button("world_skydom") is False:
                raise QuestException("Failed to move out of the Phantagrande Skydom.")
        elif current_skydom.__contains__("Nalhegrande"):
            # Attempt to move to the left-most section of the skydom.
            Game.find_and_click_button("world_left_arrow", suppress_error = True)

            if Game.find_and_click_button("world_skydom") is False:
                raise QuestException("Failed to move out of the Nalhegrande Skydom.")
        elif current_skydom.__contains__("Oarlyegrande"):
            if Game.find_and_click_button("world_skydom") is False:
                raise QuestException("Failed to move out of the Oarlyegrande Skydom.")

        Game.wait(3.0)

        return None

    @staticmethod
    def _enter_skydom(new_skydom: str):
        """Enter a skydom from the world map.

        Args:
            new_skydom (str): Name of the skydom that the bot will be moving to.

        Returns:
            None
        """
        from bot.game import Game

        if new_skydom.__contains__("Phantagrande"):
            if Game.find_and_click_button("skydom_phantagrande") is False:
                raise QuestException("Failed to move into Phantagrande Skydom.")
        elif new_skydom.__contains__("Nalhegrande"):
            if Game.find_and_click_button("skydom_nalhegrande") is False:
                raise QuestException("Failed to move into Nalhegrande Skydom.")
        elif new_skydom.__contains__("Oarlyegrande"):
            if Game.find_and_click_button("skydom_oarlyegrande") is False:
                raise QuestException("Failed to move into Oarlyegrande Skydom.")

        Game.wait(3.0)

        return None

    @staticmethod
    def _navigate_to_phantagrande_skydom_island(map_name: str, current_island: str):
        """Navigates the bot to the specified island inside the Phantagrande Skydom

        Args:
            map_name (str): Name of the expected Island inside the Phantagrande Skydom.
            current_island (str): Name of the Island inside the Phantagrande Skydom that the bot is currently at.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[QUEST] Beginning process to navigate to the island inside the Phantagrande Skydom: {map_name}...")

        if Quest._phantagrande_page_1_islands.__contains__(map_name):
            # Switch pages if bot is on Page 2.
            if Quest._phantagrande_page_2_islands.__contains__(current_island) and Game.find_and_click_button("world_left_arrow") is False:
                raise QuestException("Failed to move to Page 1 of Phantagrande Skydom.")

            # Move to the expected Island.
            if Game.find_and_click_button("map_" + map_name.lower().replace(" ", "_").replace("-", "_")) is False:
                # If the name of the island is obscured, like by the "Next" text indicating that the user's next quest is there, fallback to the manual method.
                arrow_location = ImageUtils.find_button("world_right_arrow")

                if map_name == "Port Breeze Archipelago":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 320, arrow_location[1] - 160, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 215, arrow_location[1] - 100, "world_right_arrow")
                elif map_name == "Valtz Duchy":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 150, arrow_location[1] - 85, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 100, arrow_location[1] - 50, "world_right_arrow")
                elif map_name == "Auguste Isles":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 375, arrow_location[1] - 5, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 250, arrow_location[1] - 5, "world_right_arrow")
                elif map_name == "Lumacie Archipelago":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 85, arrow_location[1] + 40, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 60, arrow_location[1] + 35, "world_right_arrow")
                elif map_name == "Albion Citadel":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 265, arrow_location[1] + 120, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 180, arrow_location[1] + 85, "world_right_arrow")
                else:
                    raise QuestException(f"Unexpected map name when trying to navigate in Phantagrande Skydom Page 1: {map_name}")
        elif Quest._phantagrande_page_2_islands.__contains__(map_name):
            if Quest._phantagrande_page_1_islands.__contains__(current_island) and Game.find_and_click_button("world_right_arrow") is False:
                raise QuestException("Failed to move to Page 2 of Phantagrande Skydom.")

            # Move to the expected Island.
            if not Game.find_and_click_button("map_" + map_name.lower().replace(" ", "_").replace("-", "_")):
                # If the name of the island is obscured, like by the "Next" text indicating that the user's next quest is there, fallback to the manual method.
                arrow_location = ImageUtils.find_button("world_left_arrow")

                if map_name == "Mist-Shrouded Isle":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] + 160, arrow_location[1] + 115, "world_left_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] + 110, arrow_location[1] + 85, "world_left_arrow")
                elif map_name == "Golonzo Island":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] + 360, arrow_location[1] + 85, "world_left_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] + 235, arrow_location[1] + 60, "world_left_arrow")
                elif map_name == "Amalthea Island":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] + 125, arrow_location[1] - 15, "world_left_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] + 85, arrow_location[1] - 5, "world_left_arrow")
                elif map_name == "Former Capital Mephorash":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] + 350, arrow_location[1] - 50, "world_left_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] + 240, arrow_location[1] - 30, "world_left_arrow")
                elif map_name == "Agastia":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] + 190, arrow_location[1] - 150, "world_left_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] + 125, arrow_location[1] - 95, "world_left_arrow")
                else:
                    raise QuestException(f"Unexpected map name when trying to navigate in Phantagrande Skydom Page 2: {map_name}")

        # Click "Go" on the popup after clicking on the island node.
        if Game.find_and_click_button("go") is False:
            raise QuestException(f"Failed to enter {map_name} as the Go button is missing.")

        return None

    @staticmethod
    def _navigate_to_nalhegrande_skydom_island(map_name: str, current_island: str):
        """Navigates the bot to the specified island inside the Nalhegrande Skydom

        Args:
            map_name (str): Name of the expected Island inside the Nalhegrande Skydom.
            current_island (str): Name of the Island inside the Nalhegrande Skydom that the bot is currently at.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[QUEST] Beginning process to navigate to the island inside the Nalhegrande Skydom: {map_name}...")

        if Quest._nalhegrande_page_1_islands.__contains__(map_name):
            # Switch pages if bot is on Page 2.
            if Quest._nalhegrande_page_2_islands.__contains__(current_island) and Game.find_and_click_button("world_left_arrow") is False:
                raise QuestException("Failed to move to Page 1 of Nalhegrande Skydom.")

            # Move to the expected Island.
            if Game.find_and_click_button("map_" + map_name.lower().replace(" ", "_").replace("-", "_")) is False:
                # If the name of the island is obscured, like by the "Next" text indicating that the user's next quest is there, fallback to the manual method.
                arrow_location = ImageUtils.find_button("world_right_arrow")

                if map_name == "Merkmal Island":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 345, arrow_location[1] + 215, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 230, arrow_location[1] + 140, "world_right_arrow")
                elif map_name == "Groz Island":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 310, arrow_location[1] + 35, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 205, arrow_location[1] + 15, "world_right_arrow")
                elif map_name == "Kluger Island":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 100, arrow_location[1] + 90, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 65, arrow_location[1] + 60, "world_right_arrow")
                elif map_name == "The Edgelands":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] - 240, arrow_location[1] - 155, "world_right_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] - 160, arrow_location[1] - 110, "world_right_arrow")
                else:
                    raise QuestException(f"Unexpected map name when trying to navigate in Nalhegrande Skydom Page 1: {map_name}")

        elif Quest._nalhegrande_page_2_islands.__contains__(map_name):
            if Quest._nalhegrande_page_1_islands.__contains__(current_island) and Game.find_and_click_button("world_right_arrow") is False:
                raise QuestException("Failed to move to Page 2 of Nalhegrande Skydom.")

            # Move to the expected Island.
            if not Game.find_and_click_button("map_" + map_name.lower().replace(" ", "_").replace("-", "_")):
                # If the name of the island is obscured, like by the "Next" text indicating that the user's next quest is there, fallback to the manual method.
                arrow_location = ImageUtils.find_button("world_left_arrow")

                if map_name == "Bestia Island":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] + 130, arrow_location[1] + 240, "world_left_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] + 85, arrow_location[1] + 150, "world_right_arrow")
                elif map_name == "Reiche Island":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] + 320, arrow_location[1] + 60, "world_left_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] + 215, arrow_location[1] + 35, "world_right_arrow")
                elif map_name == "Starke Island":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(arrow_location[0] + 170, arrow_location[1] - 100, "world_left_arrow")
                    else:
                        MouseUtils.move_and_click_point(arrow_location[0] + 115, arrow_location[1] - 70, "world_right_arrow")
                else:
                    raise QuestException(f"Unexpected map name when trying to navigate in Nalhegrande Skydom Page 2: {map_name}")

        # Click "Go" on the popup after clicking on the island node.
        if Game.find_and_click_button("go") is False:
            raise QuestException(f"Failed to enter {map_name} as the Go button is missing.")

        return None

    @staticmethod
    def _navigate_to_oarlyegrande_skydom_island(map_name: str):
        """Navigates the bot to the specified island inside the Oarlyegrande Skydom

        Args:
            map_name (str): Name of the expected Island inside the Oarlyegrande Skydom.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[QUEST] Beginning process to navigate to the island inside the Oarlyegrande Skydom: {map_name}...")

        if Quest._oarlyegrande_page_1_islands.__contains__(map_name):
            # Move to the expected Island.
            if Game.find_and_click_button("map_" + map_name.lower().replace(" ", "_").replace("-", "_")) is False:
                # If the name of the island is obscured, like by the "Next" text indicating that the user's next quest is there, fallback to the manual method.
                skydom_location = ImageUtils.find_button("world_skydom")

                if map_name == "New Utopia":
                    if Settings.use_first_notch is False:
                        MouseUtils.move_and_click_point(skydom_location[0] - 200, skydom_location[1] + 175, "world_skydom")
                    else:
                        MouseUtils.move_and_click_point(skydom_location[0] - 130, skydom_location[1] + 120, "world_skydom")
                else:
                    raise QuestException(f"Unexpected map name when trying to navigate in Oarlyegrande Skydom: {map_name}")

        # Click "Go" after clicking on the island node.
        if Game.find_and_click_button("go_oarlyegrande") is False:
            raise QuestException(f"Failed to enter {map_name} as the Go button is missing.")

        return None

    @staticmethod
    def _select_episode():
        """Selects the required episode using the mission's name.

        Returns:
            None
        """
        from bot.game import Game

        if Settings.mission_name.__contains__("Episode"):
            if Settings.mission_name.__contains__("Episode 1"):
                Game.find_and_click_button("episode_1")
            elif Settings.mission_name.__contains__("Episode 2"):
                Game.find_and_click_button("episode_2")
            elif Settings.mission_name.__contains__("Episode 3"):
                Game.find_and_click_button("episode_3")
            elif Settings.mission_name.__contains__("Episode 4"):
                Game.find_and_click_button("episode_4")

            Game.find_and_click_button("ok")

        return None

    @staticmethod
    def _select_phantagrande_chapter_node():
        """Selects the Phantagrande chapter node for the mission.

        Returns:
            None
        """

        # Grab the location of the "World" button.
        world_location = ImageUtils.find_button("world", tries = 30)
        if world_location is None:
            world_location = ImageUtils.find_button("world2", tries = 30)

        if Settings.mission_name == "Scattered Cargo":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 1 (115) node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 95, world_location[1] + 95, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 60, world_location[1] + 60, "template_node")
        elif Settings.mission_name == "Lucky Charm Hunt":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 6 (122) node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 330, world_location[1] + 15, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 215, world_location[1] + 15, "template_node")
        elif Settings.mission_name == "Special Op's Request":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 8 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 260, world_location[1] + 150, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 165, world_location[1] + 105, "template_node")
        elif Settings.mission_name == "Threat to the Fisheries":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 9 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 215, world_location[1] + 115, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 140, world_location[1] + 80, "template_node")
        elif Settings.mission_name == "The Fruit of Lumacie" or Settings.mission_name == "Whiff of Danger":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 13 (39/52) node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 80, world_location[1] + 90, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 45, world_location[1] + 65, "template_node")
        elif Settings.mission_name == "I Challenge You!":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 17 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 120, world_location[1] + 120, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 70, world_location[1] + 80, "template_node")
        elif Settings.mission_name == "For Whom the Bell Tolls":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 22 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 180, world_location[1] + 35, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 115, world_location[1] + 25, "template_node")
        elif Settings.mission_name == "Golonzo's Battles of Old":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 25 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 195, world_location[1] + 5, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 130, world_location[1] + 5, "template_node")
        elif Settings.mission_name == "The Dungeon Diet":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 30 (44/65) node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 240, world_location[1] + 25, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 160, world_location[1] + 15, "template_node")
        elif Settings.mission_name == "Trust Busting Dustup":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 36 (123) node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 320, world_location[1] + 15, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 210, world_location[1] + 10, "template_node")
        elif Settings.mission_name == "Erste Kingdom Episode 4":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 70 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 255, world_location[1] + 135, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 165, world_location[1] + 95, "template_node")
        elif Settings.mission_name == "Imperial Wanderer's Soul":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 55 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 160, world_location[1] + 145, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 105, world_location[1] + 95, "template_node")
        elif Settings.mission_name == "Rocket Raid":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 59 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 70, world_location[1] + 85, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 45, world_location[1] + 60, "template_node")
        else:
            raise QuestException(f"Selected mission of {Settings.mission_name} does not exist.")

        return None

    @staticmethod
    def _select_nalhegrande_chapter_node():
        """Selects the Nalhegrande chapter node for the mission.

        Returns:
            None
        """
        from bot.game import Game

        # Grab the location of the "World" button.
        world_location = ImageUtils.find_button("world", tries = 30)
        if world_location is None:
            world_location = ImageUtils.find_button("world2", tries = 30)

        if Settings.mission_name == "Stocking Up for Winter":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 80 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 15, world_location[1] + 65, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 10, world_location[1] + 50, "template_node")
        elif Settings.mission_name == "The Mysterious Room":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 81 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 200, world_location[1] + 45, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 135, world_location[1] + 35, "template_node")
        elif Settings.mission_name == "The Right of Might" or Settings.mission_name == "Idelva Kingdom Episode 4":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 124 node...")
            Game.find_and_click_button("arcarum_sandbox_right_arrow", tries = 1, suppress_error = True)
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 235, world_location[1] + 50, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 160, world_location[1] + 35, "template_node")
        elif Settings.mission_name == "Pholia the Maiden Episode 1" or Settings.mission_name == "Pholia the Maiden Episode 3":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 85 node...")
            Game.find_and_click_button("arcarum_sandbox_right_arrow", tries = 1, suppress_error = True)
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 165, world_location[1] + 130, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 110, world_location[1] + 90, "template_node")
        elif Settings.mission_name == "Teachings of the Sage Episode 2":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 89 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 335, world_location[1] + 70, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 220, world_location[1] + 50, "template_node")
        elif Settings.mission_name == "Isle of Primals Episode 3":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 129 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 225, world_location[1] + 135, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 150, world_location[1] + 95, "template_node")
        elif Settings.mission_name == "Deception's Inception Episode 4":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 100 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 285, world_location[1] + 65, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 190, world_location[1] + 50, "template_node")
        elif Settings.mission_name == "Be All That You Can Be":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 102 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 10, world_location[1] + 80, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 5, world_location[1] + 45, "template_node")
        elif Settings.mission_name == "Once Lost, Once Found":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 108 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 295, world_location[1] + 70, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 195, world_location[1] + 50, "template_node")
        elif Settings.mission_name == "A Girl Named Mika Episode 2":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 113 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 180, world_location[1] + 65, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 120, world_location[1] + 50, "template_node")
        else:
            raise QuestException(f"Selected mission of {Settings.mission_name} does not exist.")

        return None

    @staticmethod
    def _select_oarlyegrande_chapter_node():
        """Selects the Oarlyegrande chapter node for the mission.

        Returns:
            None
        """
        # Grab the location of the "World" button.
        world_location = ImageUtils.find_button("world", tries = 30)
        if world_location is None:
            world_location = ImageUtils.find_button("world2", tries = 30)

        if Settings.mission_name == "House of Happiness":
            MessageLog.print_message(f"\n[QUEST] Moving to Chapter 132 node...")
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(world_location[0] + 155, world_location[1] + 130, "template_node")
            else:
                MouseUtils.move_and_click_point(world_location[0] + 105, world_location[1] + 90, "template_node")
        else:
            raise QuestException(f"Selected mission of {Settings.mission_name} does not exist.")

        return None

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

        current_island = ""
        formatted_map_name = Settings.map_name.lower().replace(" ", "_").replace("-", "_")

        # Determine target skydom.
        if Quest._phantagrande_page_1_islands.__contains__(Settings.map_name) or Quest._phantagrande_page_2_islands.__contains__(Settings.map_name):
            target_skydom = "Phantagrande Skydom"
        elif Quest._nalhegrande_page_1_islands.__contains__(Settings.map_name) or Quest._nalhegrande_page_2_islands.__contains__(Settings.map_name):
            target_skydom = "Nalhegrande Skydom"
        elif Quest._oarlyegrande_page_1_islands.__contains__(Settings.map_name):
            target_skydom = "Oarlyegrande Skydom"
        else:
            raise QuestException("Invalid Skydom associated with map in settings.")

        # Check which island the bot is at.
        if ImageUtils.confirm_location(f"map_{formatted_map_name}", tries = 1):
            MessageLog.print_message(f"[QUEST] Bot is currently on the correct island.")
            check_location = True
            current_skydom = target_skydom
        else:
            MessageLog.print_message(f"[QUEST] Bot is currently not on the correct island.")
            check_location = False

            location_list = Quest._phantagrande_page_1_islands + Quest._phantagrande_page_2_islands + Quest._nalhegrande_page_1_islands + Quest._nalhegrande_page_2_islands + Quest._oarlyegrande_page_1_islands

            # Determine current island.
            while len(location_list) > 0:
                temp_map_location = location_list.pop(0)
                temp_formatted_map_location = temp_map_location.lower().replace(" ", "_").replace("-", "_")

                if ImageUtils.confirm_location(f"map_{temp_formatted_map_location}", tries = 1):
                    MessageLog.print_message(f"[QUEST] Bot's current location is at {temp_map_location}. Now moving to {Settings.map_name}...")
                    current_island = temp_map_location
                    break

            # Now determine current skydom.
            if Quest._phantagrande_page_1_islands.__contains__(current_island) or Quest._phantagrande_page_2_islands.__contains__(current_island):
                current_skydom = "Phantagrande Skydom"
            elif Quest._nalhegrande_page_1_islands.__contains__(current_island) or Quest._nalhegrande_page_2_islands.__contains__(current_island):
                current_skydom = "Nalhegrande Skydom"
            elif Quest._oarlyegrande_page_1_islands.__contains__(current_island):
                current_skydom = "Oarlyegrande Skydom"
            else:
                raise QuestException("Current island does not fit into any of the skydoms defined.")

        # Once the bot has determined where it is, go to the Quest screen.
        Game.find_and_click_button("quest")

        Game.wait(3.0)

        # Check for the "You retreated from the raid battle" popup.
        if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
            Game.find_and_click_button("ok")

        if ImageUtils.confirm_location("quest"):
            # If the bot is currently not at the correct island, exit from it.
            if not check_location:
                # Click the "World" button to exit the island and land at the World page.
                Game.find_and_click_button("world")

                Game.wait(3.0)

                # If current skydom is different from the target skydom, move to the target skydom.
                if current_skydom != target_skydom:
                    Quest._exit_skydom(current_skydom)
                    Quest._enter_skydom(target_skydom)

            # From the World page, move to the target island and then select the target chapter node.
            if Quest._phantagrande_page_1_islands.__contains__(Settings.map_name) or Quest._phantagrande_page_2_islands.__contains__(Settings.map_name):
                if not check_location:
                    Quest._navigate_to_phantagrande_skydom_island(Settings.map_name, current_island)
                    Game.wait(3.0)

                Quest._select_phantagrande_chapter_node()
            elif Quest._nalhegrande_page_1_islands.__contains__(Settings.map_name) or Quest._nalhegrande_page_2_islands.__contains__(Settings.map_name):
                if not check_location:
                    Quest._navigate_to_nalhegrande_skydom_island(Settings.map_name, current_island)
                    Game.wait(3.0)

                Quest._select_nalhegrande_chapter_node()
            elif Quest._oarlyegrande_page_1_islands.__contains__(Settings.map_name):
                if not check_location:
                    Quest._navigate_to_oarlyegrande_skydom_island(Settings.map_name)
                    Game.wait(3.0)

                Quest._select_oarlyegrande_chapter_node()

            # After being on the correct chapter node, scroll down the screen and then click the mission to start.
            MessageLog.print_message(f"[QUEST] Now bringing up the Summon Selection screen for \"{Settings.mission_name}\"...")
            tries = 5
            while Game.find_and_click_button("mission_" + Settings.mission_name.replace(" ", "_")) is False:
                tries -= 1
                if tries <= 0:
                    raise QuestException("Cannot find the mission location after scrolling down the Quest screen multiple times.")

                MouseUtils.scroll_screen(Settings.home_button_location[0], Settings.home_button_location[1] - 50, -500)
                Game.wait(0.5)

            # Now click on the mission node to start.
            Game.find_and_click_button("mission_" + Settings.mission_name.replace(" ", "_"))

            # Apply special navigation for Episode missions.
            Quest._select_episode()
        else:
            raise QuestException("Failed to arrive at the Quest page.")

        return None

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Quest Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

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
                if ImageUtils.confirm_location("items_picked_up", tries = 10):
                    Game.find_and_click_button("ok")

                # Now start Combat Mode and detect any item drops.
                if CombatMode.start_combat_mode():
                    Game.collect_loot(is_completed = True)
        else:
            raise QuestException("Failed to arrive at the Summon Selection screen.")

        return None
