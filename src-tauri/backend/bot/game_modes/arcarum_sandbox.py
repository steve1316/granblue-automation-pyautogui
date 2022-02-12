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
            "x": 335,
            "y": 210
        },
        "Living Lightning Rod": {
            "section": 0,
            "x": 60,
            "y": 200
        },
        "Eletion Drake": {
            "section": 0,
            "x": 105,
            "y": 340
        },
        "Paradoxical Gate": {
            "section": 1,
            "x": 305,
            "y": 205
        },
        "Blazing Everwing": {
            "section": 1,
            "x": 180,
            "y": 190
        },
        "Death Seer": {
            "section": 1,
            "x": 55,
            "y": 270
        },
        "Hundred-Armed Hulk": {
            "section": 2,
            "x": 305,
            "y": 185
        },
        "Terror Trifecta": {
            "section": 2,
            "x": 210,
            "y": 260
        },
        "Rageborn One": {
            "section": 2,
            "x": 285,
            "y": 295
        },

        # Zone Faym
        "Tident Grandmaster": {
            "section": 0,
            "x": 350,
            "y": 210
        },
        "Hoarfrost Icequeen": {
            "section": 0,
            "x": 210,
            "y": 270
        },
        "Oceanic Archon": {
            "section": 0,
            "x": 95,
            "y": 340
        },
        "Farsea Predator": {
            "section": 1,
            "x": 350,
            "y": 210
        },
        "Faymian Fortress": {
            "section": 1,
            "x": 205,
            "y": 270
        },
        "Draconic Simulacrum": {
            "section": 1,
            "x": 70,
            "y": 210
        },
        "Azureflame Dragon": {
            "section": 2,
            "x": 340,
            "y": 215
        },
        "Eyes of Sorrow": {
            "section": 2,
            "x": 315,
            "y": 345
        },
        "Mad Shearwielder": {
            "section": 2,
            "x": 60,
            "y": 215
        },

        # Zone Goliath
        "Avatar of Avarice": {
            "section": 0,
            "x": 285,
            "y": 345
        },
        "Temptation's Guide": {
            "section": 0,
            "x": 215,
            "y": 170
        },
        "World's Veil": {
            "section": 0,
            "x": 170,
            "y": 270
        },
        "Goliath Keeper": {
            "section": 1,
            "x": 355,
            "y": 335
        },
        "Bloodstained Barbarian": {
            "section": 1,
            "x": 260,
            "y": 205
        },
        "Frenzied Howler": {
            "section": 1,
            "x": 50,
            "y": 190
        },
        "Goliath Vanguard": {
            "section": 1,
            "x": 65,
            "y": 390
        },
        "Vestige of Truth": {
            "section": 2,
            "x": 375,
            "y": 210
        },
        "Writhing Despair": {
            "section": 2,
            "x": 250,
            "y": 260
        },

        # Zone Harbinger
        "Vengeful Demigod": {
            "section": 0,
            "x": 235,
            "y": 185
        },
        "Dirgesinger": {
            "section": 0,
            "x": 345,
            "y": 235
        },
        "Wildwind COnjurer/Fullthunder Conjurer": {
            "section": 0,
            "x": 215,
            "y": 310
        },
        "Harbinger Simurgh": {
            "section": 0,
            "x": 120,
            "y": 260
        },
        "Harbinger Hardwood": {
            "section": 1,
            "x": 365,
            "y": 320
        },
        "Demanding Stormgod": {
            "section": 1,
            "x": 170,
            "y": 250
        },
        "Harbinger Tyrant": {
            "section": 2,
            "x": 370,
            "y": 200
        },
        "Phantasmagoric Aberration": {
            "section": 2,
            "x": 230,
            "y": 315
        },
        "Dimensional Riftwalker": {
            "section": 2,
            "x": 115,
            "y": 245
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

        # Now click on the specified node that has the mission offset by the coordinates associated with it based off of the Home Menu button location.
        home_location: Tuple[int, int] = ImageUtils.find_button("home_menu")
        MouseUtils.move_and_click_point(home_location[0] - x, home_location[1] + y, "arcarum_node")

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
    @staticmethod
    def _refill_aap():
        """Refills AAP if necessary.

        Returns:
            None
        """
        if ImageUtils.confirm_location("aap"):
            from bot.game import Game

            MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Bot ran out of AAP. Refilling now...")
            use_locations = ImageUtils.find_all("use")
            MouseUtils.move_and_click_point(use_locations[0][0], use_locations[0][1], "use")

            Game.wait(1.0)
            Game.find_and_click_button("ok")
            Game.wait(1.0)

            MessageLog.print_message(f"[ARCARUM.SANDBOX] AAP is now refilled.")

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
        # Refill AAP if needed.
        ArcarumSandbox._refill_aap()

        if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
            if CombatMode.start_combat_mode():
                number_of_items_dropped = Game.collect_loot(is_completed = True)

        return number_of_items_dropped
