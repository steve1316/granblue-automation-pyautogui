from utils.message_log import MessageLog
from utils.settings import Settings
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class ArcarumException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Arcarum:
    """
    Provides the navigation and any necessary utility functions to handle the Arcarum game mode.
    """

    _expedition: str = Settings.mission_name
    _first_run: bool = True
    _encountered_boss: bool = False

    @staticmethod
    def _navigate_to_map() -> bool:
        """Navigates to the specified Arcarum expedition.

        Returns:
            (bool): True if the bot was able to start/resume the expedition. False otherwise.
        """
        from bot.game import Game

        if Arcarum._first_run:
            MessageLog.print_message(f"\n[ARCARUM] Now beginning navigation to {Arcarum._expedition}.")
            Game.go_back_home()

            # Navigate to the Arcarum banner.
            tries = 30
            while tries > 0:
                if Game.find_and_click_button("arcarum_banner", tries = 1) is False:
                    MouseUtils.scroll_screen_from_home_button(-200)
                    tries -= 1
                    if tries <= 0:
                        raise ArcarumException("Failed to navigate to Arcarum from the Home screen.")
                else:
                    break

            Arcarum._first_run = False
        else:
            Game.wait(4)

        # Now make sure that the Extreme difficulty is selected.
        Game.wait(1)

        # Check if bot is at Replicard Sandbox.
        if ImageUtils.confirm_location("arcarum_sandbox"):
            Game.find_and_click_button("arcarum_head_back")
            Game.wait(1.0)

        # Confirm the completion popup if it shows up.
        if ImageUtils.confirm_location("arcarum_expedition"):
            Game.find_and_click_button("ok")

        Game.find_and_click_button("arcarum_extreme")

        # Finally, navigate to the specified map to start it.
        MessageLog.print_message(f"[ARCARUM] Now starting the specified expedition: {Arcarum._expedition}.")
        formatted_map_name = Arcarum._expedition.lower().replace(" ", "_")

        if Game.find_and_click_button(f"arcarum_{formatted_map_name}", tries = 10) is False:
            # Resume the expedition if it is already in-progress.
            Game.find_and_click_button("arcarum_exploring")
        elif ImageUtils.confirm_location("arcarum_departure_check"):
            MessageLog.print_message(f"[ARCARUM] Now using 1 Arcarum ticket to start this expedition...")
            result_check = Game.find_and_click_button("start_expedition")
            Game.wait(6)
            return result_check
        elif Game.find_and_click_button("resume"):
            Game.wait(3)
            return True
        else:
            raise ArcarumException("Failed to encounter the Departure Check to confirm starting the expedition.")

    @staticmethod
    def _choose_action() -> str:
        """Chooses the next action to take for the current Arcarum expedition.

        Returns:
            (str): The action to take next.
        """
        from bot.game import Game

        # Wait a second in case the "Do or Die" animation plays.
        Game.wait(2.0)

        # Determine what action to take.
        tries = 3
        while tries > 0:
            MessageLog.print_message(f"\n[ARCARUM] Now determining what action to take with {tries} tries remaining...")

            # Prioritise any enemies/chests/thorns that are available on the current node.
            arcarum_actions = ImageUtils.find_all("arcarum_action")
            if len(arcarum_actions) > 0:
                MouseUtils.move_and_click_point(arcarum_actions[0][0], arcarum_actions[0][1], "arcarum_action")

                Game.wait(2)

                Game.check_for_captcha()

                if ImageUtils.confirm_location("arcarum_party_selection", tries = 3, bypass_general_adjustment = True):
                    return "Combat"
                elif Game.find_and_click_button("ok", tries = 3, bypass_general_adjustment = True):
                    return "Claimed Treasure/Keythorn"
                else:
                    return "Claimed Spirethorn/No Action"

            # Clear any detected Treasure popup after claiming a chest.
            MessageLog.print_message(f"[ARCARUM] No action found for the current node. Looking for Treasure popup...")
            if ImageUtils.confirm_location("arcarum_treasure", tries = 3, bypass_general_adjustment = True):
                Game.find_and_click_button("ok")
                return "Claimed Treasure"

            # Next, determine if there is a available node to move to. Any bound monsters should have been destroyed by now.
            MessageLog.print_message(f"[ARCARUM] No Treasure popup detected. Looking for an available node to move to...")
            if Game.find_and_click_button("arcarum_node", tries = 3, bypass_general_adjustment = True):
                Game.wait(1)
                return "Navigating"

            # Check if a Arcarum boss has appeared. This is after checking for available actions and before searching for a node to move to avoid false positives.
            if Arcarum._check_for_boss():
                return "Boss Detected"

            # Next, attempt to navigate to a node that is occupied by mob(s).
            MessageLog.print_message(f"[ARCARUM] No available node to move to. Looking for nodes with mobs on them...")
            if Game.find_and_click_button("arcarum_mob", tries = 3, bypass_general_adjustment = True) or Game.find_and_click_button("arcarum_red_mob", tries = 3, bypass_general_adjustment = True):
                Game.wait(1)
                return "Navigating"

            # If all else fails, see if there are any unclaimed chests, like the ones spawned by a random special event that spawns chests on all nodes.
            MessageLog.print_message(f"[ARCARUM] No nodes with mobs on them. Looking for nodes with chests on them...")
            if Game.find_and_click_button("arcarum_silver_chest", tries = 3, bypass_general_adjustment = True) or \
                    Game.find_and_click_button("arcarum_gold_chest", tries = 3, bypass_general_adjustment = True):
                Game.wait(1)
                return "Navigating"

            tries -= 1

        MessageLog.print_message(f"[ARCARUM] No action can be taken. Defaulting to moving to the next area.")
        return "Next Area"

    @staticmethod
    def _check_for_boss() -> bool:
        """Checks for the existence of 3-3, 6-3 or 9-3 boss if user settings enabled it.

        Returns:
            (bool): Flag on whether or not a Boss was detected.
        """
        if Settings.enable_stop_on_arcarum_boss:
            MessageLog.print_message(f"\n[ARCARUM] Checking if boss is available...")

            if ImageUtils.find_button("arcarum_boss", tries = 3, bypass_general_adjustment = True) or ImageUtils.find_button("arcarum_boss2", tries = 3, bypass_general_adjustment = True):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def start():
        """Starts the process of completing Arcarum expeditions.

        Returns:
            None
        """
        from bot.game import Game

        runs_completed = 0
        while runs_completed < Settings.item_amount_to_farm:
            Arcarum._navigate_to_map()

            while True:
                action = Arcarum._choose_action()
                MessageLog.print_message(f"[ARCARUM] Action to take will be: {action}")

                if action == "Combat":
                    # Start Combat Mode.
                    if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
                        if ImageUtils.confirm_location("elemental_damage"):
                            raise ArcarumException(
                                "Encountered an important mob for Arcarum and the selected party does not conform to the enemy's weakness. Perhaps you would like to do this battle yourself?")
                        elif ImageUtils.confirm_location("arcarum_restriction"):
                            raise ArcarumException("Encountered a party restriction for Arcarum. Perhaps you would like to complete this section by yourself?")

                        if CombatMode.start_combat_mode():
                            Game.collect_loot(is_completed = False, skip_info = True)
                            Game.find_and_click_button("expedition")
                elif action == "Navigating":
                    # Move to the next available node.
                    Game.find_and_click_button("move")
                elif action == "Next Area":
                    # Either navigate to the next area or confirm the expedition's conclusion.
                    if Game.find_and_click_button("arcarum_next_stage"):
                        Game.find_and_click_button("ok")
                        MessageLog.print_message(f"[ARCARUM] Moving to the next area...")
                    elif Game.find_and_click_button("arcarum_checkpoint"):
                        Game.find_and_click_button("arcarum")
                        MessageLog.print_message(f"[ARCARUM] Expedition is complete.")
                        runs_completed += 1

                        Game.wait(1)
                        Game.check_for_skyscope()
                        break
                elif action == "Boss Detected":
                    MessageLog.print_message(f"[ARCARUM] Boss has been detected. Stopping the bot.")
                    raise ArcarumException("Boss has been detected. Stopping the bot.")

        return None
