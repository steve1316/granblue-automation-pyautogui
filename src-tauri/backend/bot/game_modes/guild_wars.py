from typing import Tuple, List

from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class GuildWarsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GuildWars:
    """
    Provides the navigation and any necessary utility functions to handle the Guild Wars game mode.
    """

    @staticmethod
    def _navigate():
        """Navigates to the specified Guild Wars mission.

        Returns:
            None
        """
        from bot.game import Game

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        MessageLog.print_message(f"\n[GUILD.WARS] Now navigating to Guild Wars...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        Game.find_and_click_button("home_menu")
        Game.wait(1.0)
        banner_locations = ImageUtils.find_all("event_banner", custom_confidence = 0.7)
        if len(banner_locations) == 0:
            banner_locations = ImageUtils.find_all("event_banner_blue", custom_confidence = 0.7)

        if Settings.guild_wars_enable_new_position:
            if Settings.guild_wars_new_position > len(banner_locations) - 1:
                raise GuildWarsException("Value set for New Position was found to be invalid compared to the actual number of events found in the Home Menu.")
            MouseUtils.move_and_click_point(banner_locations[Settings.guild_wars_new_position][0], banner_locations[Settings.guild_wars_new_position][1], "event_banner")
        else:
            MouseUtils.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        Game.wait(3.0)

        difficulty = ""
        if Settings.mission_name == "Extreme":
            difficulty = "Extreme"
        elif Settings.mission_name == "Extreme+":
            difficulty = "Extreme+"
        elif Settings.mission_name == "NM90":
            difficulty = "NM90"
        elif Settings.mission_name == "NM95":
            difficulty = "NM95"
        elif Settings.mission_name == "NM100":
            difficulty = "NM100"
        elif Settings.mission_name == "NM150":
            difficulty = "NM150"
        elif Settings.mission_name == "NM200":
            difficulty = "NM200"

        if ImageUtils.confirm_location("guild_wars"):
            # Scroll the screen down a little bit.
            MouseUtils.scroll_screen_from_home_button(-200)

            Game.wait(3.0)

            raid_battle_locations = ImageUtils.find_all("event_raid_battle")

            # Perform different navigation actions based on whether the user wants to farm meat or to farm Nightmares.
            if difficulty == "Extreme" or difficulty == "Extreme+":
                MessageLog.print_message(f"\n[GUILD.WARS] Now proceeding to farm meat.")

                # Click on the banner to farm meat.
                if len(raid_battle_locations) < 3:
                    MouseUtils.move_and_click_point(raid_battle_locations[1][0], raid_battle_locations[1][1], "event_raid_battle")
                else:
                    MouseUtils.move_and_click_point(raid_battle_locations[2][0], raid_battle_locations[2][1], "event_raid_battle")

                Game.wait(3.0)

                if ImageUtils.confirm_location("guild_wars_meat"):
                    # Now click on the specified Mission to start. Also attempt at fixing the deadzone issue by looping.
                    tries = 10
                    MessageLog.print_message(f"[GUILD.WARS] Now hosting {difficulty} now...")

                    ap_locations = ImageUtils.find_all("ap_30")

                    if difficulty == "Extreme":
                        MouseUtils.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap_30")
                    elif difficulty == "Extreme+":
                        MouseUtils.move_and_click_point(ap_locations[1][0], ap_locations[1][1], "ap_30")

                    Game.wait(3.0)

                    while ImageUtils.wait_vanish("ap_30", timeout = 3) is False:
                        if difficulty == "Extreme":
                            MouseUtils.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap_30")
                        elif difficulty == "Extreme+":
                            MouseUtils.move_and_click_point(ap_locations[1][0], ap_locations[1][1], "ap_30")

                        Game.wait(3.0)

                        tries -= 1
                        if tries <= 0:
                            if difficulty == "Extreme+":
                                raise GuildWarsException("You did not unlock Extreme+ yet!")
                            else:
                                raise GuildWarsException("There appears to be a deadzone issue that the bot failed 10 times to resolve. Please refresh the page and try again.")

                    return None
                else:
                    raise GuildWarsException("Failed to open component to host Meat raids in the Guild Wars page.")
            else:
                MessageLog.print_message(f"\n[GUILD.WARS] Now proceeding to farm Nightmares.")

                day_1 = ImageUtils.confirm_location("guild_wars_nightmare_first_day")
                if day_1:
                    # Logic for Day 1. Only NM90 is available.
                    MessageLog.print_message(f"\n[GUILD.WARS] Today is Day 1 so hosting NM90.")
                    Game.find_and_click_button("ok")

                    # Check if the Nightmare selection was successful and put the bot into the Support Summon Selection screen. If not, then go back to farm meat.
                    if not ImageUtils.wait_vanish("ok", timeout = 10):
                        GuildWars._farm_meat(raid_battle_locations)
                elif difficulty == "NM90" or difficulty == "NM95" or difficulty == "NM100":
                    # Logic for Day 2+. NM90, NM95 and NM100 are now available.
                    MessageLog.print_message(f"\n[GUILD.WARS] Today is Day 2+.")
                    if len(raid_battle_locations) < 3:
                        MouseUtils.move_and_click_point(raid_battle_locations[0][0], raid_battle_locations[0][1], "event_raid_battle")
                    else:
                        MouseUtils.move_and_click_point(raid_battle_locations[1][0], raid_battle_locations[1][1], "event_raid_battle")

                    # Select the Nightmare.
                    nightmare_locations = ImageUtils.find_all("guild_wars_nightmares")
                    if difficulty == "NM90":
                        MouseUtils.move_and_click_point(nightmare_locations[0][0], nightmare_locations[0][1], "guild_wars_nightmares")
                    elif difficulty == "NM95":
                        MouseUtils.move_and_click_point(nightmare_locations[1][0], nightmare_locations[1][1], "guild_wars_nightmares")
                    else:
                        MouseUtils.move_and_click_point(nightmare_locations[1][0], nightmare_locations[1][1], "guild_wars_nightmares")

                    # Check if the Nightmare selection was successful and put the bot into the Support Summon Selection screen. If not, then go back to farm meat.
                    if not ImageUtils.wait_vanish("close", timeout = 10):
                        GuildWars._farm_meat(raid_battle_locations)
                elif difficulty == "NM150" or difficulty == "NM200":
                    if len(raid_battle_locations) >= 3:
                        MessageLog.print_message(f"\n[GUILD.WARS] Today is Day 2+ and United Battles (NM150/NM200) may be available.")
                        MouseUtils.move_and_click_point(raid_battle_locations[0][0], raid_battle_locations[0][1], "event_raid_battle")

                        Game.wait(1.0)

                        nightmare_locations = ImageUtils.find_all("guild_wars_nightmares")

                        start_check = False
                        if Game.find_and_click_button("start"):
                            MessageLog.print_message(f"[GUILD.WARS] Scans indicate that NM150 is the only United Battle available.")
                            start_check = True
                        elif len(nightmare_locations) == 0:
                            GuildWars._farm_meat(raid_battle_locations)
                            start_check = True
                        elif difficulty == "NM150":
                            MessageLog.print_message(f"[GUILD.WARS] Now hosting NM150 now...")
                            MouseUtils.move_and_click_point(nightmare_locations[0][0], nightmare_locations[0][1], "guild_wars_nightmares")
                            start_check = ImageUtils.wait_vanish("close", timeout = 10)
                        elif difficulty == "NM200":
                            if len(nightmare_locations) != 2:
                                raise GuildWarsException(f"Was not able to detect the location of NM200 with size of {len(nightmare_locations)}.")

                            MessageLog.print_message(f"[GUILD.WARS] Now hosting NM200 now...")
                            MouseUtils.move_and_click_point(nightmare_locations[1][0], nightmare_locations[1][1], "guild_wars_nightmares")
                            start_check = ImageUtils.wait_vanish("close", timeout = 10)

                        # Check if the Nightmare selection was successful and put the bot into the Support Summon Selection screen. If not, then go back to farm meat.
                        if start_check is False:
                            GuildWars._farm_meat(raid_battle_locations)
                    else:
                        raise GuildWarsException("Scans indicate that United Battles are not available yet.")
        else:
            raise GuildWarsException("Failed to arrive at Guild Wars page.")

        return None

    @staticmethod
    def _farm_meat(locations: List[Tuple[int, ...]]):
        """Begins a run to farm meat from Extreme+.

        Args:
            locations (List[Tuple[int, ...]]): List of the raid locations to go back to.

        Returns:
            None
        """
        from bot.game import Game

        # If there is not enough meat to host, host Extreme+ instead.
        MessageLog.print_message(f"\n[GUILD.WARS] User lacks meat to host the Nightmare. Hosting Extreme+ instead...")

        if Game.find_and_click_button("close") is False or Game.find_and_click_button("cancel") is False:
            raise GuildWarsException("Failed to close popup in order to get back to the list of Guild War raids.")

        # Click on the banner to farm meat.
        if len(locations) < 2:
            MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "event_raid_battle")
        else:
            MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "event_raid_battle")

        Game.wait(1.0)

        if ImageUtils.confirm_location("guild_wars_meat"):
            MessageLog.print_message(f"[GUILD.WARS] Now hosting Extreme+ now...")
            Game.find_and_click_button("guild_wars_meat_extreme+", y_offset = -50)

            # Alert the user if they did not unlock Extreme+ and stop the bot.
            if not ImageUtils.wait_vanish("guild_wars_meat_extreme+", timeout = 30):
                raise GuildWarsException("You did not unlock Extreme+ yet!")
        else:
            raise GuildWarsException("Failed to open component to host Meat raids in the Guild Wars page due to running out of host materials.")

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Guild Wars Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            GuildWars._navigate()
        elif Game.find_and_click_button("play_again"):
            Game.check_for_popups()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            GuildWars._navigate()

        # Check for AP.
        Game.check_for_ap()

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
            if summon_check:
                # Select the Party.
                Game.find_party_and_start_mission(Settings.group_number, Settings.party_number)

                # Now start Combat Mode and detect any item drops.
                if CombatMode.start_combat_mode():
                    Game.collect_loot(is_completed = True)
        else:
            raise GuildWarsException("Failed to arrive at the Summon Selection screen.")

        return None
