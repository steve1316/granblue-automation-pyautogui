# Granblue Automation using Template Matching (It is like Full Auto, but with Full Customization!)

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub last commit](https://img.shields.io/github/last-commit/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub issues](https://img.shields.io/github/issues/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub pull requests](https://img.shields.io/github/issues-pr/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub](https://img.shields.io/github/license/steve1316/gfl-database?logo=GitHub)

This Python application is designed for educational research purposes on studying how to automate certain workflows via image template matching using PyAutoGUI and GuiBot. PyAutoGUI accomplishes this by taking over the mouse, hence why it is recommended to run this on a separate machine than the one that you use daily.

Screenshots are taken and cropped for PyAutoGUI to perform image template matching. This will determine where the bot is currently at and will inform the bot on what to do next from there. Should PyAutoGUI fail to template match, GuiBot will take over. I have found that on default settings, GuiBot performs admirably well compared to PyAutoGUI in terms of template matching.

There is a feature already in-game that can automate gameplay called "Semi/Full Auto" but does not offer any way to customize what each character does on a turn-by-turn basis. This program aims to provide that customization. Users can create their own combat scripts using predefined terms and can indicate which turns the bot will execute their script, somewhat akin to constructing pseudocode.

## Disclaimer

By downloading this program, you consent to your account potentially getting flagged for excessive farming and banned in the next banwave by KMR. I hold no responsibility for how much you use this program for. I trust you have the self-control necessary to only farm in a reasonable amount of time.

# Features

- [x] Customize what skills to use during each turn in a user-created plan. Users can select which plan to use when starting the bot.
- [x] A launchable GUI to keep track of logs and selecting what combat script to use.
- [x] Farm user-defined amounts of specified materials from Quest, Coop, Raid, Event, etc.
- [ ] A user-defined timer for how long the bot should run for.
- [x] Support for Quest navigation.
- [ ] Support for Coop navigation.
- [ ] Support for Raid navigation.
- [ ] Support for Event(s) navigation.
- [ ] Support for Guild Wars navigation.
- [ ] Grab room codes from specified raids using user-created Twitter Developer account to connect to their API to scrape user tweets.
- [ ] Alert for when anti-bot CAPTCHA pops up.

# TODO List (until 1.0 release)
## Backend
- [x] Save each message in the Queue to a list in memory. When frontend requests for a saved log file, save the list in memory to a new log file.
- [x] Clean up Combat Mode by having all absolute coordinates in variables at the top.
- [x] Consolidate all finding button and clicking it logic into one function.
- [x] Implement detection if party wiped during Combat Mode.
- [ ] Implement selection from list of Summons in order of most preferred to least. If none after several tries, pick the very first Summon randomly.
- [ ] (LOW PRIORITY - After 1.0) Remove all sys.exit() code.
- [ ] (LOW PRIORITY - After 1.0) Implement Special Quests navigation/items.
- [ ] (LOW PRIORITY - After 1.0) Implement Coop Quests navigation/items.
- [ ] (LOW PRIORITY - After 1.0) Implement Raid navigation/items.
	- [ ] (LOW PRIORITY - After 1.0) Implement Twitter room code scraper/parser.
	- [ ] (LOW PRIORITY - After 1.0) Implement Captcha detection.
- [ ] (LOW PRIORITY - After 1.0) Implement Event navigation/items.
- [ ] (LOW PRIORITY - After 1.0) Implement Guild Wars/Rise of the Beasts navigation/items.
- [ ] (LOW PRIORITY - After 1.0) Implement if-else logic for users to use in combat scripts.
- [ ] (LOW PRIORITY - After 1.0) Deal with any left-over TODOs.
- [ ] (LOW PRIORITY - After 1.0) Eventually remove dependency on Game class from ImageUtils and MouseUtils and move any relevant functionality over to the Game class.
## Frontend
- [x] Add a Save Logs button.
- [x] Add a Group/Party selector.
- [x] Add a Summons selector. (Maybe with pictures?)
- [x] Add a selector for the amount of the specified item to be farmed.
- [ ] (LOW PRIORITY - After 1.0) Implement a user-defined timer for how long the bot can run for.
- [ ] (LOW PRIORITY - After 1.0) Add Special Quest items.
- [ ] (LOW PRIORITY - After 1.0) Add Coop items.
- [ ] (LOW PRIORITY - After 1.0) Add Raid items.
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

