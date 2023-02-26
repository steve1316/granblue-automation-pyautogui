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

    # The x and y coordinates are the difference between the center of the Menu button at the top-right and the center of the node itself.
    # The section refers to the left most page that the node is located in starting at page 0.
    _mission_data = {
        ##########
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
        "Eletion Glider": {
            "section": 2,
            "x": 70,
            "y": 260
        },

        ##########
        # Zone Faym
        "Trident Grandmaster": {
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
        "Faymian Gun": {
            "section": 2,
            "x": 200,
            "y": 285
        },

        ##########
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
            "y": 360
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
        "Goliath Triune": {
            "section": 2,
            "x": 50,
            "y": 300
        },

        ##########
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
        "Wildwind Conjurer/Fullthunder Conjurer": {
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
            "x": 275,
            "y": 250
        },
        "Harbinger Stormer": {
            "section": 1,
            "x": 180,
            "y": 150
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
        },

        ##########
        # Zone Invidia
        "Infernal Hellbeast": {
            "section": 0,
            "x": 350,
            "y": 215
        },
        "Spikeball": {
            "section": 0,
            "x": 115,
            "y": 260
        },
        "Blushing Groom": {
            "section": 0,
            "x": 45,
            "y": 185
        },
        "Unworldly Guardian": {
            "section": 1,
            "x": 290,
            "y": 260
        },
        "Deva of Wisdom": {
            "section": 1,
            "x": 185,
            "y": 130
        },
        "Sword of Aberration": {
            "section": 1,
            "x": 170,
            "y": 220
        },
        "Athena Militis": {
            "section": 1,
            "x": 185,
            "y": 350
        },

        ##########
        # Zone Joculator
        "Glacial Hellbeast": {
            "section": 0,
            "x": 50,
            "y": 180
        },
        "Giant Sea Plant": {
            "section": 0,
            "x": 375,
            "y": 280
        },
        "Maiden of the Depths": {
            "section": 0,
            "x": 145,
            "y": 340
        },
        "Bloody Soothsayer": {
            "section": 1,
            "x": 260,
            "y": 340
        },
        "Nebulous One": {
            "section": 1,
            "x": 30,
            "y": 280
        },
        "Dreadful Scourge": {
            "section": 1,
            "x": 240,
            "y": 140
        },
        "Grani Militis": {
            "section": 1,
            "x": 200,
            "y": 230
        },

        ##########
        # Zone Kalendae
        "Bedeviled Plague": {
            "section": 1,
            "x": 300,
            "y": 180
        },
        "Tainted Hellmaiden": {
            "section": 1,
            "x": 100,
            "y": 340
        },
        "Watcher from Above": {
            "section": 1,
            "x": 20,
            "y": 215
        },
        "Scintillant Matter": {
            "section": 0,
            "x": 365,
            "y": 245
        },
        "Ebony Executioner": {
            "section": 0,
            "x": 250,
            "y": 145
        },
        "Hellbeast of Doom": {
            "section": 0,
            "x": 125,
            "y": 345
        },
        "Baal Militis": {
            "section": 0,
            "x": 220,
            "y": 245
        },

        ##########
        # Zone Liber
        "Mounted Toxophilite": {
            "section": 0,
            "x": 225,
            "y": 145
        },
        "Beetle of Damnation": {
            "section": 0,
            "x": 230,
            "y": 345
        },
        "Ageless Guardian Beast": {
            "section": 0,
            "x": 120,
            "y": 250
        },
        "Solar Princess": {
            "section": 1,
            "x": 330,
            "y": 265
        },
        "Drifting Blade Demon": {
            "section": 1,
            "x": 225,
            "y": 150
        },
        "Simpering Beast": {
            "section": 1,
            "x": 220,
            "y": 335
        },
        "Garuda Militis": {
            "section": 1,
            "x": 50,
            "y": 225
        },
    }

    # The x and y coordinates are the difference between the center of the Menu button at the top-right and the center of the node itself.
    # The section refers to the left most page that the node is located in starting at page 0.
    _mission_data_first_notch = {
        ##########
        # Zone Eletio
        "Slithering Seductress": {
            "section": 0,
            "x": 225,
            "y": 135
        },
        "Living Lightning Rod": {
            "section": 0,
            "x": 40,
            "y": 200
        },
        "Eletion Drake": {
            "section": 0,
            "x": 70,
            "y": 220
        },
        "Paradoxical Gate": {
            "section": 1,
            "x": 225,
            "y": 135
        },
        "Blazing Everwing": {
            "section": 1,
            "x": 115,
            "y": 125
        },
        "Death Seer": {
            "section": 1,
            "x": 15,
            "y": 180
        },
        "Hundred-Armed Hulk": {
            "section": 2,
            "x": 200,
            "y": 125
        },
        "Terror Trifecta": {
            "section": 2,
            "x": 140,
            "y": 170
        },
        "Rageborn One": {
            "section": 2,
            "x": 190,
            "y": 230
        },
        "Eletion Glider": {
            "section": 2,
            "x": 40,
            "y": 165
        },

        ##########
        # Zone Faym
        "Trident Grandmaster": {
            "section": 0,
            "x": 200,
            "y": 140
        },
        "Hoarfrost Icequeen": {
            "section": 0,
            "x": 140,
            "y": 140
        },
        "Oceanic Archon": {
            "section": 0,
            "x": 60,
            "y": 225
        },
        "Farsea Predator": {
            "section": 1,
            "x": 235,
            "y": 140
        },
        "Faymian Fortress": {
            "section": 1,
            "x": 135,
            "y": 180
        },
        "Draconic Simulacrum": {
            "section": 1,
            "x": 45,
            "y": 140
        },
        "Azureflame Dragon": {
            "section": 2,
            "x": 225,
            "y": 90
        },
        "Eyes of Sorrow": {
            "section": 2,
            "x": 210,
            "y": 225
        },
        "Mad Shearwielder": {
            "section": 2,
            "x": 40,
            "y": 145
        },
        "Faymian Gun": {
            "section": 2,
            "x": 135,
            "y": 175
        },

        ##########
        # Zone Goliath
        "Avatar of Avarice": {
            "section": 0,
            "x": 190,
            "y": 235
        },
        "Temptation's Guide": {
            "section": 0,
            "x": 145,
            "y": 115
        },
        "World's Veil": {
            "section": 0,
            "x": 110,
            "y": 175
        },
        "Goliath Keeper": {
            "section": 1,
            "x": 235,
            "y": 220
        },
        "Bloodstained Barbarian": {
            "section": 1,
            "x": 170,
            "y": 135
        },
        "Frenzied Howler": {
            "section": 1,
            "x": 30,
            "y": 125
        },
        "Goliath Vanguard": {
            "section": 1,
            "x": 40,
            "y": 225
        },
        "Vestige of Truth": {
            "section": 2,
            "x": 245,
            "y": 140
        },
        "Writhing Despair": {
            "section": 2,
            "x": 165,
            "y": 170
        },
        "Goliath Triune": {
            "section": 2,
            "x": 35,
            "y": 210
        },

        ##########
        # Zone Harbinger
        "Vengeful Demigod": {
            "section": 0,
            "x": 160,
            "y": 120
        },
        "Dirgesinger": {
            "section": 0,
            "x": 230,
            "y": 155
        },
        "Wildwind Conjurer/Fullthunder Conjurer": {
            "section": 0,
            "x": 140,
            "y": 205
        },
        "Harbinger Simurgh": {
            "section": 0,
            "x": 80,
            "y": 175
        },
        "Harbinger Hardwood": {
            "section": 1,
            "x": 245,
            "y": 215
        },
        "Demanding Stormgod": {
            "section": 1,
            "x": 180,
            "y": 165
        },
        "Harbinger Stormer": {
            "section": 1,
            "x": 125,
            "y": 105
        },
        "Harbinger Tyrant": {
            "section": 2,
            "x": 245,
            "y": 135
        },
        "Phantasmagoric Aberration": {
            "section": 2,
            "x": 155,
            "y": 210
        },
        "Dimensional Riftwalker": {
            "section": 2,
            "x": 75,
            "y": 165
        },

        ##########
        # Zone Invidia
        "Infernal Hellbeast": {
            "section": 0,
            "x": 235,
            "y": 140
        },
        "Spikeball": {
            "section": 0,
            "x": 80,
            "y": 170
        },
        "Blushing Groom": {
            "section": 0,
            "x": 30,
            "y": 120
        },
        "Unworldly Guardian": {
            "section": 1,
            "x": 195,
            "y": 170
        },
        "Deva of Wisdom": {
            "section": 1,
            "x": 125,
            "y": 85
        },
        "Sword of Aberration": {
            "section": 1,
            "x": 115,
            "y": 145
        },
        "Athena Militis": {
            "section": 1,
            "x": 120,
            "y": 215
        },

        ##########
        # Zone Joculator
        "Glacial Hellbeast": {
            "section": 0,
            "x": 35,
            "y": 125
        },
        "Giant Sea Plant": {
            "section": 0,
            "x": 255,
            "y": 185
        },
        "Maiden of the Depths": {
            "section": 0,
            "x": 100,
            "y": 225
        },
        "Bloody Soothsayer": {
            "section": 1,
            "x": 175,
            "y": 225
        },
        "Nebulous One": {
            "section": 1,
            "x": 20,
            "y": 185
        },
        "Dreadful Scourge": {
            "section": 1,
            "x": 160,
            "y": 90
        },
        "Grani Militis": {
            "section": 1,
            "x": 135,
            "y": 165
        },

        ##########
        # Zone Kalendae
        "Bedeviled Plague": {
            "section": 1,
            "x": 200,
            "y": 120
        },
        "Tainted Hellmaiden": {
            "section": 1,
            "x": 70,
            "y": 225
        },
        "Watcher from Above": {
            "section": 1,
            "x": 15,
            "y": 140
        },
        "Scintillant Matter": {
            "section": 0,
            "x": 245,
            "y": 160
        },
        "Ebony Executioner": {
            "section": 0,
            "x": 170,
            "y": 90
        },
        "Hellbeast of Doom": {
            "section": 0,
            "x": 85,
            "y": 230
        },
        "Baal Militis": {
            "section": 0,
            "x": 135,
            "y": 155
        },

        ##########
        # Zone Liber
        "Mounted Toxophilite": {
            "section": 0,
            "x": 155,
            "y": 95
        },
        "Beetle of Damnation": {
            "section": 0,
            "x": 155,
            "y": 230
        },
        "Ageless Guardian Beast": {
            "section": 0,
            "x": 85,
            "y": 165
        },
        "Solar Princess": {
            "section": 1,
            "x": 220,
            "y": 175
        },
        "Drifting Blade Demon": {
            "section": 1,
            "x": 150,
            "y": 100
        },
        "Simpering Beast": {
            "section": 1,
            "x": 150,
            "y": 225
        },
        "Garuda Militis": {
            "section": 1,
            "x": 30,
            "y": 160
        },
    }

    @staticmethod
    def _navigate_to_mission(skip_to_action: bool = False):
        """Navigates to the specified Arcarum Replicard Sandbox mission inside the current Zone.

        Args:
            skip_to_action (bool, optional): True if the mission is already selected. Defaults to False.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"[ARCARUM.SANDBOX] Now beginning navigation to {Settings.mission_name} inside {Settings.map_name}...")

        if skip_to_action is False:
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
        elif Settings.enable_defender and Settings.number_of_defeated_defenders < Settings.number_of_defenders:
            MouseUtils.move_and_click_point(action_locations[0][0], action_locations[0][1], "arcarum_sandbox_action")
            MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Found Defender and fighting it...")
            Settings.engaged_defender_battle = True
        else:
            MouseUtils.move_and_click_point(action_locations[1][0], action_locations[1][1], "arcarum_sandbox_action")

        return None

    @staticmethod
    def _reset_position():
        """Resets the position of the bot to be at the left-most edge of the map.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"[ARCARUM.SANDBOX] Now determining if bot is starting all the way at the left edge of the Zone...")
        while Game.find_and_click_button("arcarum_sandbox_left_arrow", tries = 1, suppress_error = True):
            Game.wait(1.0)

        MessageLog.print_message(f"[ARCARUM.SANDBOX] Left edge of the Zone has been reached.")

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
            tries = 30
            while tries > 0:
                if Game.find_and_click_button("arcarum_banner", tries = 1) is False:
                    MouseUtils.scroll_screen_from_home_button(-200)
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
            navigation_check = Game.find_and_click_button("arcarum_sandbox_zone_eletio")
        elif Settings.map_name == "Zone Faym":
            navigation_check = Game.find_and_click_button("arcarum_sandbox_zone_faym")
        elif Settings.map_name == "Zone Goliath":
            navigation_check = Game.find_and_click_button("arcarum_sandbox_zone_goliath")
        elif Settings.map_name == "Zone Harbinger":
            navigation_check = Game.find_and_click_button("arcarum_sandbox_zone_harbinger")
        elif Settings.map_name == "Zone Invidia":
            navigation_check = Game.find_and_click_button("arcarum_sandbox_zone_invidia")
        elif Settings.map_name == "Zone Joculator":
            navigation_check = Game.find_and_click_button("arcarum_sandbox_zone_joculator")
        elif Settings.map_name == "Zone Kalendae":
            navigation_check = Game.find_and_click_button("arcarum_sandbox_zone_kalendae")
        elif Settings.map_name == "Zone Liber":
            navigation_check = Game.find_and_click_button("arcarum_sandbox_zone_liber")
        else:
            raise ArcarumSandboxException("Invalid map name provided for Arcarum Replicard Sandbox navigation.")

        if navigation_check is False:
            raise ArcarumSandboxException("Failed to navigate into the Sandbox Zone.")

        Game.wait(2.0)

        # Now that the Zone is on screen, have the bot move all the way to the left side of the map.
        ArcarumSandbox._reset_position()

        # Finally, select the mission.
        ArcarumSandbox._navigate_to_mission()

        return None

    @staticmethod
    def _refill_aap():
        """Refills AAP if necessary.

        Returns:
            None
        """
        if ImageUtils.confirm_location("aap", tries = 10):
            from bot.game import Game

            MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Bot ran out of AAP. Refilling now...")
            use_locations = ImageUtils.find_all("use")
            MouseUtils.move_and_click_point(use_locations[1][0], use_locations[1][1], "use")

            Game.wait(1.0)
            Game.find_and_click_button("ok")
            Game.wait(1.0)

            MessageLog.print_message(f"[ARCARUM.SANDBOX] AAP is now refilled.")

        return None
    
    @staticmethod
    def _play_zone_boss():
        """Clicks on Play if you are fighting a zone boss.

        Returns:
            None
        """
        play_button = ImageUtils.find_button("play")
        if play_button:
            MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Now fighting zone boss...")
            MouseUtils.move_and_click_point(play_button[0], play_button[1], "play")

        return None

    @staticmethod
    def _open_gold_chest():
        """Clicks on a gold chest.
        If it is a mimic, fight it, if not, click ok.

        Returns:
            None
        """
        from bot.game import Game

        action_locations: List[Tuple[int, ...]] = ImageUtils.find_all("arcarum_sandbox_action")
        MouseUtils.move_and_click_point(action_locations[0][0], action_locations[0][1], "arcarum_sandbox_action")
        Game.find_and_click_button("ok")
        Game.wait(3.0)
        if Game.find_and_click_button("ok", suppress_error = True) is False:
            MouseUtils.move_and_click_point(action_locations[0][0], action_locations[0][1], "arcarum_sandbox_action")
            Game.wait(3.0)
            if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
                if CombatMode.start_combat_mode():
                    Game.collect_loot(is_completed = True)
            Game.find_and_click_button("expedition")
                 
        Game.wait(2.0)
        ArcarumSandbox._reset_position()
        ArcarumSandbox._navigate_to_mission()

    @staticmethod
    def start():
        """Starts the process of completing Arcarum Replicard Sandbox missions.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if ArcarumSandbox._first_run:
            ArcarumSandbox._navigate_to_zone()
        elif Game.find_and_click_button("play_again") is False:
            if Game.check_for_pending():
                ArcarumSandbox._first_run = True
                ArcarumSandbox._navigate_to_zone()
            else:
                # If the bot cannot find the "Play Again" button, click the Expedition button.
                Game.find_and_click_button("expedition")

                # Wait out the animations that play, whether it be Treasure or Defender spawning.
                Game.wait(5.0)

                # Click away the Treasure popup if it shows up.
                Game.find_and_click_button("ok", suppress_error = True)
                if Settings.enable_gold_chest and Game.find_and_click_button("arcarum_gold_chest") is True:
                    ArcarumSandbox._open_gold_chest()
                else:
                    # Start the mission again.
                    Game.wait(3.0)
                    ArcarumSandbox._navigate_to_mission(skip_to_action = True)

        # Refill AAP if needed.
        ArcarumSandbox._play_zone_boss()
        ArcarumSandbox._refill_aap()

        Game.wait(3.0)

        if Settings.engaged_defender_battle:
            if Game.find_party_and_start_mission(Settings.defender_group_number, Settings.defender_party_number, bypass_first_run = True):
                if CombatMode.start_combat_mode(is_defender = Settings.engaged_defender_battle):
                    Game.collect_loot(is_completed = True, is_defender = Settings.engaged_defender_battle)
        else:
            if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
                if CombatMode.start_combat_mode():
                    Game.collect_loot(is_completed = True)

        return None
