from utils.message_log import MessageLog
from utils.settings import Settings
from utils.image_utils import ImageUtils
from bot.combat_mode import CombatMode


class GenericException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Generic:
    """
    Provides any lightweight utility functions necessary to repeat a setup that supports the "Play Again" logic.
    """

    @staticmethod
    def start():
        """Starts the process of completing a generic setup that supports the 'Play Again' logic.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[GENERIC] Now checking for run eligibility...")

        # Bot can start either at the Combat screen with the "Attack" button visible, the Loot Collection screen with the "Play Again" button visible, or the Coop Room screen.
        if ImageUtils.find_button("attack", tries = 10):
            MessageLog.print_message(f"[GENERIC] Bot is at the Combat screen. Starting Combat Mode now...")
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)
        elif Game.find_and_click_button("coop_start", tries = 10):
            MessageLog.print_message(f"[GENERIC] Bot is at the Coop Room screen. Starting the Coop mission and Combat Mode now...")

            Game.wait(3.0)

            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)

                # Head back to the Coop Room.
                Game.find_and_click_button("coop_room")

                # Check for "Daily Missions" popup for Coop.
                if ImageUtils.confirm_location("coop_daily_missions"):
                    Game.find_and_click_button("close")
        else:
            MessageLog.print_message(f"[GENERIC] Bot is not at the Combat or Coop Room screen. Checking for the Loot Collection screen now...")

            # Press the "Play Again" button if necessary, otherwise start Combat Mode.
            if Game.find_and_click_button("play_again"):
                Game.check_for_popups()
            else:
                raise GenericException(
                    "Failed to detect the 'Play Again' button. Bot can start either at the Combat screen with the 'Attack' button visible, the Loot Collection screen with the 'Play Again' " +
                    "button visible, or the Coop Room screen with the 'Start' button visible with the party already selected...")

            # Check for AP.
            Game.check_for_ap()

            # Check if the bot is at the Summon Selection screen.
            if ImageUtils.confirm_location("select_a_summon", tries = 30):
                summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
                if summon_check:
                    # Do not select party and just commence the mission.
                    MessageLog.print_message(f"[GENERIC] Skipping party selection and immediately commencing mission...")
                    if Game.find_and_click_button("ok", tries = 30):
                        # Close the "Item Picked Up" popup.
                        Game.wait(1.0)
                        if ImageUtils.confirm_location("items_picked_up", tries = 10):
                            Game.find_and_click_button("ok")

                        # Now start Combat Mode and detect any item drops.
                        if CombatMode.start_combat_mode():
                            Game.collect_loot(is_completed = True)
                    else:
                        raise GenericException("Failed to skip party selection.")
            else:
                raise GenericException("Failed to arrive at the Summon Selection screen.")

        return None
