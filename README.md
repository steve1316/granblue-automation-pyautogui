# Granblue Automation using Template Matching (It is like Full Auto, but with Full Customization!)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub last commit](https://img.shields.io/github/last-commit/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub issues](https://img.shields.io/github/issues/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub pull requests](https://img.shields.io/github/issues-pr/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub](https://img.shields.io/github/license/steve1316/gfl-database?logo=GitHub)

This Python application is designed for educational research purposes on studying how to automate certain workflows via image template matching using PyAutoGUI and GuiBot. PyAutoGUI accomplishes this by taking over the mouse, hence why it is recommended to run this on a separate machine than the one that you use daily. This can be circumvented by running this on a virtual machine like VMWare Workstation Player so you can keep using your main computer without interruption.

Screenshots are taken and cropped for PyAutoGUI to perform image template matching. This will determine where the bot is currently at and will inform the bot on what to do next from there. Should PyAutoGUI fail to template match, GuiBot will take over. I have found that on default settings, GuiBot performs admirably well compared to PyAutoGUI in terms of template matching.

There is a feature already in-game that can automate gameplay called "Semi/Full Auto" but does not offer any way to customize what each character does on a turn-by-turn basis. This program's primary goal is to provide that customization. Users can create their own combat scripts using predefined case-insensitive keywords and can indicate which turns the bot will execute their script, somewhat akin to constructing pseudocode.

For example:
```
// This is a comment. The bot will ignore this line.
# This is also a comment.

Turn 1:
    // On Turn 1, the 6th summon will be summoned. The character on the first position will use their 
    // 2nd and then 4th skill. Then the character on the third position will use their 3rd skill. 
    // Finally, the bot will attack to end the turn.
    summon(6)
    character1.useSkill(2).useSkill(4)
    character3.useSkill(3)
end

# The bot will keep clicking the Attack button until it reaches the 5th turn.
// Keywords are case-insensitive. So long as you spell them correctly, the bot will 
// have no trouble reading your combat script.
tURn 5:
    CharActer2.USEskill(2)
end

// Use the exit keyword to leave the raid without retreating. Recommended if you are farming raids and 
// only want the bot to be in each raid for a certain number of turns before moving on to the next raid.
exit

```

# Table of Contents
- [Features](<#Features>)
- [TODO List](<#TODO-List>)
  - [Backend](<##Backend>)
  - [Combat Scripting](<##Combat-Scripting>)
  - [Frontend](<##Frontend>)
- [Requirements](<#Requirements>)
  - [Python Dependencies](<##Python-Dependencies-(make-sure-to-have-these-installed-before-moving-on-to-the-instructions)>)
- [Instructions](<#Instructions>)
  - [How to create a Combat Script](<###How-to-create-my-own-Combat-Script>)
  - [How to farm Raids](<#Instructions-for-the-Raid-component-of-this-application-(optional,-only-if-you-want-to-farm-Raids)>)
  - [Virtualization](<#Instructions-on-how-to-get-this-working-on-VMWare-Workstation-Player-or-a-similar-virtual-machine>)
- [Wiki](<#Wiki>)
- [Technologies used](<#Technologies-Used>)

## Disclaimer
By downloading this program, you consent to your account potentially getting flagged for excessive farming and banned in the next banwave by KMR. I hold no responsibility for how much you use this program for. I trust you have the self-control necessary to only farm in reasonable bursts of time.

# Features
- [x] Customize what skills to use during each turn in a user-created plan. Users can select which plan to use when starting the bot.
- [x] A launchable GUI to keep track of logs and selecting what combat script to use.
- [x] Farm user-defined amounts of specified materials from Quest, Coop, Raid, Event, etc.
- [ ] A user-defined timer for how long the bot should run for.
- [x] Support for Quest navigation.
- [x] Support for Coop navigation.
- [x] Support for Raid navigation.
  - [x] Grab room codes from specified raids using user-created Twitter Developer account to connect to their API to scrape user tweets.
  - [ ] Alert for when anti-bot CAPTCHA pops up.
- [ ] Support for Event(s) navigation.
- [ ] Support for Guild Wars navigation.
- [ ] Support for Arcarum (currently unknown as to whether I will tackle this. This has to come after I finish the rest of the planned features for me to consider this)

# TODO List
## Backend
- [x] ~~Save each message in the Queue to a list in memory. When frontend requests for a saved log file, save the list in memory to a new log file.~~
- [x] ~~Clean up Combat Mode by having all absolute coordinates in variables at the top.~~
- [x] ~~Consolidate all finding button and clicking it logic into one function.~~
- [x] ~~Implement detection if party wiped during Combat Mode.~~
- [ ] ~~Implement selection from list of Summons in order of most preferred to least. If none after several tries, pick the very first Summon randomly.~~ This is axed for now. Might come back to this after the rest of the TODO List is completed.
- [x] ~~(MEDIUM PRIORITY) Remove all sys.exit() code.~~
- [x] ~~(HIGH PRIORITY) Implement Special Quests navigation/items.~~
- [x] ~~(HIGH PRIORITY) Implement Coop Quests navigation.~~
  - [x] ~~(HIGH PRIORITY) Implement Coop items.~~
  - [x] ~~(HIGH PRIORITY) Link this Coop component from backend to frontend.~~
- [x] ~~(HIGH PRIORITY) Implement Raid navigation.~~
    - [x] ~~(MAX PRIORITY) Implement way to exit out of Raids via user script and implement checks for max of 3 on-going raids. Also check to see for pending rewards.~~
    - [x] ~~(MAX PRIORITY) Link Raid component from backend to frontend.~~
    - [x] ~~(HIGH PRIORITY) Implement items to farm in Raids.~~
	- [x] ~~(HIGH PRIORITY) Implement Twitter room code scraper/parser.~~
	- [ ] (HIGH PRIORITY) Implement Captcha detection.
	- [x] ~~(MAX PRIORITY) Create instructions on how to create a Twitter Developer account for the Raid component and have the user set the keys into a text file in the project folder.~~
- [ ] (LOW PRIORITY) Implement Event navigation/items.
- [ ] (LOW PRIORITY) Implement Guild Wars/Rise of the Beasts navigation/items.
- [ ] (LOW PRIORITY) Deal with any left-over TODOs.
- [x] ~~(MEDIUM PRIORITY) Implement try-excepts to inform users of when errors occur.~~
- [ ] (LOW PRIORITY) Eventually remove dependency on Game class from ImageUtils and MouseUtils and move any relevant functionality over to the Game class.
- [x] ~~(MAX PRIORITY) Because this project was developed on a 1440p monitor, anything less or more than that would break the image processing. All image processing in this project needs to be generalized such that it would not matter whether the user has a 1440p or a 1080p monitor, they would get both get the same results.~~
- [ ] (LOW PRIORITY) Create instructions for Linux if it is confirmed to be supported.
- [x] ~~(MEDIUM PRIORITY) Create a Wiki in GitHub detailing the usage of this program and provide more documentation on the combat script capability that users can achieve.~~
  - [ ] (LOW PRIORITY) Create a page in the Wiki detailing what quests/raids/items that the program currently supports.

## Combat Scripting
- [ ] (LOW PRIORITY) Implement if-else logic for users to use in combat scripts.
  - [ ] (LOW PRIORITY) Implement HP/Overdrive/Break status checking in combat scripts.
- [ ] (LOW PRIORITY) Implement targeting for skills that require the user to select a target in combat scripts (enemies or own characters).

## Frontend
- [x] ~~Add a Save Logs button.~~
- [x] ~~Add a Group/Party selector.~~
- [x] ~~Add a Summons selector. (Maybe with pictures?)~~
- [x] ~~Add a selector for the amount of the specified item to be farmed.~~
- [ ] (MEDIUM PRIORITY) Implement a user-defined timer for how long the bot can run for.
- [x] ~~(HIGH PRIORITY) Add Special Quest items.~~
- [x] ~~(HIGH PRIORITY) Add Coop items.~~
- [x] ~~(HIGH PRIORITY) Add Raid items.~~
# Requirements
1. [Python 3.8.3+](https://www.python.org/downloads/release/python-383/)
2. [Granblue Fantasy account](http://game.granbluefantasy.jp/)
3. [Twitter Developer account (needed to farm Raids)](https://developer.twitter.com/en)
4. [VMware Workstation Player (optional, if your computer is strong enough to support virtualization)](https://www.vmware.com/products/workstation-player.html)

## Python Dependencies (make sure to have these installed before moving on to the instructions)
```
# Execute this command in a terminal opened in the project folder to install all of these requirements.

pip install -r requirements.txt
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

   - For Mac: I do not have a Mac system so I do not know how they invoke python. Please look online on how to do that for yourself.
5. Continue by following the instructions that are now shown to you by heading to the Settings and fill out each section. At the end, you will be notified when the program is ready to begin.
6. (Optional) Check out the config.ini in the root of the project folder and see what internal settings you would like to change before starting.

---
### How to create my own Combat Script
- Visit the [Combat Scripting Documentation and Examples wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Combat-Scripting-Documentation-and-Examples) for combat scripting usage and examples.

---

### Instructions for the Raid component of this application (optional, only if you want to farm Raids)
In order to get a Twitter Developer account, you need a Twitter account. Recommended to use the one bound to your GBF account just to keep it all in one place.
1. Head to https://developer.twitter.com/en/apply-for-access and click "Apply for a developer account".
2. Select "Hobbyist" and then "Exploring the API" and click "Get Started".
3. If you have not already, add a valid phone number to your account. Now fill out the form and select "Some Experience" for your coding experience and then click "Next".
4. In the first textbox, state your intention on exploring the Twitter API for educational purposes and using what you learned to develop a Python application. You can either craft your own response based on mine below or copy it outright:

`
I want to develop a Python application for a mobile Japanese game called Granblue Fantasy that uses tweepy and I want to explore what the Twitter Standard API 1.1 has to offer for me. I plan to use what I learn and apply it to the application so that it can search tweets made by users from the game in the past 24 hours based on user-created queries and parse specific text in the tweets. This is for educational purposes only.
`

5. Check Yes for "Are you planning to analyze Twitter data?" and either craft your own response based on mine below or copy it outright:

`
The application will allow the users to look up tweets made in the past 24 hours while searching for tweets that have specific text or keywords in the tweets. It will then return and display those tweets onto the application's GUI.
`

6. Uncheck the rest of the options and then click "Next".
7. Accept the "Developer agreement & policy" and click "Submit Application".
8. Once you verify the email sent to you, either two things will happen:
   - You get accepted immediately and can get started on Step 9.
   - You have to wait for Twitter to approve your application.
9. Once you get accepted, head over to https://developer.twitter.com/en/portal/dashboard and click on "Projects & Apps" on the left sidebar and click on "+ Create App".
10.  Give a name to your app. For example, mine is called `GBF Battle ID Finder` and click "Complete".
11.  Now click on "App Settings" at the bottom. Then click on "Keys and tokens" at the top.
12.  Click "Regenerate" for Consumer Keys and copy the API key and the API key secret into their respective places in config.ini in the root of the project folder. After that, click "Yes, I saved them".
13.  Now click "Generate" for "Access token & secret". Again, copy these 2 tokens into their respective places in config.ini and after that, click "Yes, I saved them".
14.  After that, the bot is now ready to access the Twitter API to look for raids.

---

### Instructions on how to get this working on VMWare Workstation Player or a similar virtual machine
1. Download and install VMWare Workstation Player.
2. Download a Windows 10 .iso from the official Microsoft website, https://www.microsoft.com/en-us/software-download/windows10
3. Create a new virtual machine with the following settings:
	- At least 4096MB of RAM is recommended.
	- 4 processor cores is recommended.
	- At least 30GB of space reserved.
4. Boot up the virtual machine using the Windows 10 .iso and install Windows 10. After that, install VMWare Tools to give the virtual machine full processing capability by going up to Player at the top left and then going to Manage -> Install VMWare Tools. Otherwise, the virtual machine will run choppy.
5. Set the display resolution to be 1920x1080 or higher. You can set it lower, but I cannot guarantee that it will run smoothly at lower resolutions.
6. After that, download the project folder into the virtual machine and follow the instructions to start the application.

# Wiki
Visit https://github.com/steve1316/granblue-automation-pyautogui/wiki for detailed documentation and examples.

# Technologies Used
1. [Python - The main language](https://www.python.org/)
2. [Qt - Application development framework for the GUI](https://www.qt.io/product/development-tools)
3. [PyAutoGUI - For image template matching and mouse control](https://pyautogui.readthedocs.io/en/latest/)
4. [GuiBot - For image template matching if PyAutoGui fails](https://guibot.readthedocs.io/en/latest/README.html)
5. [OpenCV-Python - Provides the confidence (accuracy) argument for PyAutoGUI](https://pypi.org/project/opencv-python/)
6. [EasyOCR - For text recognition and detection](https://github.com/JaidedAI/EasyOCR)
7. [Twitter Standard API 1.1 - For searching and parsing texts for Raid room codes to join](https://developer.twitter.com/en/docs/twitter-api/v1)
8. [VMWare Workstation Player - For virtualizing the program to circumvent control of the main cursor](https://www.vmware.com/products/workstation-player.html)

