import multiprocessing
import random
import time
import traceback
from typing import List

import pyautogui

# The order of the following imports matter to avoid circular import error.
from utils.settings import Settings
from utils.message_log import MessageLog
from utils import discord_utils
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from utils.twitter_room_finder import TwitterRoomFinder
# Imports for all the supported game modes.
from bot.game_modes.arcarum import Arcarum
from bot.game_modes.arcarum_sandbox import ArcarumSandbox
from bot.game_modes.coop import Coop
from bot.game_modes.dread_barrage import DreadBarrage
from bot.game_modes.event import Event
from bot.game_modes.guild_wars import GuildWars
from bot.game_modes.proving_grounds import ProvingGrounds
from bot.game_modes.quest import Quest
from bot.game_modes.raid import Raid
from bot.game_modes.rotb import RiseOfTheBeasts
from bot.game_modes.special import Special
from bot.game_modes.xeno_clash import XenoClash
from bot.game_modes.generic import Generic


class Game:
    """
    Main driver for bot activity and navigation for the web browser bot, Granblue Fantasy.
    """

    _discord_process = None
    _discord_queue = multiprocessing.Queue()

    def __init__(self):
        super().__init__()

    @staticmethod
    def _calibrate_game_window(display_info_check: bool = False):
        """Recalibrate the dimensions of the bot window for fast and accurate image matching.

        Args:
            display_info_check (bool, optional): Displays the screen size and the dimensions of the bot window. Defaults to False.

        Returns:
            None
        """
        # Save the location of the "Home" button at the bottom of the bot window.
        Settings.home_button_location = ImageUtils.find_button("home", bypass_general_adjustment = True, tries = 1)

        MessageLog.print_message("\n[INFO] Recalibrating the dimensions of the window...")

        if Settings.home_button_location is None:
            raise RuntimeError("Calibration of window dimensions failed. Is the Home button on the bottom bar visible?")

        # Set the dimensions of the bot window and save it in ImageUtils so that future operations do not go out of bounds.
        home_back_button = ImageUtils.find_button("home_back")

        if home_back_button is None:
            raise RuntimeError("Calibration of window dimensions failed. Is the back button visible on the screen?")

        width, height = pyautogui.size()
        additional_calibration_required = Settings.static_window

        if Settings.static_window:
            MessageLog.print_message("[INFO] Using static window configuration...")
            if Settings.use_first_notch:
                window_left = home_back_button[0] - 30  # The x-coordinate of the left edge.
            else:
                window_left = home_back_button[0] - 50
            window_top = 0  # The y-coordinate of the top edge.
            if Settings.use_first_notch:
                window_width = window_left + 390  # The width of the region.
            else:
                window_width = window_left + 500
            window_height = pyautogui.size()[1]  # The height of the region.
        else:
            MessageLog.print_message("[INFO] Using dynamic window configuration...")
            window_left: int = 0
            window_top: int = 0
            window_width: int = width
            window_height: int = height

        ImageUtils.update_window_dimensions(window_left, window_top, window_width, window_height, additional_calibration_required)

        MessageLog.print_message("[SUCCESS] Dimensions of the window has been successfully recalibrated.")

        if display_info_check:
            window_dimensions = ImageUtils.get_window_dimensions()
            MessageLog.print_message("\n**********************************************************************")
            MessageLog.print_message("**********************************************************************")
            MessageLog.print_message(f"[INFO] Screen Size: {pyautogui.size()}")
            MessageLog.print_message(f"[INFO] Game Window Dimensions: Region({window_dimensions[0]}, {window_dimensions[1]}, {window_dimensions[2]}, {window_dimensions[3]})")
            MessageLog.print_message("**********************************************************************")
            MessageLog.print_message("**********************************************************************")

        return None

    @staticmethod
    def go_back_home(confirm_location_check: bool = False, display_info_check: bool = False, test_mode: bool = False):
        """Go back to the Home screen to reset the position of the bot. Also able to recalibrate the region dimensions of the bot window if
        display_info_check is True.

        Args:
            confirm_location_check (bool, optional): Check to see if the current location is confirmed to be at the Home screen. Defaults to False.
            display_info_check (bool, optional): Recalibrate the bot window dimensions and displays the info. Defaults to False.
            test_mode (bool, optional): Flag to test and get a valid scale for device compatibility.

        Returns:
            None
        """
        if test_mode:
            MessageLog.print_message("\n[DEBUG] Now beginning test to find a valid scale for this device...")
            ImageUtils.find_button("home", test_mode = True)
            return

        if not ImageUtils.confirm_location("home", bypass_general_adjustment = True):
            MessageLog.print_message("\n[INFO] Moving back to the Home screen...")

            if Game.find_and_click_button("home", bypass_general_adjustment = True) is False:
                raise Exception(
                    "HOME button is not found. Stopping bot to prevent cascade of errors. Please readjust your confidences/scales. Maybe the Home button located on the bottom bar is not visible?")

            # Handle any misc popups on the Home screen.
            Game.find_and_click_button("close", suppress_error = True)

            if confirm_location_check:
                Game.wait(2.0)

                if ImageUtils.confirm_location("home", bypass_general_adjustment = True) is False:
                    Game.find_and_click_button("reload")
                    Game.wait(4.0)
                    if ImageUtils.confirm_location("home", bypass_general_adjustment = True) is False:
                        raise Exception("Failed to head back to the Home screen after clicking on the Home button.")
        else:
            MessageLog.print_message("[INFO] Bot is at the Home screen.")

        # Recalibrate the dimensions of the bot window.
        if display_info_check:
            Game._calibrate_game_window(display_info_check = True)

        return None

    @staticmethod
    def wait(seconds: float = 3.0):
        """Wait the specified seconds to account for ping or loading.

        Args:
            seconds (float, optional): Number of seconds for the execution to wait for. Defaults to 3.0.

        Returns:
            None
        """
        if Settings.reduce_delay_seconds > 0.0:
            if seconds - Settings.reduce_delay_seconds < 0.0:
                time.sleep(seconds)
            else:
                time.sleep(seconds - Settings.reduce_delay_seconds)
        else:
            time.sleep(seconds)
        return None

    @staticmethod
    def find_and_click_button(button_name: str, clicks: int = 1, tries: int = 0, x_offset: int = 0, y_offset: int = 0, custom_confidence: float = 0.80, suppress_error: bool = False,
                              bypass_general_adjustment: bool = True):
        """Find the center point of a button image and click it.

        Args:
            button_name (str): Name of the button image file in the /images/buttons/ folder.
            clicks (int, optional): Number of mouse clicks when clicking the button image location. Defaults to 1.
            tries (int, optional): Number of tries to attempt to find the specified button image. Defaults to 0 which will use ImageUtil's default.
            x_offset (int, optional): Offset the x-coordinate of the click location. Defaults to 0.
            y_offset (int, optional): Offset the y-coordinate of the click location. Defaults to 0.
            custom_confidence (float, optional): Use a custom confidence for the template matching. Defaults to 0.80.
            suppress_error (bool, optional): Suppresses template matching error depending on boolean. Defaults to False.
            bypass_general_adjustment (bool, optional): Bypass using the general adjustment for the number of tries if ImageUtil's default is not being used. Defaults to True.

        Returns:
            (bool): Return True if the button was found and clicked. Otherwise, return False.
        """
        if Settings.debug_mode:
            MessageLog.print_message(f"\n[DEBUG] Attempting to find and click the button: \"{button_name}\".")

        if tries == 0:
            if button_name.lower() == "quest":
                temp_location = ImageUtils.find_button("quest_blue", custom_confidence = custom_confidence)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("quest_red", custom_confidence = custom_confidence)

                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, "quest_blue", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "raid":
                temp_location = ImageUtils.find_button("raid_flat", custom_confidence = custom_confidence)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("raid_bouncing", custom_confidence = custom_confidence)

                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, "raid_flat", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "coop_start":
                temp_location = ImageUtils.find_button("coop_start_flat", custom_confidence = custom_confidence)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("coop_start_faded", custom_confidence = custom_confidence)

                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, "coop_start_flat", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "event_special_quest":
                temp_location = ImageUtils.find_button("event_special_quest", custom_confidence = custom_confidence)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("event_special_quest_flat", custom_confidence = custom_confidence)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("event_special_quest_bouncing", custom_confidence = custom_confidence)

                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, "event_special_quest", mouse_clicks = clicks)
                    return True
            else:
                temp_location = ImageUtils.find_button(button_name.lower(), custom_confidence = custom_confidence)
                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, button_name, mouse_clicks = clicks)
                    return True
        else:
            if button_name.lower() == "quest":
                temp_location = ImageUtils.find_button("quest_blue", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("quest_red", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)

                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, "quest_blue", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "raid":
                temp_location = ImageUtils.find_button("raid_flat", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("raid_bouncing", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)

                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, "raid_flat", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "coop_start":
                temp_location = ImageUtils.find_button("coop_start_flat", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("coop_start_faded", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)

                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, "coop_start_flat", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "event_special_quest":
                temp_location = ImageUtils.find_button("event_special_quest", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("event_special_quest_flat", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)
                if temp_location is None:
                    temp_location = ImageUtils.find_button("event_special_quest_bouncing", tries = tries, custom_confidence = custom_confidence, bypass_general_adjustment = bypass_general_adjustment)

                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, "event_special_quest", mouse_clicks = clicks)
                    return True
            else:
                temp_location = ImageUtils.find_button(button_name.lower(), tries = tries, suppress_error = suppress_error, custom_confidence = custom_confidence,
                                                       bypass_general_adjustment = bypass_general_adjustment)
                if temp_location is not None:
                    MouseUtils.move_and_click_point(temp_location[0] + x_offset, temp_location[1] + y_offset, button_name, mouse_clicks = clicks)
                    return True

        return False

    @staticmethod
    def check_for_captcha():
        """Checks for CAPTCHA right after selecting a Summon and if detected, alert the user and then stop the bot.

        Returns:
            None
        """
        try:
            if ImageUtils.confirm_location("captcha", bypass_general_adjustment = True):
                raise RuntimeError("CAPTCHA DETECTED!")
            else:
                MessageLog.print_message("\n[CAPTCHA] CAPTCHA not detected.")

            return None
        except RuntimeError:
            Game._discord_queue.put(f"> Bot encountered exception while checking for CAPTCHA: \n{traceback.format_exc()}")
            MessageLog.print_message(f"\n[ERROR] Bot encountered exception while checking for CAPTCHA: \n{traceback.format_exc()}")
            ImageUtils.generate_alert_for_captcha()

    @staticmethod
    def _delay_between_runs():
        """Execute a delay after every run completed based on user settings.

        Returns:
            None
        """
        if Settings.enable_delay_between_runs:
            # Check if the provided delay is valid.
            if int(Settings.delay_in_seconds) < 0:
                MessageLog.print_message("\n[INFO] Provided delay in seconds for the resting period is not valid. Defaulting to 15 seconds.")
                Settings.delay_in_seconds = 15

            MessageLog.print_message(f"\n[INFO] Now waiting for {Settings.delay_in_seconds} seconds as the resting period. Please do not navigate from the current screen.")

            Game.wait(int(Settings.delay_in_seconds))
        elif not Settings.enable_delay_between_runs and Settings.enable_randomized_delay_between_runs:
            # Check if the lower and upper bounds are valid.
            if int(Settings.delay_in_seconds_lower_bound) < 0 or int(Settings.delay_in_seconds_lower_bound) > int(Settings.delay_in_seconds_upper_bound):
                MessageLog.print_message("\n[INFO] Provided lower bound delay in seconds for the resting period is not valid. Defaulting to 15 seconds.")
                Settings.delay_in_seconds_lower_bound = 15
            if int(Settings.delay_in_seconds_upper_bound) < 0 or int(Settings.delay_in_seconds_upper_bound) < int(Settings.delay_in_seconds_lower_bound):
                MessageLog.print_message("\n[INFO] Provided upper bound delay in seconds for the resting period is not valid. Defaulting to 60 seconds.")
                Settings.delay_in_seconds_upper_bound = 60

            new_seconds = random.randrange(int(Settings.delay_in_seconds_lower_bound), int(Settings.delay_in_seconds_upper_bound))
            MessageLog.print_message(
                f"\n[INFO] Given the bounds of ({Settings.delay_in_seconds_lower_bound}, {Settings.delay_in_seconds_upper_bound}), bot will now wait for {new_seconds} seconds as a resting period. Please do not navigate from the current screen.")

            Game.wait(new_seconds)

        MessageLog.print_message("\n[INFO] Resting period complete.")
        return None

    @staticmethod
    def _move_mouse_security_check():
        """Moves the mouse off the game window and stay like that for a bit to attempt circumvention of possible bot detection. This is PC specific, not possible for the Android version.

        Returns:
            None
        """
        if Settings.enable_mouse_security_attempt_bypass:
            MessageLog.print_message("\n[INFO] Moving mouse off game window to attempt circumvention of possible bot detection...")

            # Get width and height of the screen.
            width, height = pyautogui.size()

            # Get current x,y coordinate of the mouse.
            curr_x, curr_y = pyautogui.position()

            # Depending on where the mouse is, move the mouse off the game window left or right.
            if curr_x <= width / 2:
                # This is the left half of the screen.
                MouseUtils.move_to(width - 100, curr_y, custom_mouse_speed = Settings.custom_mouse_speed)
            else:
                # This is the right half of the screen.
                MouseUtils.move_to(100, curr_y, custom_mouse_speed = Settings.custom_mouse_speed)

            # Now wait for several seconds before continuing.
            new_seconds = random.randrange(2, 10)
            MessageLog.print_message(f"[INFO] Now waiting {new_seconds} seconds...")
            Game.wait(new_seconds)
            MessageLog.print_message("[INFO] Waiting complete. Now resuming bot operations...")
        return None

    @staticmethod
    def select_summon(summon_list: List[str], summon_element_list: List[str]):
        """Finds and selects the specified Summon based on the current index on the Summon Selection screen and then checks for CAPTCHA right
        afterwards.

        Args:
            summon_list (List[str]): List of names of the Summon image's file name in /images/summons/ folder.
            summon_element_list (List[str]): List of names of the Summon element image file in the /images/buttons/ folder.

        Returns:
            (bool): True if the Summon was found and clicked. Otherwise, return False.
        """
        MessageLog.print_message("\n[INFO] Starting process for Support Summon Selection...")

        # Format the Summon name and Summon element name strings.
        for idx, summon in enumerate(summon_list):
            summon_list[idx] = summon.lower().replace(" ", "_")
        for idx, summon_ele in enumerate(summon_element_list):
            summon_element_list[idx] = summon_ele.lower()

        summon_location = ImageUtils.find_summon(summon_list, summon_element_list)
        if summon_location is not None:
            MouseUtils.move_and_click_point(summon_location[0], summon_location[1], "template_support_summon", mouse_clicks = 2)

            # Check for CAPTCHA here. If detected, stop the bot and alert the user.
            Game.check_for_captcha()

            return True
        elif Settings.enable_bypass_reset_summon:
            MessageLog.print_message("[INFO] Bypassing procedure to reset Summons. Reloading page and selecting the very first one now...")

            Game.find_and_click_button("reload")
            Game.wait(3.0)

            # Now select the first Summon.
            choose_a_summon_location = ImageUtils.find_button("choose_a_summon")
            MouseUtils.move_and_click_point(choose_a_summon_location[0], choose_a_summon_location[1] + 187, "choose_a_summon")

            return True
        else:
            # If a Summon is not found, start a Trial Battle to refresh Summons.
            Game._reset_summons()
            return False

    @staticmethod
    def _reset_summons():
        """Reset the Summons available by starting and then retreating from a Old Lignoid Trial Battle.

        Returns:
            None
        """
        MessageLog.print_message("\n[INFO] Now refreshing Summons...")
        Game.go_back_home(confirm_location_check = True)

        # Scroll down the screen to see the "Gameplay Extra" button on smaller screen sizes.
        MouseUtils.scroll_screen_from_home_button(-600)

        if Game.find_and_click_button("gameplay_extras"):
            # If the bot cannot find the "Trial Battles" button, keep scrolling down until it does. It should not take more than 2 loops to see it for any reasonable screen size.
            while Game.find_and_click_button("trial_battles") is False:
                MouseUtils.scroll_screen_from_home_button(-300)

            if ImageUtils.confirm_location("trial_battles"):
                # Click on the "Old Lignoid" button.
                Game.find_and_click_button("trial_battles_old_lignoid")

                # Select any detected "Play" button.
                Game.find_and_click_button("play_round_button")

                # Now select the first Summon.
                choose_a_summon_location = ImageUtils.find_button("choose_a_summon")
                MouseUtils.move_and_click_point(choose_a_summon_location[0], choose_a_summon_location[1] + 187, "choose_a_summon")

                # Now start the Old Lignoid Trial Battle right away and then wait a few seconds.
                Game.find_and_click_button("party_selection_ok")
                Game.wait(3.0)

                # Retreat from this Trial Battle.
                Game.find_and_click_button("menu", tries = 30)
                Game.find_and_click_button("retreat", tries = 30)
                Game.find_and_click_button("retreat_confirmation", tries = 30)
                Game.go_back_home()

                if ImageUtils.confirm_location("home"):
                    MessageLog.print_message("[SUCCESS] Summons have now been refreshed.")
        else:
            MessageLog.print_message("[WARNING] Failed to reset Summons as the 'Gameplay Extras' button is not visible.")

        return None

    @staticmethod
    def find_party_and_start_mission(group_number: int, party_number: int, tries: int = 30, bypass_first_run: bool = False):
        """Select the specified Group and Party. It will then start the mission.

        Args:
            group_number (int): The Group that the specified Party is in.
            party_number (int): The specified Party to start the mission with.
            tries (int, optional): Number of tries to select a Set before failing. Defaults to 30.
            bypass_first_run (bool, optional): Determines if the bot should reselect the party in subsequent runs. Defaults to False.

        Returns:
            (bool): Returns False if it detects the "Raid is full/Raid is already done" dialog. Otherwise, return True.
        """
        # Repeat runs already have the same party already selected.
        if Settings.party_selection_first_run or bypass_first_run:
            MessageLog.print_message(f"\n[INFO] Starting process to select Group {group_number}, Party {party_number}...")

            # Find the Group that the Party is in first. If the specified Group number is less than 8, it is in Set A. Otherwise, it is in Set B. If failed, alternate searching for Set A / Set B until
            # found or tries are depleted.
            set_location = None
            if Settings.farming_mode == "Arcarum Sandbox":
                while set_location is None:
                    set_location = ImageUtils.find_button("party_set_extra", tries = 10)
                    if set_location is None:
                        tries -= 1
                        if tries <= 0:
                            raise RuntimeError("Could not find Set Extra.")
            else:
                if Settings.farming_mode == "Raid" and ImageUtils.find_button("party_set_extra", tries = 3):
                    MessageLog.print_message(f"[INFO] Skipping Set Selection due to Raid only allowing parties from the Extra category.")
                elif group_number < 8:
                    while set_location is None:
                        set_location = ImageUtils.find_button("party_set_a")
                        if set_location is None:
                            tries -= 1
                            if tries <= 0:
                                raise RuntimeError("Could not find Set A.")

                            # See if the user had Set B active instead of Set A if matching failed.
                            Game.find_and_click_button("party_set_b")
                else:
                    while set_location is None:
                        set_location = ImageUtils.find_button("party_set_b")
                        if set_location is None:
                            tries -= 1
                            if tries <= 0:
                                raise RuntimeError("Could not find Set B.")

                            # See if the user had Set A active instead of Set B if matching failed.
                            Game.find_and_click_button("party_set_a")

            # Center the mouse on the "Set A" / "Set B" button and then click the correct Group tab.
            if Settings.debug_mode:
                MessageLog.print_message(f"[DEBUG] Successfully selected the correct Set. Now selecting Group {group_number}...")

            # Determine offsets and increments for the group selection.
            if Settings.use_first_notch is False:
                x_offset = 360
                x_inc = 60
                y_offset = 55
            else:
                x_offset = 235
                x_inc = 40
                y_offset = 40

            if group_number == 1 or group_number == 8:
                x = set_location[0] - x_offset + (x_inc * 0)
            elif group_number == 2 or group_number == 9:
                x = set_location[0] - x_offset + (x_inc * 1)
            elif group_number == 3 or group_number == 10:
                x = set_location[0] - x_offset + (x_inc * 2)
            elif group_number == 4 or group_number == 11:
                x = set_location[0] - x_offset + (x_inc * 3)
            elif group_number == 5 or group_number == 12:
                x = set_location[0] - x_offset + (x_inc * 4)
            elif group_number == 6 or group_number == 13:
                x = set_location[0] - x_offset + (x_inc * 5)
            else:
                x = set_location[0] - x_offset + (x_inc * 6)
            y = set_location[1] + y_offset

            MouseUtils.move_and_click_point(x, y, "template_group", mouse_clicks = 2)

            # Now select the correct Party.
            if Settings.debug_mode:
                MessageLog.print_message(f"[DEBUG] Successfully selected Group {group_number}. Now selecting Party {party_number}...")

            # Determine offsets and increments for the party selection.
            if Settings.use_first_notch is False:
                x_offset = 325
                x_inc = 60
                y_offset = 325
            else:
                x_offset = 215
                x_inc = 40
                y_offset = 220

            if party_number == 1 or party_number == 8:
                x = set_location[0] - x_offset + (x_inc * 0)
            elif party_number == 2 or party_number == 9:
                x = set_location[0] - x_offset + (x_inc * 1)
            elif party_number == 3 or party_number == 10:
                x = set_location[0] - x_offset + (x_inc * 2)
            elif party_number == 4 or party_number == 11:
                x = set_location[0] - x_offset + (x_inc * 3)
            elif party_number == 5 or party_number == 12:
                x = set_location[0] - x_offset + (x_inc * 4)
            elif party_number == 6 or party_number == 13:
                x = set_location[0] - x_offset + (x_inc * 5)
            else:
                x = set_location[0] - x_offset + (x_inc * 6)

            y = set_location[1] + y_offset

            MouseUtils.move_and_click_point(x, y, "template_party", mouse_clicks = 2)

            Settings.party_selection_first_run = False

            MessageLog.print_message(f"[INFO] Successfully selected Group {group_number}, Party {party_number}. Now starting the mission.")
        else:
            MessageLog.print_message("\n[INFO] Reusing the same Party.")

        # Find and click the "OK" button to start the mission.
        Game.find_and_click_button("ok")

        # If a popup appears and says "This raid battle has already ended. The Home screen will now appear.", return False.
        if Settings.farming_mode.lower() == "raid" and ImageUtils.confirm_location("raids"):
            MessageLog.print_message("\n[WARNING] Raid unfortunately just ended. Backing out now...")
            Game.find_and_click_button("ok")
            Game.wait(3.0)
            return False

        Game.wait(3.0)
        return True

    @staticmethod
    def check_for_ap():
        """Check if the user has enabled the auto-restore option for AP.

        Returns:
            None
        """
        Game.wait(3)

        if ImageUtils.confirm_location("not_enough_ap", tries = 2):
            raise RuntimeError("AP auto-restore check failed. Please enable the auto-restore option in the in-game settings according to the GitHub instructions.")
        else:
            MessageLog.print_message("\n[INFO] AP auto-restore check passed. Continuing to Party Selection...")

        return None

    @staticmethod
    def check_for_ep():
        """Check if the user has enabled the auto-restore option for EP.

        Returns:
            None
        """
        Game.wait(3)

        if Settings.farming_mode.lower() == "raid" and ImageUtils.confirm_location("not_enough_ep", tries = 2):
            raise RuntimeError("EP auto-restore check failed. Please enable the auto-restore option in the in-game settings according to the GitHub instructions.")
        else:
            MessageLog.print_message("[INFO] EP auto-restore check passed. Continuing to Party Selection...")

        return None

    @staticmethod
    def collect_loot(is_completed: bool, is_pending_battle: bool = False, is_event_nightmare: bool = False, skip_info: bool = False, skip_popup_check: bool = False, is_defender: bool = False):
        """Collects the loot from the Results screen while clicking away any dialog popups while updating the internal item count.

        Args:
            is_completed (bool): Allows incrementing of number of runs completed. This is for Farming Modes who have multi-part sections to them to prevent unnecessary incrementing of runs when it wasn't finished with 1 yet.
            is_pending_battle (bool, optional): Skip the incrementation of runs attempted if this was a Pending Battle. Defaults to False.
            is_event_nightmare (bool, optional): Skip the incrementation of runs attempted if this was a Event Nightmare. Defaults to False.
            skip_info (bool, optional): Skip printing the information of the run. Defaults to False.
            skip_popup_check (bool, optional): Skip checking for popups to get to the Loot Collected screen. Defaults to False.
            is_defender (bool, optional): Skip the incrementation of runs attempted if this was a Defender. Defaults to False.

        Returns:
            None
        """
        temp_amount = 0

        # Close all popups until the bot reaches the Loot Collected screen.
        if skip_popup_check is False:
            loot_collection_tries = 30
            while not ImageUtils.confirm_location("loot_collected", tries = 1, disable_adjustment = True):
                loot_collection_tries -= 1
                if loot_collection_tries <= 0:
                    raise RuntimeError("Unable to progress in the Loot Collection process.")

                Game.find_and_click_button("ok", tries = 1, suppress_error = True)
                Game.find_and_click_button("close", tries = 1, suppress_error = True)
                Game.find_and_click_button("cancel", tries = 1, suppress_error = True)

                # Search for and click on the "Extended Mastery" popup.
                Game.find_and_click_button("new_extended_mastery_level", tries = 1, suppress_error = True)

                if ImageUtils.confirm_location("no_loot", tries = 1, suppress_error = True, disable_adjustment = True):
                    return None

                if Settings.debug_mode:
                    MessageLog.print_message("[DEBUG] Have not detected the Loot Collection screen yet...")

        # Now that the bot is at the Loot Collected screen, detect any user-specified items.
        if is_completed and not is_pending_battle and not is_event_nightmare and not is_defender:
            MessageLog.print_message("\n[INFO] Detecting if any user-specified loot dropped from this run...")
            if Settings.item_name != "EXP" and Settings.item_name != "Angel Halo Weapons" and Settings.item_name != "Repeated Runs":
                temp_amount = ImageUtils.find_farmed_items(Settings.item_name)
            else:
                temp_amount = 1

            Settings.amount_of_runs_finished += 1
            Settings.item_amount_farmed += temp_amount
        elif is_pending_battle:
            MessageLog.print_message("\n[INFO] Detecting if any user-specified loot dropped from this pending battle...")
            if Settings.item_name != "EXP" and Settings.item_name != "Angel Halo Weapons" and Settings.item_name != "Repeated Runs":
                temp_amount = ImageUtils.find_farmed_items(Settings.item_name)
            else:
                temp_amount = 0

            Settings.item_amount_farmed += temp_amount

        # If there were item drops detected and the user opt in to sending their result to Granblue Automation Statistics, then have the frontend send the API request.
        if temp_amount != 0 and Settings.enable_opt_in_api:
            if is_pending_battle:
                Game._send_api_result(temp_amount, 0.0)
            else:
                Game._send_api_result(temp_amount, Settings.combat_elapsed_time)

        if is_completed and not is_pending_battle and not is_event_nightmare and not skip_info and not is_defender:
            if Settings.item_name != "EXP" and Settings.item_name != "Angel Halo Weapons" and Settings.item_name != "Repeated Runs":
                MessageLog.print_message("\n**********************************************************************")
                MessageLog.print_message("**********************************************************************")
                MessageLog.print_message(f"[FARM] Farming Mode: {Settings.farming_mode}")
                MessageLog.print_message(f"[FARM] Mission: {Settings.mission_name}")
                MessageLog.print_message(f"[FARM] Summons: {Settings.summon_list}")
                MessageLog.print_message(f"[FARM] Amount of {Settings.item_name} gained from this run: {temp_amount}")
                MessageLog.print_message(f"[FARM] Amount of {Settings.item_name} gained in total: {Settings.item_amount_farmed} / {Settings.item_amount_to_farm}")
                MessageLog.print_message(f"[FARM] Amount of runs completed: {Settings.amount_of_runs_finished}")
                MessageLog.print_message("**********************************************************************")
                MessageLog.print_message("**********************************************************************\n")

                if temp_amount != 0:
                    if Settings.item_amount_farmed >= Settings.item_amount_to_farm:
                        discord_string = f"> {temp_amount}x __{Settings.item_name}__ gained from this run: **[{Settings.item_amount_farmed - temp_amount} / {Settings.item_amount_to_farm}]** -> " \
                                         f"**[{Settings.item_amount_farmed} / {Settings.item_amount_to_farm}]** :white_check_mark:"
                    else:
                        discord_string = f"> {temp_amount}x __{Settings.item_name}__ gained from this run: **[{Settings.item_amount_farmed - temp_amount} / {Settings.item_amount_to_farm}]** -> " \
                                         f"**[{Settings.item_amount_farmed} / {Settings.item_amount_to_farm}]**"

                    Game._discord_queue.put(discord_string)
            else:
                MessageLog.print_message("\n**********************************************************************")
                MessageLog.print_message("**********************************************************************")
                MessageLog.print_message(f"[FARM] Farming Mode: {Settings.farming_mode}")
                MessageLog.print_message(f"[FARM] Mission: {Settings.mission_name}")
                MessageLog.print_message(f"[FARM] Summons: {Settings.summon_list}")
                MessageLog.print_message(f"[FARM] Amount of runs completed: {Settings.amount_of_runs_finished} / {Settings.item_amount_to_farm}")
                MessageLog.print_message("**********************************************************************")
                MessageLog.print_message("**********************************************************************\n")

                if Settings.amount_of_runs_finished >= Settings.item_amount_to_farm:
                    discord_string = f"> Runs completed for __{Settings.mission_name}__: **[{Settings.amount_of_runs_finished - 1} / {Settings.item_amount_to_farm}]** -> " \
                                     f"**[{Settings.amount_of_runs_finished} / {Settings.item_amount_to_farm}]** :white_check_mark:"
                else:
                    discord_string = f"> Runs completed for __{Settings.mission_name}__: **[{Settings.amount_of_runs_finished - 1} / {Settings.item_amount_to_farm}]** -> " \
                                     f"**[{Settings.amount_of_runs_finished} / {Settings.item_amount_to_farm}]**"

                Game._discord_queue.put(discord_string)
        elif is_pending_battle and temp_amount > 0 and not skip_info:
            if Settings.item_name != "EXP" and Settings.item_name != "Angel Halo Weapons" and Settings.item_name != "Repeated Runs":
                MessageLog.print_message("\n**********************************************************************")
                MessageLog.print_message("**********************************************************************")
                MessageLog.print_message(f"[FARM] Farming Mode: {Settings.farming_mode}")
                MessageLog.print_message(f"[FARM] Mission: {Settings.mission_name}")
                MessageLog.print_message(f"[FARM] Summons: {Settings.summon_list}")
                MessageLog.print_message(f"[FARM] Amount of {Settings.item_name} gained from this pending battle: {temp_amount}")
                MessageLog.print_message(f"[FARM] Amount of {Settings.item_name} gained in total: {Settings.item_amount_farmed} / {Settings.item_amount_to_farm}")
                MessageLog.print_message(f"[FARM] Amount of runs completed: {Settings.amount_of_runs_finished}")
                MessageLog.print_message("**********************************************************************")
                MessageLog.print_message("**********************************************************************\n")

                if temp_amount != 0:
                    if Settings.item_amount_farmed >= Settings.item_amount_to_farm:
                        discord_string = f"> {temp_amount}x __{Settings.item_name}__ gained from this pending battle: **[{Settings.item_amount_farmed - temp_amount} / {Settings.item_amount_to_farm}]** -> " \
                                         f"**[{Settings.item_amount_farmed} / {Settings.item_amount_to_farm}]** :white_check_mark:"
                    else:
                        discord_string = f"> {temp_amount}x __{Settings.item_name}__ gained from this pending battle: **[{Settings.item_amount_farmed - temp_amount} / {Settings.item_amount_to_farm}]** -> " \
                                         f"**[{Settings.item_amount_farmed} / {Settings.item_amount_to_farm}]**"

                    Game._discord_queue.put(discord_string)
        elif is_defender:
            Settings.engaged_defender_battle = False
            Settings.number_of_defeated_defenders += 1
            MessageLog.print_message("\n**********************************************************************")
            MessageLog.print_message("**********************************************************************")
            MessageLog.print_message(f"[FARM] Farming Mode: {Settings.farming_mode}")
            MessageLog.print_message(f"[FARM] Mission: {Settings.mission_name}")
            MessageLog.print_message(f"[FARM] Summons: {Settings.summon_list}")
            MessageLog.print_message(f"[FARM] Amount of Defenders defeated: {Settings.number_of_defeated_defenders}/{Settings.number_of_defenders}")
            MessageLog.print_message("**********************************************************************")
            MessageLog.print_message("**********************************************************************\n")

        return None

    @staticmethod
    def check_for_popups() -> bool:
        """Detect any popups and attempt to close them all with the final destination being the Summon Selection screen.

        Returns:
            (bool): True if there was a Nightmare mission detected or some other popup appeared that requires the navigation process to be restarted.
        """
        MessageLog.print_message(f"\n[INFO] Now beginning process to check for popups...")

        check_popup_tries = 30
        while ImageUtils.confirm_location("select_a_summon", tries = 1, suppress_error = True) is False:
            check_popup_tries -= 1
            if check_popup_tries <= 0:
                raise RuntimeError("Failed to progress in the Check for Popups process...")

            if Settings.farming_mode == "Rise of the Beasts" and ImageUtils.confirm_location("proud_solo_quest", tries = 1):
                # Scroll down the screen a little bit because the popup itself is too long for screen sizes around 1080p.
                MouseUtils.scroll_screen_from_home_button(-400)

            # Check for certain popups for certain Farming Modes.
            if (Settings.farming_mode == "Rise of the Beasts" and RiseOfTheBeasts.check_for_rotb_extreme_plus()) or (
                    Settings.farming_mode == "Special" and Settings.mission_name == "VH Angel Halo" and Settings.item_name == "Angel Halo Weapons" and Special.check_for_dimensional_halo()) or (
                    (Settings.farming_mode == "Event" or Settings.farming_mode == "Event (Token Drawboxes)") and Event.check_for_event_nightmare()) or (
                    Settings.farming_mode == "Xeno Clash" and XenoClash.check_for_xeno_clash_nightmare()):
                return True

            # If the bot tried to repeat a Extreme/Impossible difficulty Event Raid and it lacked the treasures to host it, go back to select the Mission again.
            if (Settings.farming_mode == "Event (Token Drawboxes)" or Settings.farming_mode == "Guild Wars") and ImageUtils.confirm_location("not_enough_treasure", tries = 1):
                Game.find_and_click_button("ok")
                return True

            # Attempt to close any popup by clicking on any detected "Close" and "Cancel" buttons.
            if Game.find_and_click_button("close", tries = 1, suppress_error = True) is False:
                Game.find_and_click_button("cancel", tries = 1, suppress_error = True)

            if Settings.debug_mode:
                MessageLog.print_message("[DEBUG] Have not detected the Support Summon Selection screen yet...")

        return False

    @staticmethod
    def _clear_pending_battle():
        """Process a Pending Battle.

        Returns:
            (bool): Return True if a Pending Battle was successfully processed. Otherwise, return False.
        """
        if Game.find_and_click_button("tap_here_to_see_rewards", tries = 10):
            MessageLog.print_message(f"[INFO] Clearing this Pending Battle...")
            Game.wait(1)

            # If there is loot available, start loot detection.
            if ImageUtils.confirm_location("no_loot", disable_adjustment = True):
                MessageLog.print_message(f"[INFO] No loot can be collected.")

                # Navigate back to the Quests screen.
                Game.find_and_click_button("quests")

                return True
            else:
                if Settings.farming_mode == "Raid":
                    Game.collect_loot(is_completed = True)
                else:
                    Game.collect_loot(is_completed = False, is_pending_battle = True)

                Game.find_and_click_button("close", suppress_error = True)
                Game.find_and_click_button("ok", suppress_error = True)

                return True
        else:
            MessageLog.print_message(f"[INFO] No more Pending Battles left to claim.")

        return False

    @staticmethod
    def check_for_friend_request():
        """Check for the Friend Request popup.

        Returns:
            None
        """
        if ImageUtils.confirm_location("friend_request"):
            Game.find_and_click_button("cancel")
            Game.wait(2.0)
        return None

    @staticmethod
    def check_for_skyscope():
        """Check for the Skyscope popup.

        Returns:
            None
        """
        if ImageUtils.confirm_location("skyscope"):
            Game.find_and_click_button("close")
            Game.wait(2.0)
        return None

    @staticmethod
    def check_for_pending():
        """Check and collect any pending rewards and free up slots for the bot to join more raids.

        Returns:
            (bool): Return True if Pending Battles were detected. Otherwise, return False.
        """
        MessageLog.print_message(f"\n[INFO] Starting process of checking for Pending Battles...")

        if Settings.enable_pending_battles_adjustment:
            Game.wait(Settings.adjust_before_pending_battle)
        else:
            Game.wait(1)

        if ImageUtils.confirm_location("check_your_pending_battles", tries = 2, bypass_general_adjustment = True) or \
                ImageUtils.confirm_location("pending_battles", tries = 2, bypass_general_adjustment = True) or \
                Game.find_and_click_button("quest_results_pending_battles", tries = 2, bypass_general_adjustment = True):
            MessageLog.print_message(f"[INFO] Found Pending Battles that need collecting from.")

            Game.find_and_click_button("ok")
            Game.wait(1)

            if ImageUtils.confirm_location("pending_battles"):
                # Process the current Pending Battle.
                while Game._clear_pending_battle():
                    # While on the Loot Collected screen, if there are more Pending Battles then head back to the Pending Battles screen.
                    if ImageUtils.find_button("quest_results_pending_battles"):
                        Game.find_and_click_button("quest_results_pending_battles")
                        Game.wait(1)

                        # Close the Skyscope mission popup.
                        Game.check_for_skyscope()
                    else:
                        # When there are no more Pending Battles, go back to the Home screen.
                        Game.find_and_click_button("home")

                        # Close the Skyscope mission popup.
                        Game.check_for_skyscope()
                        break

            MessageLog.print_message(f"[INFO] Pending battles have been cleared.")
            return True

        MessageLog.print_message(f"[INFO] No Pending Battles needed to be cleared.")
        return False

    @staticmethod
    def start_discord_process():
        """Starts the Discord process.

        Returns:
            None
        """
        if Settings.enable_discord and Settings.discord_token != "" and Settings.user_id != 0:
            MessageLog.print_message("\n[DISCORD] Starting Discord process on a new Thread...")
            Game._discord_process = multiprocessing.Process(target = discord_utils.start_now, args = (Settings.discord_token, Settings.user_id, Game._discord_queue))
            Game._discord_process.start()
        else:
            MessageLog.print_message("\n[DISCORD] Unable to start Discord process. Either you opted not to turn it on or your included token/user id inside the Settings or settings.json are invalid.")

        return None

    @staticmethod
    def stop_discord_process():
        """Stops the Discord process.

        Returns:
            None
        """
        if Game._discord_process is not None and Game._discord_process.is_alive():
            MessageLog.print_message("\n[DISCORD] Now terminating Discord process...")
            while Game._discord_queue.empty() is False:
                Game.wait(1.0)

            Game._discord_queue.put(f"```diff\n- Terminated connection to Discord API for Granblue Automation\n```")
            MessageLog.print_message("[DISCORD] Terminated connection to Discord API and terminating its Thread.")
            Game.wait(1.0)
            Game._discord_process.terminate()

        return None

    @staticmethod
    def _send_api_result(amount: int, elapsed_time: float):
        """Prints a formatted message as a way to send the event back to the frontend in order to have it send the result to the database.

        Args:
            amount (int): Amount of items detected for this run.
            elapsed_time (str): Elapsed time for Combat Mode from start to finish.

        Returns:
            None
        """
        formatted_elapsed_time = elapsed_time
        if formatted_elapsed_time != 0.0:
            import datetime
            formatted_elapsed_time = str(datetime.timedelta(seconds = elapsed_time)).split('.')[0]

        MessageLog.print_message(f"\nSending API request to Granblue Automation Statistics...")
        MessageLog.print_message(f"API-RESULT|{Settings.item_name}|{amount}|{formatted_elapsed_time}")
        return None

    @staticmethod
    def start_farming_mode():
        """Start the Farming Mode using the given parameters.

        Returns:
            (bool): True if Farming Mode ended successfully.
        """
        exception_occurred = False
        try:
            Game.start_discord_process()

            if Settings.enable_test_for_home_screen:
                Game.go_back_home(confirm_location_check = True, test_mode = True)
                return True

            # Calibrate the dimensions of the bot window on bot launch.
            Game._calibrate_game_window(display_info_check = True)

            if Settings.item_name != "EXP":
                MessageLog.print_message("\n######################################################################")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message(f"[FARM] Starting Farming Mode for {Settings.farming_mode}.")
                MessageLog.print_message(f"[FARM] Farming {Settings.item_amount_to_farm}x {Settings.item_name} at {Settings.mission_name}.")
                MessageLog.print_message(f"[FARM] Combat Script name: {Settings.combat_script_name}")
                MessageLog.print_message(f"[FARM] Combat Script: {Settings.combat_script}")
                MessageLog.print_message(f"[FARM] Summons: {Settings.summon_list}")
                MessageLog.print_message(f"[FARM] Group #: {Settings.group_number}")
                MessageLog.print_message(f"[FARM] Party #: {Settings.party_number}")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message("######################################################################\n")
            else:
                MessageLog.print_message("\n######################################################################")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message(f"[FARM] Starting Farming Mode for {Settings.farming_mode}.")
                MessageLog.print_message(f"[FARM] Doing {Settings.item_amount_to_farm}x runs for {Settings.item_name} at {Settings.mission_name}.")
                MessageLog.print_message(f"[FARM] Combat Script name: {Settings.combat_script_name}")
                MessageLog.print_message(f"[FARM] Combat Script: {Settings.combat_script}")
                MessageLog.print_message(f"[FARM] Summons: {Settings.summon_list}")
                MessageLog.print_message(f"[FARM] Group #: {Settings.group_number}")
                MessageLog.print_message(f"[FARM] Party #: {Settings.party_number}")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message("######################################################################\n")

            if Settings.farming_mode == "Raid":
                TwitterRoomFinder.connect()

            first_run = True
            while Settings.item_amount_farmed < Settings.item_amount_to_farm:
                if Settings.farming_mode == "Quest":
                    Quest.start(first_run)
                elif Settings.farming_mode == "Special":
                    Special.start(first_run)
                elif Settings.farming_mode == "Coop":
                    Coop.start(first_run)
                elif Settings.farming_mode == "Raid":
                    Raid.start(first_run)
                elif Settings.farming_mode == "Event" or Settings.farming_mode == "Event (Token Drawboxes)":
                    Event.start(first_run)
                elif Settings.farming_mode == "Rise of the Beasts":
                    RiseOfTheBeasts.start(first_run)
                elif Settings.farming_mode == "Guild Wars":
                    GuildWars.start(first_run)
                elif Settings.farming_mode == "Dread Barrage":
                    DreadBarrage.start(first_run)
                elif Settings.farming_mode == "Proving Grounds":
                    ProvingGrounds.start(first_run)
                elif Settings.farming_mode == "Xeno Clash":
                    XenoClash.start(first_run)
                elif Settings.farming_mode == "Arcarum":
                    Arcarum.start()
                elif Settings.farming_mode == "Arcarum Sandbox":
                    ArcarumSandbox.start()
                elif Settings.farming_mode == "Generic":
                    Generic.start()

                if Settings.item_amount_farmed < Settings.item_amount_to_farm:
                    # Generate a resting period if the user enabled it.
                    Game._delay_between_runs()
                    Game._move_mouse_security_check()
                    first_run = False

        except Exception as e:
            Game._discord_queue.put(f"> Bot encountered exception in Farming Mode: \n{e}")
            exception_occurred = True
            MessageLog.print_message(f"\n[ERROR] Bot encountered exception in Farming Mode: \n{traceback.format_exc()}")
            ImageUtils.generate_alert(f"Bot encountered exception in Farming Mode: \n{e}")

        if Settings.farming_mode == "Raid":
                TwitterRoomFinder.disconnect()

        Game.stop_discord_process()
        
        if exception_occurred:
            MessageLog.print_message("\n######################################################################")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("[FARM] Ending Farming Mode due to encountering Exception.")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("######################################################################\n")
            Game.wait(1.0)
            return False
        else:
            MessageLog.print_message("\n######################################################################")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("[FARM] Ending Farming Mode.")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("######################################################################\n")
            Game._move_mouse_security_check()
            Game.wait(1.0)
            return True
