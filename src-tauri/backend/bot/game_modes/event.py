from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class EventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Event:
    """
    Provides the navigation and any necessary utility functions to handle the Event or Event (Token Drawboxes) game mode.
    """

    @staticmethod
    def check_for_event_nightmare():
        """Checks for Event Nightmare and if it appears and the user enabled it in user settings, start it.

        Returns:
            (bool): Return True if Event Nightmare was detected and successfully completed. Otherwise, return False.
        """
        from bot.game import Game

        if Settings.enable_nightmare and ImageUtils.find_button("event_claim_loot"):
            # First check if the Event Nightmare is skippable.
            event_claim_loot_location = ImageUtils.find_button("event_claim_loot", suppress_error = True)
            if event_claim_loot_location is not None:
                MessageLog.print_message("\n[EVENT] Skippable Event Nightmare detected. Claiming it now...")
                MouseUtils.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                Game.collect_loot(is_completed = False, is_event_nightmare = True)
                return True
            else:
                MessageLog.print_message("\n[EVENT] Detected Event Nightmare. Starting it now...")

                MessageLog.print_message("\n********************************************************************************")
                MessageLog.print_message("********************************************************************************")
                MessageLog.print_message(f"[EVENT] Event Nightmare")
                MessageLog.print_message(f"[EVENT] Event Nightmare Summon Elements: {Settings.nightmare_summon_elements_list}")
                MessageLog.print_message(f"[EVENT] Event Nightmare Summons: {Settings.nightmare_summon_list}")
                MessageLog.print_message(f"[EVENT] Event Nightmare Group Number: {Settings.nightmare_group_number}")
                MessageLog.print_message(f"[EVENT] Event Nightmare Party Number: {Settings.nightmare_party_number}")
                MessageLog.print_message(f"[EVENT] Event Nightmare Combat Script: {Settings.nightmare_combat_script_name}")
                MessageLog.print_message("********************************************************************************")
                MessageLog.print_message("********************************************************************************\n")

                # Click the "Play Next" button to head to the Summon Selection screen.
                Game.find_and_click_button("play_next")

                Game.wait(1)

                # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
                if ImageUtils.confirm_location("select_a_summon", tries = 30):
                    Game.select_summon(Settings.nightmare_summon_list, Settings.nightmare_summon_elements_list)
                    start_check = Game.find_party_and_start_mission(int(Settings.nightmare_group_number), int(Settings.nightmare_party_number), bypass_first_run = True)

                    # Once preparations are completed, start Combat Mode.
                    if start_check and CombatMode.start_combat_mode(is_nightmare = True):
                        Game.collect_loot(is_completed = False, is_event_nightmare = True)
                        return True

        elif not Settings.enable_nightmare and ImageUtils.find_button("event_claim_loot"):
            # First check if the Event Nightmare is skippable.
            event_claim_loot_location = ImageUtils.find_button("event_claim_loot", suppress_error = True)
            if event_claim_loot_location is not None:
                MessageLog.print_message("\n[EVENT] Skippable Event Nightmare detected but user opted to not run it. Claiming it regardless...")
                MouseUtils.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                Game.collect_loot(is_completed = False, is_event_nightmare = True)
                return True
            else:
                MessageLog.print_message("\n[EVENT] Event Nightmare detected but user opted to not run it. Moving on...")
                Game.find_and_click_button("close")
        else:
            MessageLog.print_message("\n[EVENT] No Event Nightmare detected. Moving on...")

        return False

    @staticmethod
    def _navigate_token_drawboxes():
        """Navigates to the specified Event (Token Drawboxes) mission.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"[EVENT.TOKEN.DRAWBOXES] Now beginning process to navigate to the mission: {Settings.mission_name}...")

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        Game.find_and_click_button("home_menu")
        Game.wait(1.0)
        banner_locations = ImageUtils.find_all("event_banner", custom_confidence = 0.7)
        if len(banner_locations) == 0:
            banner_locations = ImageUtils.find_all("event_banner_blue", custom_confidence = 0.7)
            if len(banner_locations) == 0:
                raise EventException("Failed to find the Event banner.")

        if Settings.event_enable_new_position:
            if Settings.event_new_position > len(banner_locations) - 1:
                raise EventException("Value set for New Position was found to be invalid compared to the actual number of events found in the Home Menu.")
            MouseUtils.move_and_click_point(banner_locations[Settings.event_new_position][0], banner_locations[Settings.event_new_position][1], "event_banner")
        else:
            MouseUtils.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")

        Game.wait(3.0)

        # Check and click away the "Daily Missions" popup.
        if ImageUtils.confirm_location("event_daily_missions", tries = 3):
            MessageLog.print_message(f"\n[EVENT.TOKEN.DRAWBOXES] Detected \"Daily Missions\" popup. Clicking it away...")
            Game.find_and_click_button("close")

        # Remove the difficulty prefix from the mission name.
        difficulty = ""
        formatted_mission_name = ""
        if Settings.mission_name.find("VH ") == 0:
            difficulty = "Very Hard"
            formatted_mission_name = Settings.mission_name[3:]
        elif Settings.mission_name.find("EX ") == 0:
            difficulty = "Extreme"
            formatted_mission_name = Settings.mission_name[3:]
        elif Settings.mission_name.find("EX+ ") == 0:
            difficulty = "Extreme+"
            formatted_mission_name = Settings.mission_name[4:]
        elif Settings.mission_name.find("IM ") == 0:
            difficulty = "Impossible"
            formatted_mission_name = Settings.mission_name[3:]

        # Scroll down the screen a little bit for this UI layout that has Token Drawboxes.
        MouseUtils.scroll_screen_from_home_button(-200)

        if formatted_mission_name == "Event Quest":
            MessageLog.print_message(f"[EVENT.TOKEN.DRAWBOXES] Now hosting Event Quest...")
            if Game.find_and_click_button("event_quests") is False:
                raise EventException("Failed to proceed any further in Event (Token Drawboxes) navigation by missing the Event Quests button.")

            Game.wait(1)

            # Find all the round "Play" buttons.
            quest_play_locations = ImageUtils.find_all("play_round_button")

            # Only Extreme and Extreme+ difficulty is supported for farming efficiency.
            if difficulty == "Extreme":
                MouseUtils.move_and_click_point(quest_play_locations[3][0], quest_play_locations[3][1], "play_round_button")
            elif difficulty == "Extreme+":
                MouseUtils.move_and_click_point(quest_play_locations[4][0], quest_play_locations[4][1], "play_round_button")
        elif formatted_mission_name == "Event Raid":
            # Bring up the "Raid Battle" popup. Then scroll down the screen a bit for screens less than 1440p to see the entire popup.
            MessageLog.print_message(f"[EVENT.TOKEN.DRAWBOXES] Now hosting Event Raid...")
            if not Game.find_and_click_button("event_raid_battle"):
                raise EventException("Failed to detect Token Drawbox layout for this Event. Are you sure this Event has Token Drawboxes? If not, switch to \"Event\" Farming Mode.")
            MouseUtils.scroll_screen_from_home_button(-200)

            Game.wait(1)

            # Select the first category if the raids are split into two sections.
            categories = ImageUtils.find_all("event_raid_category")
            if len(categories) > 0:
                if Settings.enable_select_bottom_category is False:
                    MouseUtils.move_and_click_point(categories[0][0] - 50, categories[0][1], "event_raid_category")
                else:
                    MouseUtils.move_and_click_point(categories[1][0] - 50, categories[1][1], "event_raid_category")

            ap_locations = ImageUtils.find_all("ap")

            if difficulty == "Very Hard":
                MouseUtils.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
                if not ImageUtils.wait_vanish("close", timeout = 10):
                    MouseUtils.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
                else:
                    return None
            elif difficulty == "Extreme":
                MouseUtils.move_and_click_point(ap_locations[1][0], ap_locations[1][1], "ap")
                if not ImageUtils.wait_vanish("close", timeout = 10):
                    MouseUtils.move_and_click_point(ap_locations[1][0], ap_locations[1][1], "ap")
                else:
                    return None
            elif difficulty == "Impossible":
                MouseUtils.move_and_click_point(ap_locations[2][0], ap_locations[2][1], "ap")
                if not ImageUtils.wait_vanish("close", timeout = 10):
                    MouseUtils.move_and_click_point(ap_locations[2][0], ap_locations[2][1], "ap")
                else:
                    return None

            # If the user does not have enough Treasures to host a Extreme or an Impossible Raid, host a Very Hard Raid instead.
            MessageLog.print_message(f"[EVENT.TOKEN.DRAWBOXES] Not enough materials to host {difficulty}. Hosting Very Hard instead...")
            MouseUtils.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")
            if not ImageUtils.wait_vanish("close", timeout = 10):
                MouseUtils.move_and_click_point(ap_locations[0][0], ap_locations[0][1], "ap")

        return None

    @staticmethod
    def _navigate():
        """Navigates to the specified Event mission.

        Returns:
            None
        """
        from bot.game import Game

        # Switch over to the navigation logic for Event (Token Drawboxes) if needed.
        if Settings.farming_mode == "Event (Token Drawboxes)":
            Event._navigate_token_drawboxes()
        else:
            MessageLog.print_message(f"[EVENT] Now beginning process to navigate to the mission: {Settings.mission_name}...")

            # Go to the Home screen.
            Game.go_back_home(confirm_location_check = True)

            Game.find_and_click_button("quest")

            Game.wait(3.0)

            # Check for the "You retreated from the raid battle" popup.
            if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
                Game.find_and_click_button("ok")

            # Go to the Special screen.
            Game.find_and_click_button("special")
            Game.wait(3.0)

            Game.find_and_click_button("special_event")

            # Remove the difficulty prefix from the mission name.
            difficulty = ""
            formatted_mission_name = ""
            if Settings.mission_name.find("N ") == 0:
                difficulty = "Normal"
                formatted_mission_name = Settings.mission_name[2:]
            elif Settings.mission_name.find("H ") == 0:
                difficulty = "Hard"
                formatted_mission_name = Settings.mission_name[2:]
            elif Settings.mission_name.find("VH ") == 0:
                difficulty = "Very Hard"
                formatted_mission_name = Settings.mission_name[3:]
            elif Settings.mission_name.find("EX ") == 0:
                difficulty = "Extreme"
                formatted_mission_name = Settings.mission_name[3:]
            elif Settings.mission_name.find("EX+ ") == 0:
                difficulty = "Extreme+"
                formatted_mission_name = Settings.mission_name[4:]

            if ImageUtils.confirm_location("special"):
                # Check to see if the user already has a Nightmare available.
                nightmare_is_available = 0
                if ImageUtils.find_button("event_nightmare") is not None:
                    nightmare_is_available = 1

                # Find all the "Select" buttons.
                select_button_locations = ImageUtils.find_all("select")
                if Settings.enable_event_location_incrementation_by_one:
                    position = 1
                else:
                    position = 0

                # Select the Event Quest or Event Raid. Additionally, offset the locations by 1 if there is a Nightmare available.
                try:
                    if formatted_mission_name == "Event Quest":
                        MessageLog.print_message(f"[EVENT] Now hosting Event Quest...")
                        MouseUtils.move_and_click_point(select_button_locations[position + nightmare_is_available][0], select_button_locations[position + nightmare_is_available][1], "select")
                    elif formatted_mission_name == "Event Raid":
                        MessageLog.print_message(f"[EVENT] Now hosting Event Raid...")
                        MouseUtils.move_and_click_point(select_button_locations[(position + 1) + nightmare_is_available][0], select_button_locations[(position + 1) + nightmare_is_available][1],
                                                        "play_round_button")
                except IndexError as e:
                    MessageLog.print_message(f"\n[ERROR] Turn on/off the 'Enable Incrementation of Location by 1' and try again.")
                    raise IndexError(e)

                Game.wait(1)

                # Find all the round "Play" buttons.
                round_play_button_locations = ImageUtils.find_all("play_round_button")

                # If Extreme+ was selected and only 3 locations were found for the play_round_button, that means Extreme+ is not available.
                if len(round_play_button_locations) == 3 and difficulty == "Extreme+":
                    MessageLog.print_message(f"[EVENT] Extreme+ was selected but it seems it is not available. Defaulting to Extreme difficulty...")
                    difficulty = "Extreme"

                # Now select the chosen difficulty.
                if difficulty == "Very Hard":
                    MouseUtils.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "play_round_button")
                elif difficulty == "Extreme":
                    MouseUtils.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "play_round_button")
                elif difficulty == "Extreme+":
                    MouseUtils.move_and_click_point(round_play_button_locations[2][0], round_play_button_locations[2][1], "play_round_button")
            else:
                raise EventException("Failed to arrive at the Special Quest screen.")

        return None

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Event or Event (Token Drawboxes) Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            Event._navigate()
        elif Game.find_and_click_button("play_again"):
            if Game.check_for_popups():
                Event._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            Event._navigate()

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
            raise EventException("Failed to arrive at the Summon Selection screen.")

        return None
