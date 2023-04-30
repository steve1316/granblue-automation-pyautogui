from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class RaidException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Raid:
    """
    Provides the navigation and any necessary utility functions to handle the Raid game mode.
    """

    _raids_joined = 0

    @staticmethod
    def _check_for_joined_raids():
        """Check and update the number of raids currently joined.

        Returns:
            None
        """
        # TODO: Make sure Recent tab is active.

        # Find out the number of currently joined raids.
        joined_locations = ImageUtils.find_all("joined")

        if joined_locations is not None:
            Raid._raids_joined = len(joined_locations)
            MessageLog.print_message(f"\n[RAID] There are currently {Raid._raids_joined} raids joined.")

        return None

    @staticmethod
    def _clear_joined_raids():
        """Begin process to wait out the joined raids if there are 3 or more currently active.

        Returns:
            None
        """
        from bot.game import Game

        # If the maximum number of raids has been joined, collect any pending rewards with a interval of 30 seconds in between until the number of joined raids is below 3.
        while Raid._raids_joined >= 3:
            MessageLog.print_message(f"\n[RAID] Maximum raids of 3 has been joined. Waiting 30 seconds to see if any finish.")
            Game.wait(30)

            Game.go_back_home(confirm_location_check = True)
            Game.find_and_click_button("quest")

            if Game.check_for_pending():
                Game.find_and_click_button("quest")
                Game.wait(3.0)

            Game.find_and_click_button("raid")
            Game.wait(3.0)
            Raid._check_for_joined_raids()

        return None

    @staticmethod
    def _join_raid() -> bool:
        """Start the process to fetch a valid room code and join it.

        Returns:
            (bool): True if the bot arrived at the Summon Selection screen.
        """
        from bot.game import Game

        recovery_time = 15

        # TODO: replace with raid finder in-game.

    @staticmethod
    def _navigate():
        """Navigates to the specified Raid.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[RAID] Beginning process to navigate to the raid: {Settings.mission_name}...")

        # Head to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        # Then navigate to the Quest screen.
        Game.find_and_click_button("quest")

        Game.wait(3.0)

        # Check for the "You retreated from the raid battle" popup.
        if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
            Game.find_and_click_button("ok")

        # Check for any Pending Battles popup.
        if Game.check_for_pending():
            Game.find_and_click_button("quest")

        # Now navigate to the Raid screen.
        Game.find_and_click_button("raid")

        if ImageUtils.confirm_location("raid"):
            # Check for any joined raids and if the max number of raids joined was reached, clear them.
            Raid._check_for_joined_raids()
            Raid._clear_joined_raids()

            # Click on the "Enter ID" button and then start the process to join a raid.
            MessageLog.print_message(f"\n[RAID] Now moving to the \"Enter ID\" screen.")
            if Game.find_and_click_button("enter_id"):
                Raid._join_raid()
        else:
            raise RaidException("Failed to reach the Backup Requests screen.")

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Raid Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            Raid._navigate()
        else:
            # Check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            Raid._navigate()

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)

            if summon_check:
                # Select the Party.
                if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
                    # Handle the rare case where joining the Raid after selecting the Summon and Party led the bot to the Quest Results screen with no loot to collect.
                    if ImageUtils.confirm_location("no_loot", disable_adjustment = True):
                        MessageLog.print_message("\n[RAID] Seems that the Raid just ended. Moving back to the Home screen and joining another Raid...")
                    elif CombatMode.start_combat_mode():
                        Game.collect_loot(is_completed = True)
                else:
                    MessageLog.print_message("\n[RAID] Seems that the Raid ended before the bot was able to join. Now looking for another Raid to join...")
        else:
            raise RaidException("Failed to arrive at the Summon Selection screen.")

        return None
