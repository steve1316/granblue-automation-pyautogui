import datetime
from timeit import default_timer as timer

import pyautogui


class MouseUtils:
    """
    Provides the utility functions needed to perform mouse-related actions.

    Attributes
    ----------
    starting_time (float): Used to keep track of the program's elapsed time for logging purposes.

    mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.5.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to True.

    """

    def __init__(self, starting_time: float, mouse_speed: float = 0.5, debug_mode: bool = False):
        super().__init__()

        self.starting_time = starting_time

        self.mouse_speed = mouse_speed
        self.debug_mode = debug_mode

    def printtime(self):
        """Formats the time since the bot started into a readable, printable HH:MM:SS format using timedelta.

        Returns:
            str: A formatted string that displays the elapsed time since the bot started.
        """
        return str(datetime.timedelta(seconds=(timer() - self.starting_time))).split('.')[0]

    def move_to(self, x: int, y: int, custom_mouse_speed: float = 0.0):
        """Move the cursor to the coordinates on the screen.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            custom_mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.

        Returns:
            None
        """
        if (custom_mouse_speed <= 0.0):
            custom_mouse_speed = self.mouse_speed

        pyautogui.moveTo(x, y, custom_mouse_speed)
        return None

    def move_to_instantly(self, x: int, y: int):
        """Move the cursor instantly to the coordinates on the screen.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.

        Returns:
            None
        """
        pyautogui.moveTo(x, y)
        return None

    def move_and_click_point(self, x: int, y: int, custom_mouse_speed: float = 0.0, mouse_clicks=1):
        """Move the cursor to the specified point on the screen and clicks it.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            custom_mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.

        Returns:
            None
        """
        if (custom_mouse_speed <= 0.0):
            custom_mouse_speed = 0.0

        pyautogui.moveTo(x, y, custom_mouse_speed)
        pyautogui.click(clicks=mouse_clicks)
        return None

    def click_point_instantly(self, x: int, y: int):
        """Click the specified point on the screen instantly.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.

        Returns:
            None
        """
        pyautogui.click(x, y)
        return None

    def scroll_screen(self, x: int, y: int, scroll_clicks: int):
        """Attempt to scroll the screen to reveal more UI elements from the provided x and y coordinates.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            scroll_clicks (int): How much to scroll the screen. Positive for scrolling up and negative for scrolling down.

        Returns:
            None
        """
        if(self.debug_mode):
            print(f"{self.printtime()} [DEBUG] Now scrolling the screen from ({x}, {y}) by {scroll_clicks} clicks...")

        self.move_to(x, y)
        pyautogui.scroll(scroll_clicks, x=x, y=y)
        return None
