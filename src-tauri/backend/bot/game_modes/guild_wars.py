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
                                ImageUtils.generate_alert("You did not unlock Extreme+ yet!")
                                raise GuildWarsException("You did not unlock Extreme+ yet!")
                            else:
                                raise GuildWarsException("There appears to be a deadzone issue that the bot failed 10 times to resolve. Please refresh the page and try again.")

                    return None
                else:
                    raise GuildWarsException("Failed to open component to host Meat raids in the Guild Wars page.")
            else:
                MessageLog.print_message(f"\n[GUILD.WARS] Now proceeding to farm Nightmares.")

                start_check_for_nm150_nm200 = False

                # Click on the banner to farm Nightmares.
                if difficulty != "NM150" or difficulty != "NM200":
                    if len(raid_battle_locations) < 3:
                        MouseUtils.move_and_click_point(raid_battle_locations[0][0], raid_battle_locations[0][1], "event_raid_battle")
                    else:
                        MouseUtils.move_and_click_point(raid_battle_locations[1][0], raid_battle_locations[1][1], "event_raid_battle")

                    nightmare_locations = ImageUtils.find_all("guild_wars_nightmares")

                    # If today is the first/second day of Guild Wars, only NM90 will be available.
                    if ImageUtils.confirm_location("guild_wars_nightmare_first_day"):
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
                    MessageLog.print_message(f"\n[GUILD.WARS] Now hosting NM150/NM200 now...")

                    if len(raid_battle_locations) >= 3:
                        MouseUtils.move_and_click_point(raid_battle_locations[0][0], raid_battle_locations[0][1], "event_raid_battle")

                        if not ImageUtils.wait_vanish("guild_wars_nightmare_united_battle", timeout = 10):
                            Game.find_and_click_button("guild_wars_nightmare_united_battle")

                        nightmare_locations = ImageUtils.find_all("guild_wars_nightmares")

                        if ImageUtils.confirm_location("guild_wars_nightmare"):
                            start_check_for_nm150_nm200 = Game.find_and_click_button("start")
                        elif difficulty == "NM150":
                            MessageLog.print_message(f"[GUILD.WARS] Now hosting NM150 now...")
                            MouseUtils.move_and_click_point(nightmare_locations[0][0], nightmare_locations[0][1], "guild_wars_nightmares")
                            start_check_for_nm150_nm200 = True
                        elif difficulty == "NM200":
                            MessageLog.print_message(f"[GUILD.WARS] Now hosting NM200 now...")
                            MouseUtils.move_and_click_point(nightmare_locations[1][0], nightmare_locations[1][1], "guild_wars_nightmares")
                            start_check_for_nm150_nm200 = True

                if start_check_for_nm150_nm200 is False:
                    # If there is not enough meat to host, host Extreme+ instead.
                    MessageLog.print_message(f"\n[GUILD.WARS] User lacks meat or navigation failed to host the Nightmare. Hosting Extreme+ instead...")

                    if difficulty != "NM150":
                        Game.find_and_click_button("close")
                    else:
                        Game.find_and_click_button("cancel")

                    # Click on the banner to farm meat.
                    if len(raid_battle_locations) < 2:
                        MouseUtils.move_and_click_point(raid_battle_locations[1][0], raid_battle_locations[1][1], "event_raid_battle")
                    else:
                        MouseUtils.move_and_click_point(raid_battle_locations[2][0], raid_battle_locations[2][1], "event_raid_battle")

                    if ImageUtils.confirm_location("guild_wars_meat"):
                        MessageLog.print_message(f"[GUILD.WARS] Now hosting Extreme+ now...")
                        Game.find_and_click_button("guild_wars_meat_extreme+")

                        # Alert the user if they did not unlock Extreme+ and stop the bot.
                        if not ImageUtils.wait_vanish("guild_wars_meat_extreme+", timeout = 30):
                            ImageUtils.generate_alert("You did not unlock Extreme+ yet!")
                            raise GuildWarsException("You did not unlock Extreme+ yet!")
                    else:
                        GuildWarsException("Failed to open component to host Meat raids in the Guild Wars page due to running out of host materials.")
        else:
            raise GuildWarsException("Failed to arrive at Guild Wars page.")

        return None

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
