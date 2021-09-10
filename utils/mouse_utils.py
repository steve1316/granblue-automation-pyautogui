import random
import traceback

import pyautogui
import pyclick
import pyperclip


class MouseUtils:
    """
    Provides the utility functions needed to perform mouse-related actions.

    Attributes
    ----------
    game (bot.Game): The Game object.
    
    enable_bezier_curve (bool): Enables the usage of the Bezier Curve to allow the bot to utilize human-like but slow mouse movement.

    mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.2.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """

    def __init__(self, game, enable_bezier_curve: bool, mouse_speed: float = 0.2, debug_mode: bool = False):
        super().__init__()

        self._game = game
        self._enable_bezier_curve = enable_bezier_curve
        self._mouse_speed = mouse_speed
        self._debug_mode = debug_mode

        if enable_bezier_curve:
            self._hc = pyclick.HumanClicker()
        else:
            pyautogui.MINIMUM_DURATION = 0.1
            pyautogui.MINIMUM_SLEEP = 0.05
            pyautogui.PAUSE = 0.25

    def move_to(self, x: int, y: int, custom_mouse_speed: float = 0.0):
        """Move the cursor to the coordinates on the screen.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            custom_mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.0.

        Returns:
            None
        """
        try:
            if self._enable_bezier_curve:
                # HumanClicker only accepts int as the mouse speed.
                if int(custom_mouse_speed) < 1:
                    custom_mouse_speed = 1

                self._hc.move((x, y), duration = custom_mouse_speed, humanCurve = pyclick.HumanCurve(pyautogui.position(), (x, y)))
            else:
                if custom_mouse_speed <= 0.0:
                    custom_mouse_speed = self._mouse_speed

                pyautogui.moveTo(x, y, duration = custom_mouse_speed, tween = pyautogui.easeInOutQuad)
            return None
        except Exception:
            self._game.print_and_save(f"\n[ERROR] Bot encountered exception attempting to move the mouse cursor to Point({x}, {y}): \n{traceback.format_exc()}")

    def move_and_click_point(self, x: int, y: int, image_name: str, custom_mouse_speed: float = 0.0, mouse_clicks: int = 1):
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
        try:
            if self._debug_mode:
                self._game.print_and_save(f"[DEBUG] Old coordinates: ({x}, {y})")

            new_x, new_y = self._randomize_point(x, y, image_name)

            if self._debug_mode:
                self._game.print_and_save(f"[DEBUG] New coordinates: ({new_x}, {new_y})")

            # Move the mouse to the specified coordinates.
            if self._enable_bezier_curve:
                # HumanClicker only accepts int as the mouse speed.
                if int(custom_mouse_speed) < 1:
                    custom_mouse_speed = 1

                self._hc.move((new_x, new_y), duration = custom_mouse_speed, humanCurve = pyclick.HumanCurve(pyautogui.position(), (new_x, new_y)))
            else:
                if custom_mouse_speed <= 0.0:
                    custom_mouse_speed = self._mouse_speed

                pyautogui.moveTo(x, y, duration = custom_mouse_speed, tween = pyautogui.easeInOutQuad)

            pyautogui.click(clicks = mouse_clicks)

            # This delay is necessary as ImageUtils will take the screenshot too fast and the bot will use the last frame before clicking to navigate.
            self._game.wait(1)

            return None
        except Exception:
            self._game.print_and_save(f"\n[ERROR] Bot encountered exception attempting to move the mouse cursor to Point({x}, {y}) and clicking it: \n{traceback.format_exc()}")

    def _randomize_point(self, x: int, y: int, image_name: str):
        """Randomize the clicking location in an attempt to avoid clicking the same location that may make the bot look suspicious.

        Args:
            x (int): X coordinate on the screen of the center of the match location.
            y (int): Y coordinate on the screen of the center of the match location.
            image_name (str): File name of the image in /images/buttons/ folder.

        Returns:
            (int, int): Tuple of the newly randomized location to click.
        """
        try:
            # Get the width and height of the template image.
            width, height = self._game.image_tools.get_button_dimensions(image_name)

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
        except Exception:
            self._game.print_and_save(f"\n[ERROR] Bot encountered exception attempting to randomize point: \n{traceback.format_exc()}")

    def scroll_screen(self, x: int, y: int, scroll_clicks: int):
        """Attempt to scroll the screen to reveal more UI elements from the provided x and y coordinates.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            scroll_clicks (int): How much to scroll the screen. Positive for scrolling up and negative for scrolling down.

        Returns:
            None
        """
        if self._debug_mode:
            self._game.print_and_save(f"[DEBUG] Now scrolling the screen from ({x}, {y}) by {scroll_clicks} clicks...")

        try:
            self.move_to(x, y)

            if self._enable_bezier_curve:
                # Reset the pause delay back to 0.25, primarily for ImageUtils' methods using pyautogui.
                pyautogui.PAUSE = 0.25

            pyautogui.scroll(scroll_clicks, x = x, y = y)
            return None
        except Exception:
            self._game.print_and_save(f"\n[ERROR] Bot encountered exception attempting to scroll the screen at Point({x}, {y}) by {scroll_clicks} clicks: \n{traceback.format_exc()}")

    def scroll_screen_from_home_button(self, scroll_clicks: int):
        """Attempt to scroll the screen using the "Home" button coordinates to reveal more UI elements.

        Args:
            scroll_clicks (int): How much to scroll the screen. Positive for scrolling up and negative for scrolling down.

        Returns:
            None
        """
        try:
            x = self._game.home_button_location[0]
            y = self._game.home_button_location[1] - 50

            if self._debug_mode:
                self._game.print_and_save(f"[DEBUG] Now scrolling the screen from the \"Home\" button's coordinates at ({x}, {y}) by {scroll_clicks} clicks...")

            self.move_to(x, y)

            if self._enable_bezier_curve:
                # Reset the pause delay back to 0.25, primarily for ImageUtils' methods using pyautogui.
                pyautogui.PAUSE = 0.25

            pyautogui.scroll(scroll_clicks, x = x, y = y)
            return None
        except Exception:
            self._game.print_and_save(f"\n[ERROR] Bot encountered exception attempting to scroll the screen from the \"Home\" button: \n{traceback.format_exc()}")

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
