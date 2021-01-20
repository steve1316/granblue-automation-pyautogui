import datetime
from timeit import default_timer as timer

import pyautogui
import pyperclip


class MouseUtils:
    """
    Provides the utility functions needed to perform mouse-related actions.

    Attributes
    ----------
    game (game.Game): The Game object.
    
    starting_time (float): Used to keep track of the program's elapsed time for logging purposes.

    mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.2.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """

    def __init__(self, game, starting_time: float, mouse_speed: float = 0.2, debug_mode: bool = False):
        super().__init__()
        
        self.game = game

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
            custom_mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.0.

        Returns:
            None
        """
        if (custom_mouse_speed <= 0.0):
            custom_mouse_speed = self.mouse_speed

        pyautogui.moveTo(x, y, custom_mouse_speed, pyautogui.easeInOutQuad)
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
            custom_mouse_speed = self.mouse_speed

        pyautogui.moveTo(x, y, custom_mouse_speed, pyautogui.easeInOutQuad)
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
            self.game.print_and_save(f"{self.printtime()} [DEBUG] Now scrolling the screen from ({x}, {y}) by {scroll_clicks} clicks...")

        self.move_to(x, y)
        pyautogui.scroll(scroll_clicks, x=x, y=y)
        return None
    
    def scroll_screen_from_home_button(self, scroll_clicks: int):
        """Attempt to scroll the screen using the Home button coordinates to reveal more UI elements.

        Args:
            scroll_clicks (int): How much to scroll the screen. Positive for scrolling up and negative for scrolling down.

        Returns:
            None
        """
        x = self.game.home_button_location[0]
        y = self.game.home_button_location[1] - 50
        
        if(self.debug_mode):
            self.game.print_and_save(f"{self.printtime()} [DEBUG] Now scrolling the screen from the Home button's coordinates at ({x}, {y}) by {scroll_clicks} clicks...")

        self.move_to(x, y)
        pyautogui.scroll(scroll_clicks, x=x, y=y)
        return None
    
    def clear_textbox(self):
        """Clear the selected textbox of all text by selecting all text by CTRL + A and then pressing DEL.

        Returns:
            None
        """
        pyautogui.keyDown("ctrl")
        pyautogui.press("a")
        pyautogui.keyUp("ctrl")
        pyautogui.press("del")
        return None

    def copy_to_clipboard(self, message: str):
        """Copy the message to the clipboard.

        Args:
            message (str): The message to be copied.

        Returns:
            None
        """
        pyperclip.copy(message)
        return None
    
    def paste_from_clipboard(self):
        """Paste from the clipboard. Make sure that the textbox is already selected.

        Returns:
            None
        """
        message = pyperclip.paste()
        pyautogui.write(message)
        return None
