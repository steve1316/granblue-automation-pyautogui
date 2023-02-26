import random

import pyautogui
import pyclick
import pyperclip

from utils.settings import Settings
from utils.message_log import MessageLog


class MouseUtils:
    """
    Provides the utility functions needed to perform mouse-related actions.
    """

    _hc = pyclick.HumanClicker()

    if Settings.enable_bezier_curve_mouse_movement is False:
        pyautogui.MINIMUM_DURATION = 0.1
        pyautogui.MINIMUM_SLEEP = 0.05
        pyautogui.PAUSE = 0.25

    @staticmethod
    def move_to(x: int, y: int, custom_mouse_speed: float = 0.0):
        """Move the cursor to the coordinates on the screen.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            custom_mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.0.

        Returns:
            None
        """
        if Settings.enable_bezier_curve_mouse_movement:
            # HumanClicker only accepts int as the mouse speed.
            if int(custom_mouse_speed) < 1:
                custom_mouse_speed = 1

            MouseUtils._hc.move((x, y), duration = custom_mouse_speed, humanCurve = pyclick.HumanCurve(pyautogui.position(), (x, y)))
        else:
            if custom_mouse_speed <= 0.0:
                custom_mouse_speed = Settings.custom_mouse_speed

            pyautogui.moveTo(x, y, duration = custom_mouse_speed, tween = pyautogui.easeInOutQuad)

        return None

    @staticmethod
    def move_and_click_point(x: int, y: int, image_name: str, custom_mouse_speed: float = 0.0, mouse_clicks: int = 1):
        """Move the cursor to the specified point on the screen and clicks it.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            image_name (str): File name of the image in /images/buttons/ folder.
            custom_mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.0.
            mouse_clicks (int, optional): Number of mouse clicks. Defaults to 1.

        Returns:
            None
        """
        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Old coordinates: ({x}, {y})")

        new_x, new_y = MouseUtils._randomize_point(x, y, image_name)

        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] New coordinates: ({new_x}, {new_y})")

        # Move the mouse to the specified coordinates.
        if Settings.enable_bezier_curve_mouse_movement:
            # HumanClicker only accepts int as the mouse speed.
            if int(custom_mouse_speed) < 1:
                custom_mouse_speed = 1

            MouseUtils._hc.move((new_x, new_y), duration = custom_mouse_speed, humanCurve = pyclick.HumanCurve(pyautogui.position(), (new_x, new_y)))
        else:
            if custom_mouse_speed <= 0.0:
                custom_mouse_speed = Settings.custom_mouse_speed

            pyautogui.moveTo(x, y, duration = custom_mouse_speed, tween = pyautogui.easeInOutQuad)

        pyautogui.click(clicks = mouse_clicks)

        # This delay is necessary as ImageUtils will take the screenshot too fast and the bot will use the last frame before clicking to navigate.
        from bot.game import Game
        Game.wait(1)

        return None

    @staticmethod
    def _randomize_point(x: int, y: int, image_name: str):
        """Randomize the clicking location in an attempt to avoid clicking the same location that may make the bot look suspicious.

        Args:
            x (int): X coordinate on the screen of the center of the match location.
            y (int): Y coordinate on the screen of the center of the match location.
            image_name (str): File name of the image in /images/buttons/ folder.

        Returns:
            (int, int): Tuple of the newly randomized location to click.
        """
        # Get the width and height of the template image.
        from utils.image_utils import ImageUtils
        width, height = ImageUtils.get_button_dimensions(image_name)

        dimensions_x0 = x - (width // 2)
        dimensions_x1 = x + (width // 2)

        dimensions_y0 = y - (height // 2)
        dimensions_y1 = y + (height // 2)

        while True:
            new_width = random.randint(int(width * 0.2), int(width * 0.8))
            new_height = random.randint(int(height * 0.2), int(height * 0.8))

            new_x = dimensions_x0 + new_width
            new_y = dimensions_y0 + new_height

            # If the new coordinates are within the bounds of the template image, break out of the loop and return the coordinates.
            if new_x > dimensions_x0 or new_x < dimensions_x1 or new_y > dimensions_y0 or new_y < dimensions_y1:
                break

        return new_x, new_y

    @staticmethod
    def scroll_screen(x: int, y: int, scroll_clicks: int):
        """Attempt to scroll the screen to reveal more UI elements from the provided x and y coordinates.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            scroll_clicks (int): How much to scroll the screen. Positive for scrolling up and negative for scrolling down.

        Returns:
            None
        """
        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Now scrolling the screen from ({x}, {y}) by {scroll_clicks} clicks...")

        MouseUtils.move_to(x, y)

        if Settings.enable_bezier_curve_mouse_movement:
            # Reset the pause delay back to 0.25, primarily for ImageUtils' methods using pyautogui.
            pyautogui.PAUSE = 0.25

        pyautogui.scroll(scroll_clicks, x = x, y = y)

        return None

    @staticmethod
    def scroll_screen_from_home_button(scroll_clicks: int):
        """Attempt to scroll the screen using the "Home" button coordinates to reveal more UI elements.

        Args:
            scroll_clicks (int): How much to scroll the screen. Positive for scrolling up and negative for scrolling down.

        Returns:
            None
        """
        x = Settings.home_button_location[0]
        y = Settings.home_button_location[1] - 200

        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Now scrolling the screen from the \"Home\" button's coordinates at ({x}, {y}) by {scroll_clicks} clicks...")

        MouseUtils.move_to(x, y)

        if Settings.enable_bezier_curve_mouse_movement:
            # Reset the pause delay back to 0.25, primarily for ImageUtils' methods using pyautogui.
            pyautogui.PAUSE = 0.25

        pyautogui.scroll(scroll_clicks, x = x, y = y)

        return None

    @staticmethod
    def clear_textbox():
        """Clear the selected textbox of all text by selecting all text by CTRL + A and then pressing DEL.

        Returns:
            None
        """
        pyautogui.keyDown("ctrl")
        pyautogui.press("a")
        pyautogui.keyUp("ctrl")
        pyautogui.press("del")
        return None

    @staticmethod
    def copy_to_clipboard(message: str):
        """Copy the message to the clipboard.

        Args:
            message (str): The message to be copied.

        Returns:
            None
        """
        pyperclip.copy(message)
        return None

    @staticmethod
    def paste_from_clipboard():
        """Paste from the clipboard. Make sure that the textbox is already selected.

        Returns:
            None
        """
        message = pyperclip.paste()
        pyautogui.write(message)
        return None
