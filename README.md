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
- [x] Support for Raid navigation.
- [ ] Support for Event(s) navigation.
- [ ] Support for Guild Wars navigation.
- [x] Grab room codes from specified raids using user-created Twitter Developer account to connect to their API to scrape user tweets.
- [ ] Alert for when anti-bot CAPTCHA pops up.

# TODO List
## Backend
- [x] ~~Save each message in the Queue to a list in memory. When frontend requests for a saved log file, save the list in memory to a new log file.~~
- [x] ~~Clean up Combat Mode by having all absolute coordinates in variables at the top.~~
- [x] ~~Consolidate all finding button and clicking it logic into one function.~~
- [x] ~~Implement detection if party wiped during Combat Mode.~~
- [ ] ~~Implement selection from list of Summons in order of most preferred to least. If none after several tries, pick the very first Summon randomly.~~ This is axed for now. Might come back to this after the rest of the TODO List is completed.
- [ ] (MEDIUM PRIORITY) Remove all sys.exit() code.
- [x] ~~(HIGH PRIORITY) Implement Special Quests navigation/items.~~
- [ ] (HIGH PRIORITY) Implement Coop Quests navigation/items.
- [x] ~~(HIGH PRIORITY) Implement Raid navigation.~~
    - [ ] (MAX PRIORITY) Link Raid component from backend to frontend.
    - [ ] (HIGH PRIORITY) Implement items to farm in Raids. (IN-PROGRESS)
	- [x] ~~(HIGH PRIORITY) Implement Twitter room code scraper/parser.~~
	- [ ] (HIGH PRIORITY) Implement Captcha detection.
- [ ] (LOW PRIORITY) Implement Event navigation/items.
- [ ] (LOW PRIORITY) Implement Guild Wars/Rise of the Beasts navigation/items.
- [ ] (LOW PRIORITY) Implement if-else logic for users to use in combat scripts.
- [ ] (LOW PRIORITY) Deal with any left-over TODOs.
- [ ] (MEDIUM PRIORITY) Implement try-catches to inform users of when errors occur.
- [ ] (LOW PRIORITY) Eventually remove dependency on Game class from ImageUtils and MouseUtils and move any relevant functionality over to the Game class.
- [x] ~~(MAX PRIORITY) Because this project was developed on a 1440p monitor, anything less or more than that would break the image processing. All image processing in this project needs to be generalized such that it would not matter whether the user has a 1440p or a 1080p monitor, they would get both get the same results.~~
## Frontend
- [x] ~~Add a Save Logs button.~~
- [x] ~~Add a Group/Party selector.~~
- [x] ~~Add a Summons selector. (Maybe with pictures?)~~
- [x] ~~Add a selector for the amount of the specified item to be farmed.~~
- [ ] (MEDIUM PRIORITY) Implement a user-defined timer for how long the bot can run for.
- [x] ~~(HIGH PRIORITY) Add Special Quest items.~~
- [ ] (HIGH PRIORITY) Add Coop items.
- [ ] (HIGH PRIORITY) Add Raid items. (IN-PROGRESS)
# Requirements
1. [Python 3.8.3+](https://www.python.org/downloads/release/python-383/)
2. [Granblue Fantasy account](http://game.granbluefantasy.jp/)
3. [Twitter Developer account (not required for now)](https://developer.twitter.com/en)
4. More to be included soon...

## Python Dependencies (make sure to have these installed before moving on to the instructions)
```
// Execute this line in your terminal opened up in the root of the project folder to install all of the following dependencies at once.
// For Windows:
pip install -r requirements.txt

// For Linux (with some additional necessary commands):
// Note: Linux is unsupported for now. These needs further testing..
// pip3 install -r requirements_linux.txt
// sudo apt-get install python3-tk python3-dev
// sudo apt-get install qt5-default
// pip3 uninstall opencv-python
// pip3 install opencv-python-headless
// sudo apt-get install msttcorefonts // Might be unnecessary.
```

- [PyTorch 1.7.1](https://pytorch.org/) (Installing the CUDA version will improve the speed of template matching if you have a CUDA-compatible GPU)
- [GuiBot 0.41.1+](https://pypi.org/project/guibot/)
- [PyAutoGUI 0.9.52+](https://pypi.org/project/PyAutoGUI/)
- [EasyOCR 1.2.1+](https://pypi.org/project/easyocr/)
- [PySide2 5.15.2+](https://pypi.org/project/PySide2/)
- [PyYAML 5.3.1+](https://pypi.org/project/PyYAML/)
- [autopy 4.0.0+](https://pypi.org/project/autopy/)
- [tweepy 3.10.0+](https://pypi.org/project/tweepy)

# Instructions
1. Download the entire project folder.
2. Make sure you installed the project dependencies by having Python 3.8.3+ installed and ran `pip install -r requirements.txt` in a terminal.
3. Open up the game on a Chromium-based browser and log in if you haven't already done so. Click away any daily log in popups until you are at the Main/Home screen.
4. Now open up the program in the following ways for each OS:
   - For Windows: Open up the terminal in the root of the project folder and type:
	```
	python main.py
	```
   - For Linux: Open up the terminal in the root of the project folder and type:
	```
	// Note: Linux is unsupported for now...
	python3 main.py
	```
   - For Mac: I do not have a Mac system so I do not know how they invoke python. Please look online on how to do that for yourself.
4. Continue by following the instructions that are now shown to you by heading to the Settings and fill out each section. At the end, you will be notified when the program is ready to begin.

# Technologies to be Used
1. [Python - The main language](https://www.python.org/)
2. [Qt - Application development framework for the GUI](https://www.qt.io/product/development-tools)
3. [PyAutoGUI - For image template matching and mouse control](https://pyautogui.readthedocs.io/en/latest/)
4. [GuiBot - For image template matching if PyAutoGui fails](https://guibot.readthedocs.io/en/latest/README.html)
5. [OpenCV-Python - Provides the confidence (accuracy) argument for PyAutoGUI](https://pypi.org/project/opencv-python/)
6. [EasyOCR - For text recognition and detection](https://github.com/JaidedAI/EasyOCR)

