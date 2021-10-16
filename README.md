# Granblue Automation using Template Matching (It is like Full Auto, but with Full Customization!)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub last commit](https://img.shields.io/github/last-commit/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub issues](https://img.shields.io/github/issues/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub pull requests](https://img.shields.io/github/issues-pr/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub](https://img.shields.io/github/license/steve1316/granblue-automation-pyautogui?logo=GitHub)

> Discord here: https://discord.gg/5Yv4kqjAbm

> Android version here: https://github.com/steve1316/granblue-automation-android

https://user-images.githubusercontent.com/18709555/118408116-db622c00-b638-11eb-9a24-5edc59cef34e.mp4

This Python application is designed for educational research purposes on studying how to automate certain workflows via image template matching using PyAutoGUI. PyAutoGUI accomplishes this by taking over the mouse, hence why it is recommended to run this on a separate machine than the one that you use daily. This can be circumvented by running this on a virtual machine like VMWare Workstation Player so you can keep using your main computer without interruption.

Screenshots are taken and cropped for PyAutoGUI to perform image template matching. This will determine where the bot is currently at and will inform the bot on what to do next from there.

There is a feature already in-game that can automate gameplay called "Semi/Full Auto" but does not offer any way to customize what each character does on a turn-by-turn basis. This program's primary goal is to provide that customization. Users can create their own combat scripts using predefined case-insensitive keywords and can indicate which turns the bot will execute their script, somewhat akin to constructing pseudocode.

For example:
```
// This is a comment. The bot will ignore this line.
# This is also a comment.

Turn 1:
    // On Turn 1, the following commands will be executed in order:
    // 6th Summon is invoked, character 1 uses Skill 2 and then Skill 4,
    // and finally character 3 uses Skill 3.
    summon(6)
    character1.useSkill(2).useSkill(4)
    character3.useSkill(3)
end

# The bot will keep clicking the Attack button until it reaches the 5th turn.
Turn 5:
    character2.useSkill(2)
end

// Use the exit keyword to leave the raid without retreating.
// Useful when you want to farm multiple raids at once.
exit

```

## Disclaimer
By downloading this program, you consent to your account potentially getting flagged for excessive amounts of farming for multiple hours straight and banned in the next banwave by KMR. I hold no responsibility for how much or how long you use this program for. I trust you have the self-control necessary to only farm in reasonable bursts of time with breaks in between and to always be alert for when the bot encounters the CAPTCHA.

# Table of Contents
- [Features](#features)
- [Wiki](#wiki)
- [Requirements](#requirements)
  - [Python Dependencies (make sure to have these installed before moving on to the instructions)](#python-dependencies-make-sure-to-have-these-installed-before-moving-on-to-the-instructions)
- [Instructions](#instructions)
  - [Instructions to set up Discord integration](#instructions-to-set-up-discord-integration)
  - [How to create my own Combat Script?](#how-to-create-my-own-combat-script)
  - [What Missions/Items/Summons are supported?](#what-missionsitemssummons-are-supported)
  - [Instructions for farming Raids (optional, only if you want to farm Raids)](#instructions-for-farming-raids-optional-only-if-you-want-to-farm-raids)
  - [Virtual Machine Setup (optional)](#virtual-machine-setup-optional)
- [Technologies Used](#technologies-used)

# Features
- [x] Customize what skills to use during each turn in a user-created plan. Users can select which plan to use when starting the bot.
- [x] A launchable GUI to keep track of logs, adjust settings and selecting what combat script to use.
- [x] Farm user-defined amounts of specified materials from the supported Farming Modes.
- [x] A user-defined timer for how long the bot should run for.
- [x] Support for the following game modes:
    - [x] Quest
    - [x] Special
    - [x] Coop
    - [x] Raid
    - [x] Event
    - [x] Guild Wars
    - [x] Rise of the Beasts
    - [x] Dread Barrage
    - [x] Proving Grounds
    - [x] Xeno Clash
    - [x] Arcarum
- [x] Alert for when anti-bot CAPTCHA pops up.
- [x] Discord integration for informing you of status updates like loot drops via private DMs.

# Wiki
Visit the [Wiki here](https://github.com/steve1316/granblue-automation-pyautogui/wiki) for detailed documentation and examples.

# Requirements
1. [Python 3.8.3 (any version higher than this breaks PyTorch)](https://www.python.org/downloads/release/python-383/)
2. [Granblue Fantasy account](http://game.granbluefantasy.jp/)
3. [Twitter Developer account (optional, needed to farm Raids)](https://developer.twitter.com/en)
4. [VMware Workstation Player (optional, if your computer is strong enough to support virtualization)](https://www.vmware.com/products/workstation-player.html)

## Python Dependencies (make sure to have these installed before moving on to the instructions)
```
# Execute this command in a terminal opened in the project folder to install all of these requirements.

pip install -r requirements.txt
```
- [PyTorch 1.7.1](https://pytorch.org/) (Installing the CUDA version will improve the speed of template matching if you have a CUDA-compatible GPU)
- [PyAutoGUI 0.9.52+](https://pypi.org/project/PyAutoGUI/)
- [EasyOCR 1.2.1+](https://pypi.org/project/easyocr/)
- [PySide2 5.15.2+](https://pypi.org/project/PySide2/)
- [PyYAML 5.3.1+](https://pypi.org/project/PyYAML/)
- [tweepy 3.10.0+](https://pypi.org/project/tweepy)
- [pyclick 0.0.2+](https://pypi.org/project/pyclick/)
- [playsound 1.2.2+](https://pypi.org/project/playsound/)
- [pyperclip 1.8.1+](https://pypi.org/project/pyperclip/)
- [discord.py 1.7.3+](https://pypi.org/project/discord.py/)
- [opencv-python 4.5.1.48+](https://pypi.org/project/opencv-python/)

# Instructions
1. Download the entire project folder.
2. Make sure you installed the project dependencies by having Python 3.8.3+ installed and ran `pip install -r requirements.txt` in a terminal.
3. Open up the game on a Chromium-based browser and log in if you haven't already done so. Click away any daily log in popups until you are at the Main/Home screen.
   1. Make sure the window size is set to this or else the bot will not be able to detect the "Home" button:
    
        ![Correct Window Size](images/readme_assets/correct_window_size.png)
4. Now open up the program in the following ways for each OS:
   - For Windows: Open up the terminal in the root of the project folder and type:
	```
	python main.py
	```

   - For Mac: I do not have a Mac system so I do not know how they invoke python. Please look online on how to do that for yourself.
5. Continue by following the instructions that are now shown to you by heading to the Settings and fill out each section. At the end, you will be notified when the program is ready to begin.
6. (Optional) Check out the ```config.ini``` in the root of the project folder and see what internal settings you would like to change before starting. Some of these settings include mouse settings (Bezier Curve or non-Bezier Curve), Twitter API settings, Dimensional Halo settings, etc.

---
## Instructions to set up Discord integration
- Visit the [Instructions for Discord integration wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Instructions-for-Discord-integration) for setting up the program notifying you of status updates like loot drops via private DMs.

---
## How to create my own Combat Script?
- Visit the [Combat Scripting Documentation and Examples wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Combat-Scripting-Documentation-and-Examples) for combat scripting usage and examples.
---
## What Missions/Items/Summons are supported?
- Visit the [List of Supported Missions and their Farmable Items wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/List-of-Supported-Missions-and-their-Farmable-Items) for supported content.
- Visit the [Selectable Summons wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Selectable-Summons) for available Summons.
---

## Instructions for farming Raids (optional, only if you want to farm Raids)
- Visit the [Instructions for Farming Raids wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Instructions-for-Farming-Raids) for setting up Raid farming.

---

## Virtual Machine Setup (optional)
- Visit the [Virtual Machine Setup wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Virtual-Machine-Setup) for setting up a Virtual Machine to run this program on.

# Technologies Used
1. [Python - The main language](https://www.python.org/)
2. [Qt - Application development framework for the GUI](https://www.qt.io/product/development-tools)
3. [PyAutoGUI - For image template matching and mouse control](https://pyautogui.readthedocs.io/en/latest/)
4. [pyclick - For making mouse movements human-like via Bezier Curves](https://pypi.org/project/pyclick/)
5. [OpenCV-Python - Provides the confidence (accuracy) argument for PyAutoGUI](https://pypi.org/project/opencv-python/)
6. [EasyOCR - For text recognition and detection](https://github.com/JaidedAI/EasyOCR)
7. [Twitter Standard API 1.1 - For searching and parsing texts for Raid room codes to join](https://developer.twitter.com/en/docs/twitter-api/v1)
8. [VMWare Workstation Player - For virtualizing the program to circumvent control of the main cursor](https://www.vmware.com/products/workstation-player.html)

