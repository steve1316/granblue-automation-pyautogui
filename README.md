# Granblue Automation using Template Matching (It is like Full Auto, but with Full Customization!)

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub last commit](https://img.shields.io/github/last-commit/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub issues](https://img.shields.io/github/issues/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub pull requests](https://img.shields.io/github/issues-pr/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub](https://img.shields.io/github/license/steve1316/gfl-database?logo=GitHub)

This Python application is designed for educational research purposes on studying how to automate certain workflows via image template matching using PyAutoGUI and GuiBot. PyAutoGUI accomplishes this by taking over the mouse, hence why it is recommended to run this on a separate machine than the one that you use daily.

Screenshots are taken and cropped for PyAutoGUI to perform image template matching. This will determine where the bot is currently at and will inform the bot on what to do next from there. Should PyAutoGUI fail to template match, GuiBot will take over. I have found that on default settings, GuiBot performs admirably well compared to PyAutoGUI in terms of template matching.

There is a feature already in-game that can automate gameplay called "Semi/Full Auto" but does not offer any way to customize what each character does on a turn-by-turn basis. This program aims to provide that customization. Users can create their own combat scripts using predefined terms and can indicate which turns the bot will execute their script, somewhat akin to constructing pseudocode.

## Disclaimer

By downloading this program, you consent to your account potentially getting flagged for excessive farming and banned in the next banwave by KMR. I hold no responsibility for how much you use this program for. I trust you have the self-control necessary to only farm in a reasonable amount of time.

# Features

- [x] Customize what skills to use during each turn in a user-created plan. Users can select which plan to use when starting the bot.
- [ ] A launchable GUI to keep track of logs and selecting what combat script to use.
- [ ] Farm certain amounts of specified materials.
- [ ] A settable timer to stop the bot.
- [ ] Support for Quest navigation.
- [ ] Support for Coop navigation.
- [ ] Support for Raid navigation.
- [ ] Support for Event(s) navigation.
- [ ] Support for Guild Wars navigation.
- [ ] Grab room codes from specified raids using user-created Twitter Developer account to connect to their API to scrape user tweets.
- [ ] Alert for when anti-bot CAPTCHA pops up.

# TODO (in order from greatest priority to least)

- [x] Add support for Summons in combat scripts.

- [ ] [IN-PROGRESS] Create a launchable GUI that users can start and stop the bot, select which combat script to use, which mission/raid to do, and view logs.

- [ ] Setup the Twitter scrapper for raid codes.

- [ ] Add support for popular Quest farming spots for materials.

- [ ] Add support for Raids.

- [ ] Add support for Guild Wars and Rise of the Beasts.

- [ ] Add support for Coop.

- [ ] Add support for Events.

- [ ] Setup an alert for when the bot detects anti-bot CAPTCHA.

# Requirements

1. Python 3.8+ [Get it here](https://www.python.org/downloads/)
2. Granblue Fantasy account.
3. Twitter Developer account.
4. More to be included soon...

# Instructions

This section will be filled out when basic functionality has been achieved.

# Technologies to be Used

1. [Python - The main language](https://www.python.org/)
2. [Qt - Application development framework for the GUI](https://www.qt.io/product/development-tools)
3. [PyAutoGUI - For image template matching and mouse control](https://pyautogui.readthedocs.io/en/latest/)
4. [GuiBot - For image template matching if PyAutoGui fails](https://guibot.readthedocs.io/en/latest/README.html)
5. [OpenCV-Python - Provides the confidence (accuracy) argument for PyAutoGUI](https://pypi.org/project/opencv-python/)

