import random

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
        banner_locations = ImageUtils.find_all("event_banner", custom_confidence = 0.7)
        if len(banner_locations) == 0:
            banner_locations = ImageUtils.find_all("event_banner_blue", custom_confidence = 0.7)
        MouseUtils.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        Game.wait(1.0)

        difficulty = ""
        if Settings.mission_name == "Very Hard":
            difficulty = "Very Hard"
        elif Settings.mission_name == "Extreme":
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

        if ImageUtils.confirm_location("guild_wars"):
            # Scroll the screen down a little bit.
            MouseUtils.scroll_screen_from_home_button(-200)

            Game.wait(1.0)

            # Perform different navigation actions based on whether the user wants to farm meat or to farm Nightmares.
            if difficulty == "Very Hard" or difficulty == "Extreme" or difficulty == "Extreme+":
                MessageLog.print_message(f"\n[GUILD.WARS] Now proceeding to farm meat.")

                # Click on the banner to farm meat.
                Game.find_and_click_button("guild_wars_meat")

                Game.wait(1.0)

                if ImageUtils.confirm_location("guild_wars_meat"):
                    # Now click on the specified Mission to start. Also attempt at fixing the deadzone issue by looping.
                    formatted_mission_name = difficulty.replace(" ", "_")
                    tries = 10
                    MessageLog.print_message(f"[GUILD.WARS] Now hosting {difficulty} now...")
                    while ImageUtils.wait_vanish("ap_30", timeout = 1) is False:
                        Game.find_and_click_button(f"guild_wars_meat_{formatted_mission_name}", x_offset = random.randrange(-30, 30), y_offset = random.randrange(-60, -40))

                        Game.wait(3)

                        tries -= 1
                        if tries <= 0:
                            if difficulty == "Extreme+":
                                ImageUtils.generate_alert("You did not unlock Extreme+ yet!")
                                raise GuildWarsException("You did not unlock Extreme+ yet!")
                            else:
                                raise GuildWarsException("There appears to be a deadzone issue that the bot failed 10 times to resolve. Please refresh the page and try again.")

                    return None
            else:
                MessageLog.print_message(f"\n[GUILD.WARS] Now proceeding to farm Nightmares.")

                # Click on the banner to farm Nightmares.
                if difficulty != "NM150":
                    Game.find_and_click_button("guild_wars_nightmare")
                    if not ImageUtils.wait_vanish("guild_wars_nightmare", timeout = 10):
                        Game.find_and_click_button("guild_wars_nightmare")
                else:
                    MessageLog.print_message(f"\n[GUILD.WARS] Now hosting NM150 now...")
                    Game.find_and_click_button("guild_wars_nightmare_150")
                    if not ImageUtils.wait_vanish("guild_wars_nightmare_150", timeout = 10):
                        Game.find_and_click_button("guild_wars_nightmare_150")

                    if ImageUtils.confirm_location("guild_wars_nightmare"):
                        Game.find_and_click_button("start")

                if difficulty != "NM150" and ImageUtils.confirm_location("guild_wars_nightmare"):
                    nightmare_locations = ImageUtils.find_all("guild_wars_nightmares")

                    # If today is the first/second day of Guild Wars, only NM90 will be available.
                    if ImageUtils.confirm_location("guild_wars_nightmare_first_day", tries = 3):
                        MessageLog.print_message(f"[GUILD.WARS] Today is the first/second day so hosting NM90.")
                        Game.find_and_click_button("ok")

                        # Alert the user if they lack the meat to host this and stop the bot.
                        if not ImageUtils.wait_vanish("ok", timeout = 30):
                            ImageUtils.generate_alert("You do not have enough meat to host this NM90!")
                            raise GuildWarsException("You do not have enough meat to host this NM90!")

                    # If it is not the first/second day of Guild Wars, that means that other difficulties are now available.
                    elif difficulty == "NM90":
                        MessageLog.print_message(f"[GUILD.WARS] Now hosting NM90 now...")
                        MouseUtils.move_and_click_point(nightmare_locations[0][0], nightmare_locations[0][1], "guild_wars_nightmares")
                    elif difficulty == "NM95":
                        MessageLog.print_message(f"[GUILD.WARS] Now hosting NM95 now...")
                        MouseUtils.move_and_click_point(nightmare_locations[1][0], nightmare_locations[1][1], "guild_wars_nightmares")
                    elif difficulty == "NM100":
                        MessageLog.print_message(f"[GUILD.WARS] Now hosting NM100 now...")
                        MouseUtils.move_and_click_point(nightmare_locations[2][0], nightmare_locations[2][1], "guild_wars_nightmares")

                else:
                    # If there is not enough meat to host, host Extreme+ instead.
                    MessageLog.print_message(f"\n[GUILD.WARS] User lacks meat to host the Nightmare. Hosting Extreme+ instead...")

                    if difficulty != "NM150":
                        Game.find_and_click_button("close")
                    else:
                        Game.find_and_click_button("cancel")

                    # Click on the banner to farm meat.
                    Game.find_and_click_button("guild_wars_meat")

                    if ImageUtils.confirm_location("guild_wars_meat"):
                        MessageLog.print_message(f"[GUILD.WARS] Now hosting Extreme+ now...")
                        Game.find_and_click_button("guild_wars_meat_extreme+")

                        # Alert the user if they did not unlock Extreme+ and stop the bot.
                        if not ImageUtils.wait_vanish("guild_wars_meat_extreme+", timeout = 30):
                            ImageUtils.generate_alert("You did not unlock Extreme+ yet!")
                            raise GuildWarsException("You did not unlock Extreme+ yet!")

        return None

    @staticmethod
    def start(first_run: bool) -> int:
        """Starts the process to complete a run for Guild Wars Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            (int): Number of runs completed.
        """
        from bot.game import Game

        runs_completed: int = 0

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
                    runs_completed = Game.collect_loot(is_completed = True)
        else:
            raise GuildWarsException("Failed to arrive at the Summon Selection screen.")

        return runs_completed
