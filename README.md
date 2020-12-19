# Granblue Automation using PyAutoGUI (It is like Full Auto, but with Full Customization!)

This Python application is designed for educational research purposes on studying how to automate certain workflows via image template matching using PyAutoGUI. PyAutoGUI accomplishes this by taking over the mouse, hence why it is recommended to run this on a separate machine than the one that you use daily.

Screenshots are taken and cropped for PyAutoGUI to perform image processing. This will determine where the bot is currently at and will inform the bot on what to do next from there. 

There is a feature already in-game that can automate gameplay called "Semi/Full Auto" but does not offer any way to customize what each character does on a turn-by-turn basis. This program aims to provide that customization. Users can create their own combat scripts using predefined terms and can indicate which turns the bot will execute their script.

## Disclaimer

By downloading this program, you forfeit your account's safety during the use of this program. I accept no responsibility over any damages suffered to your account.

# Features

1. Customize what skills to use during each turn in a user-created plan. Users can select which plan to use when starting the bot. (DONE)
2. A launchable GUI to keep track of logs and selecting what combat script to use. (WIP)
3. Grab room codes from specified raids using user-created Twitter Developer account to connect to their API to scrape user tweets. (WIP)
4. Alert for when anti-bot CAPTCHA pops up. (WIP)
5. Support for Quest (WIP), COOP (WIP), Raid (WIP), and Guild Wars (WIP).

# TODO (in order from greatest priority to least) (WIP)

- [x] Add support for Summons in combat scripts.

- [ ] Create a launchable GUI that users can start and stop the bot, select which combat script to use, which mission/raid to do, and view logs.

- [ ] Setup the Twitter scrapper for raid codes.

- [ ] Add support for popular Quest farming spots for materials.

- [ ] Add support for Raids.

- [ ] Add support for Guild Wars and Rise of the Beasts.

- [ ] Add support for Coop.

- [ ] Add support for Events.

- [ ] Setup an alert for when the bot detects anti-bot CAPTCHA.

# Requirements (WIP)

1. Python 3.8+ [Get it here](https://www.python.org/downloads/)
2. Granblue Fantasy account.
3. Twitter Developer account.

# Instructions (WIP)

This section will be filled out when basic functionality has been achieved.

# Technologies to be Used (WIP)

1. [Python - The main language](https://www.python.org/)
2. [PyAutoGUI - For image template matching and mouse control](https://pyautogui.readthedocs.io/en/latest/)
3. [OpenCV-Python - Provides the confidence (accuracy) argument for PyAutoGUI](https://pypi.org/project/opencv-python/)

