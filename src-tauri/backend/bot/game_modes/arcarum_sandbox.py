from typing import Tuple, List

from utils.message_log import MessageLog
from utils.settings import Settings
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class ArcarumSandboxException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ArcarumSandbox:
    """
    Provides the navigation and any necessary utility functions to handle the Arcarum Replicard Sandbox game mode.
    """

    _first_run: bool = True

    _mission_data = {
        # Zone Eletio
        "Slithering Seductress": {
            "section": 0,
            "x": 178,
            "y": 341
        },
        "Living Lightning Rod": {
            "section": 0,
            "x": 452,
            "y": 334
        },
        "Eletion Drake": {
            "section": 0,
            "x": 408,
            "y": 470
        },
        "Paradoxical Gate": {
            "section": 1,
            "x": 207,
            "y": 341
        },
        "Blazing Everwing": {
            "section": 1,
            "x": 337,
            "y": 327
        },
        "Death Seer": {
            "section": 1,
            "x": 461,
            "y": 405
        },
        "Hundred-Armed Hulk": {
            "section": 2,
            "x": 212,
            "y": 321
        },
        "Terror Trifecta": {
            "section": 2,
            "x": 305,
            "y": 395
        },
        "Rageborn One": {
            "section": 2,
            "x": 230,
            "y": 428
        },

        # Zone Faym
        "Tident Grandmaster": {
            "section": 0,
            "x": 164,
            "y": 344
        },
        "Hoarfrost Icequeen": {
            "section": 0,
            "x": 306,
            "y": 405
        },
        "Oceanic Archon": {
            "section": 0,
            "x": 422,
            "y": 477
        },
        "Farsea Predator": {
            "section": 1,
            "x": 165,
            "y": 347
        },
        "Faymian Fortress": {
            "section": 1,
            "x": 309,
            "y": 406
        },
        "Draconic Simulacrum": {
            "section": 1,
            "x": 448,
            "y": 347
        },
        "Azureflame Dragon": {
            "section": 2,
            "x": 174,
            "y": 348
        },
        "Eyes of Sorrow": {
            "section": 2,
            "x": 199,
            "y": 481
        },
        "Mad Shearwielder": {
            "section": 2,
            "x": 453,
            "y": 351
        },

        # Zone Goliath
        "Avatar of Avarice": {
            "section": 0,
            "x": 231,
            "y": 482
        },
        "Temptation's Guide": {
            "section": 0,
            "x": 299,
            "y": 307
        },
        "World's Veil": {
            "section": 0,
            "x": 345,
            "y": 405
        },
        "Goliath Keeper": {
            "section": 1,
            "x": 160,
            "y": 472
        },
        "Bloodstained Barbarian": {
            "section": 1,
            "x": 254,
            "y": 338
        },
        "Frenzied Howler": {
            "section": 1,
            "x": 467,
            "y": 324
        },
        "Goliath Vanguard": {
            "section": 1,
            "x": 448,
            "y": 473
        },
        "Vestige of Truth": {
            "section": 2,
            "x": 142,
            "y": 344
        },
        "Writhing Despair": {
            "section": 2,
            "x": 264,
            "y": 396
        },

        # Zone Harbinger
        "Vengeful Demigod": {
            "section": 0,
            "x": 278,
            "y": 318
        },
        "Dirgesinger": {
            "section": 0,
            "x": 170,
            "y": 368
        },
        "Wildwind COnjurer/Fullthunder Conjurer": {
            "section": 0,
            "x": 300,
            "y": 446
        },
        "Harbinger Simurgh": {
            "section": 0,
            "x": 396,
            "y": 396
        },
        "Harbinger Hardwood": {
            "section": 1,
            "x": 148,
            "y": 454
        },
        "Demanding Stormgod": {
            "section": 1,
            "x": 244,
            "y": 384
        },
        "Harbinger Tyrant": {
            "section": 2,
            "x": 143,
            "y": 336
        },
        "Phantasmagoric Aberration": {
            "section": 2,
            "x": 284,
            "y": 450
        },
        "Dimensional Riftwalker": {
            "section": 2,
            "x": 400,
            "y": 380
        }
    }

    @staticmethod
    def _navigate_to_mission():
        """Navigates to the specified Arcarum Replicard Sandbox mission inside the current Zone.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"[ARCARUM.SANDBOX] Now beginning navigation to {Settings.mission_name} inside {Settings.map_name}...")

        section: int = ArcarumSandbox._mission_data[Settings.mission_name]["section"]
        x: int = ArcarumSandbox._mission_data[Settings.mission_name]["x"]
        y: int = ArcarumSandbox._mission_data[Settings.mission_name]["y"]

        # Shift the Zone over to the right based on the section that the mission is located at.
        if section == 1:
            Game.find_and_click_button("arcarum_sandbox_right_arrow")
        elif section == 2:
            Game.find_and_click_button("arcarum_sandbox_right_arrow")
            Game.wait(1.0)
            Game.find_and_click_button("arcarum_sandbox_right_arrow")

        Game.wait(1.0)

        # Now click on the specified node that has the mission offset by the coordinates associated with it based off of the Home button location.
        home_location: Tuple[int, int] = ImageUtils.find_button("home")
        MouseUtils.move_and_click_point(home_location[0] - x, home_location[1] - y, "arcarum_node")

        Game.wait(1.0)

        # If there is no Defender, then the first action is the mission itself. Else, it is the second action.
        action_locations: List[Tuple[int, ...]] = ImageUtils.find_all("arcarum_sandbox_action")
        if len(action_locations) == 1:
            MouseUtils.move_and_click_point(action_locations[0][0], action_locations[0][1], "arcarum_sandbox_action")
        else:
            MouseUtils.move_and_click_point(action_locations[1][0], action_locations[1][1], "arcarum_sandbox_action")

        return None

    @staticmethod
    def _navigate_to_zone():
        """Navigates to the specified Arcarum Replicard Sandbox Zone.

        Returns:
            None
        """
        from bot.game import Game

        if ArcarumSandbox._first_run:
            MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Now beginning navigation to {Settings.map_name}...")
            Game.go_back_home()

            # Navigate to the Arcarum banner.
            tries = 5
            while tries > 0:
                if Game.find_and_click_button("arcarum_banner", tries = 1) is False:
                    MouseUtils.scroll_screen_from_home_button(-300)
                    tries -= 1
                    if tries <= 0:
                        raise ArcarumSandboxException("Failed to navigate to Arcarum from the Home screen.")
                else:
                    break

            ArcarumSandbox._first_run = False
        else:
            Game.wait(4.0)

        # If the bot is not at Replicard Sandbox and instead is at regular Arcarum, navigate to Replicard Sandbox by clicking on its banner.
        if ImageUtils.confirm_location("arcarum_sandbox") is False:
            Game.find_and_click_button("arcarum_sandbox_banner")

        # Move to the Zone that the user's mission is at.
        if Settings.map_name == "Zone Eletio":
            Game.find_and_click_button("arcarum_sandbox_zone_eletio")
        elif Settings.map_name == "Zone Faym":
            Game.find_and_click_button("arcarum_sandbox_zone_faym")
        elif Settings.map_name == "Zone Goliath":
            Game.find_and_click_button("arcarum_sandbox_zone_goliath")
        elif Settings.map_name == "Zone Harbinger":
            Game.find_and_click_button("arcarum_sandbox_zone_harbinger")
        else:
            raise ArcarumSandboxException("Invalid map name provided for Arcarum Replicard Sandbox navigation.")

        Game.wait(2.0)

        # Now that the Zone is on screen, have the bot move all the way to the left side of the map.
        MessageLog.print_message(f"[ARCARUM.SANDBOX] Now determining if bot is starting all the way at the left edge of the Zone...")
        while Game.find_and_click_button("arcarum_sandbox_left_arrow", tries = 1, suppress_error = True):
            Game.wait(1.0)

        MessageLog.print_message(f"[ARCARUM.SANDBOX] Left edge of the Zone has been reached.")

        ArcarumSandbox._navigate_to_mission()

        return None

    @staticmethod
    def start() -> int:
        """Starts the process of completing Arcarum Replicard Sandbox missions.

        Returns:
            (int): Number of items detected.
        """
        from bot.game import Game

        number_of_items_dropped: int = 0

        # Start the navigation process.
        if ArcarumSandbox._first_run:
            ArcarumSandbox._navigate_to_zone()
        elif Game.find_and_click_button("play_again"):
            Game.check_for_popups()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then click the Expedition button.
            Game.check_for_pending()
            Game.find_and_click_button("expedition")

        # TODO: Create specialized function to refill AAP, not AP.

        if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
            if CombatMode.start_combat_mode():
                number_of_items_dropped = Game.collect_loot(is_completed = True)

        return number_of_items_dropped
