import pyautogui
import time
import sys
# opencv-python package is necessary for the confidence (accuracy) argument for pyautogui's locating functions.
import cv2

# This Debug class deals in helping test the pyautogui's capability to find elements on the user's screen.


class Debug:
    def __init__(self, userDefinedMouseSpeed, userDefinedConfidence, debugMode=False):
        super().__init__()
        # The mouse speed that pyautogui will use.
        self.mouseSpeed = userDefinedMouseSpeed
        # The accuracy that pyautogui will use to match images on the screen.
        self.confidence = userDefinedConfidence
        # Controls whether or not the [DEBUG] messages should be displayed.
        self.debugMode = debugMode

        # Save the coordinates of the "Home" Button.
        self.homeButtonX = None
        self.homeButtonY = None

        # Save the coordinates of the "Attack" Button.
        self.attackButtonX = None
        self.attackButtonY = None

        # Save the region size of the game window to speed up pyautogui functionality instead of searching across the entire screen.
        self.windowLeft = None
        self.windowTop = None
        self.windowWidth = None
        self.windowHeight = None

    # Find the location of the specified button and then move the cursor to its position and click it.
    def findButton(self, buttonName, checkLocation=False, customTries=3):
        # If the bot needs to go to the Quest Screen, head back to the Home Screen.
        if (buttonName.lower() == "quest"):
            self.goBackToHome()

        if(self.debugMode):
            print(
                f"\n[DEBUG] Now attempting to find the {buttonName.upper()} Button from current position...")

        x, y = self.locate(buttonName, customTries=customTries)

        if(self.debugMode):
            print(
                f"[DEBUG] Found the {buttonName.upper()} Button at ({x}, {y})!")

        self.moveToAndClickPoint(x, y, mouseSpeed=self.mouseSpeed)

        if (checkLocation):
            self.confirmLocation(buttonName)

        self.accountForPing()

    # Attempt to locate the UI image across the entire screen and return the tuple of the center point of the position where the image was found.
    def locate(self, imageName, customTries=3):
        location = None
        tries = customTries

        while (location == None):
            if(self.windowLeft != None or self.windowTop != None or self.windowWidth != None or self.windowHeight != None):
                location = pyautogui.locateOnScreen(f"images/buttons/{imageName.lower()}.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            else:
                location = pyautogui.locateOnScreen(
                    f"images/buttons/{imageName.lower()}.png", confidence=self.confidence)

            if (location == None):
                tries -= 1

                # If the number of tries has been exhausted, the bot will return None.
                if (tries <= 0):
                    #print(f"[ERROR] Could not find {imageName.upper()} Button after several tries. Returning None...")
                    return None

                if(self.debugMode):
                    print(
                        f"[DEBUG] Locating {imageName.upper()} Button failed. Trying again in 5 seconds...")

                # Sleep for 5 seconds and try again.
                self.accountForPing(5)

        # Center the location and returns a tuple.
        centerLocation = pyautogui.center(location)

        # Recalibrate where the "Attack" Button is.
        if (imageName == "attack"):
            self.attackButtonX, self.attackButtonY = centerLocation

        return centerLocation

    # Wait the specified seconds to account for bad ping or loading.
    def accountForPing(self, seconds=3):
        time.sleep(seconds)

    # Confirm the bot's position by searching for their headers.
    def confirmLocation(self, locationName, customTries=3):
        # self.accountForPing(1)
        location = None
        tries = customTries

        # Recalibrate the game window if any of the dimensions are not defined.
        if(self.windowLeft == None or self.windowTop == None or self.windowWidth == None or self.windowHeight == None):
            self.calibrateGameWindow()

        while (location == None):
            location = pyautogui.locateOnScreen(f"images/headers/{locationName}Header.png", confidence=self.confidence, region=(
                self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            if (location == None):
                tries -= 1

                # Break out of the while loop with an error message.
                if (tries == 0):
                    #print(f"[ERROR] Could not confirm location for {locationName.upper()}.")
                    return False

                if(self.debugMode):
                    print(
                        f"[DEBUG] Bot's current location is not at {locationName.upper()}. Trying again in 5 seconds...")

                # Sleep for 5 seconds and try again.
                self.accountForPing(5)

        if(self.debugMode and location != None):
            print(
                f"[DEBUG] Bot's current location is at {locationName.upper()} Screen.")
        return True

    # Recalibrate the dimensions of the game window for pyautogui.
    def calibrateGameWindow(self):
        if(self.debugMode):
            print("\n[DEBUG] Now attempting to recalibrate the game window...")

        self.homeButtonX, self.homeButtonY = self.locate("home")

        # Recalibrate the region size of the game window for pyautogui.
        # TODO: Recalibrate based on "News" Button together with "Home" Button potentially for smaller sized screens. Need to get to Home Screen first.
        self.windowLeft = self.homeButtonX - 439
        self.windowTop = self.homeButtonY - 890
        self.windowWidth = self.windowLeft + 480
        self.windowHeight = self.windowTop + 917

    # Go back to the Home Screen to reset the bot's position. Also recalibrates the region size of the game window if necessary.
    def goBackToHome(self, confirmLocationCheck=False):
        if(self.debugMode):
            print("\n[DEBUG] Now attempting to move back to the Home Screen...")

        # Avoid expensive CPU operations on finding the "Home" Button if you already found it before. Update the dimensions of the game window as well.
        if(self.homeButtonX == None or self.homeButtonY == None):
            self.homeButtonX, self.homeButtonY = self.locate("home")
            print(
                f"[DEBUG] Found Home Button at ({self.homeButtonX}, {self.homeButtonY})!")

        # Recalibrate the region size of the game window for pyautogui.
        # TODO: Recalibrate based on "News" Button together with "Home" Button potentially for smaller sized screens. Need to get to Home Screen first.
        self.windowLeft = self.homeButtonX - 439
        self.windowTop = self.homeButtonY - 890
        self.windowWidth = self.windowLeft + 480
        self.windowHeight = self.windowTop + 917

        self.moveToAndClickPoint(
            self.homeButtonX, self.homeButtonY, mouseSpeed=self.mouseSpeed)

        if(confirmLocationCheck):
            self.confirmLocation("home")

    # Attempt to drag the screen down to reveal more UI elements by locating the Home button at the bottom.
    def scrollDown(self, scrollClicks):
        # Find the Home button on the bottom right of the bar at the base of the window.
        # self.findButton("home")

        # Now move the cursor slightly up and then scroll down based on the number of scrollClicks.
        if(self.debugMode):
            print("\n[DEBUG] Now scrolling the screen down...")
        pyautogui.moveTo(self.homeButtonX, self.homeButtonY -
                         100, self.mouseSpeed)
        pyautogui.scroll(scrollClicks)

        self.accountForPing(1)

    # Move the cursor to the specified point on the screen, click it, and then account for ping.
    def moveToAndClickPoint(self, x, y, mouseSpeed=1, delay=True):
        pyautogui.moveTo(x, y, mouseSpeed)
        pyautogui.click()
        if(delay):
            self.accountForPing(1)

    # Click the specified point on the screen instantly and then account for ping.
    def clickPointInstantly(self, x, y, delay=True):
        pyautogui.click(x, y)
        if(delay):
            self.accountForPing(1)

    # Select the specified element tab for summons. Search selected tabs first, then unselected tabs.
    # TODO: ALL images need to be segmented into Lite, Regular, and High to account for different Graphics Settings.
    def findSummonElement(self, summonElementName):
        summonElementLocation = None
        tries = 3
        if(self.debugMode):
            print(
                f"\n[DEBUG] Now attempting to find selected {summonElementName.upper()} Summon Element tab...")

        while (summonElementLocation == None):
            # Search for selected Fire Element Summon tab.
            if (summonElementName.lower() == "fire"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonFireSelected.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Water Element Summon tab.
            elif (summonElementName.lower() == "water"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonWaterSelected.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Earth Element Summon tab.
            elif (summonElementName.lower() == "earth"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonEarthSelected.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Wind Element Summon tab.
            elif (summonElementName.lower() == "wind"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonWindSelected.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Light Element Summon tab.
            elif (summonElementName.lower() == "light"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonLightSelected.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Dark Element Summon tab.
            elif (summonElementName.lower() == "dark"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonDarkSelected.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Misc Element Summon tab.
            elif (summonElementName.lower() == "misc"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonMiscSelected.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))

            # If searching for selected tabs did not work, search for unselected tabs.
            if (summonElementLocation == None):
                if(self.debugMode):
                    print(
                        f"[DEBUG] Locating selected {summonElementName.upper()} Summon Element tab failed. Trying again for unselected tab...")

                # Search for unselected Fire Element Summon tab.
                if (summonElementName.lower() == "fire"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonFire.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Water Element Summon tab.
                elif (summonElementName.lower() == "water"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonWater.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Earth Element Summon tab.
                elif (summonElementName.lower() == "earth"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonEarth.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Wind Element Summon tab.
                elif (summonElementName.lower() == "wind"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonWind.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Light Element Summon tab.
                elif (summonElementName.lower() == "light"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonLight.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Dark Element Summon tab.
                elif (summonElementName.lower() == "dark"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonDark.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Misc Element Summon tab.
                elif (summonElementName.lower() == "misc"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonMisc.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))

                # If searching both selected and unselected Summon Element tabs failed, try again until tries are depleted.
                if (summonElementLocation == None):
                    tries -= 1
                    if (tries == 0):
                        sys.exit(
                            f"[ERROR] Could not find {summonElementName.upper()} Summon Element tab after several tries. Exiting Program...")

        if(self.debugMode):
            print(
                f"[DEBUG] Locating {summonElementName.upper()} Summon Element tab was successful. Clicking it now...")

        # After locating the Summon Element Tab, click it.
        summonElementCenterLocation = pyautogui.center(summonElementLocation)
        x, y = summonElementCenterLocation
        self.moveToAndClickPoint(x, y, mouseSpeed=self.mouseSpeed)

    # Find the specified Summon on the Summon Selection Screen. This is called after the findSummonElement() method in order to select the correct Summon Element tab.
    def findSummon(self, summonName):
        summonLocation = None
        tries = 3
        if(self.debugMode):
            print(
                f"\n[DEBUG] Now attempting to find {summonName.upper()} Summon...")

        while (summonLocation == None):
            summonLocation = pyautogui.locateOnScreen(f"images/summons/{summonName.lower()}.png", confidence=self.confidence, region=(
                self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            if (summonLocation == None):
                if(self.debugMode):
                    print(
                        f"[DEBUG] Locating {summonName.upper()} Summon failed. Trying again in 2 seconds...")
                tries -= 1

                # If matching failed, scroll the screen down to see more Summons.
                self.scrollDown(-400)

                if (tries == 0):
                    sys.exit(
                        f"[ERROR] Could not find {summonName.upper()} Summon after several tries. Exiting Program...")

        if(self.debugMode):
            print(
                f"[DEBUG] Located {summonName.upper()} Summon successfully. Clicking it now...")

        # If the Summon was located, click it.
        x, y = pyautogui.center(summonLocation)
        self.moveToAndClickPoint(x, y, mouseSpeed=self.mouseSpeed)

    # Select the specified group and party. It will then start the mission.
    def findPartyAndStartMission(self, groupNumber, partyNumber):
        groupLocation = None
        tries = 3

        # Find the Group first. If the selected group number is less than 8, it is in Set A. Otherwise, it is in Set B.
        if(groupNumber < 8):
            if(self.debugMode):
                print(
                    f"\n[DEBUG] Now attempting to find Set A, Group {groupNumber}...")

            while (groupLocation == None):
                groupLocation = pyautogui.locateOnScreen(f"images/buttons/partySetA.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                if (groupLocation == None):
                    if(self.debugMode):
                        print(
                            f"[DEBUG] Locating Group {groupNumber} failed. Trying again in 5 seconds...")

                    # See if the user had Set B active instead of Set A if matching failed.
                    groupLocation = pyautogui.locateOnScreen(f"images/buttons/partySetB.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                    tries -= 1

                    if (tries == 0):
                        sys.exit(
                            f"[ERROR] Could not find Group {groupNumber} after several tries. Exiting Program...")

                    self.accountForPing(5)
        else:
            if(self.debugMode):
                print(
                    f"\n[DEBUG] Now attempting to find Set B, Group {groupNumber}...")

            while (groupLocation == None):
                groupLocation = pyautogui.locateOnScreen(f"images/buttons/partySetB.png", confidence=self.confidence, region=(
                    self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                if (groupLocation == None):
                    if(self.debugMode):
                        print(
                            f"[DEBUG] Locating Group {groupNumber} failed. Trying again in 5 seconds...")

                    # See if the user had Set A active instead of Set B if matching failed.
                    groupLocation = pyautogui.locateOnScreen(f"images/buttons/partySetA.png", confidence=self.confidence, region=(
                        self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                    tries -= 1

                    if (tries == 0):
                        sys.exit(
                            f"[ERROR] Could not find Group {groupNumber} after several tries. Exiting Program...")

                    self.accountForPing(5)

        # Center on the Set button and click the correct Group Number Tab.
        if(self.debugMode):
            print(
                f"[DEBUG] Successfully found the correct Set. Now selecting Group {groupNumber}...")
        if(groupNumber == 1):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(
                x - 350, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 2):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(
                x - 290, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 3):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(
                x - 230, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 4):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(
                x - 170, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 5):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(
                x - 110, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 6):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(
                x - 50, y + 50, mouseSpeed=self.mouseSpeed)
        else:
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(
                x + 10, y + 50, mouseSpeed=self.mouseSpeed)

        # Now select the correct Party.
        if(self.debugMode):
            print(
                f"[DEBUG] Successfully found Group {groupNumber}. Now selecting Party {partyNumber}...")
        if(partyNumber == 1):
            self.clickPointInstantly(x - 309, y + 325)
        elif(partyNumber == 2):
            self.clickPointInstantly(x - 252, y + 325)
        elif(partyNumber == 3):
            self.clickPointInstantly(x - 195, y + 325)
        elif(partyNumber == 4):
            self.clickPointInstantly(x - 138, y + 325)
        elif(partyNumber == 5):
            self.clickPointInstantly(x - 81, y + 325)
        elif(partyNumber == 6):
            self.clickPointInstantly(x - 24, y + 325)

        if(self.debugMode):
            print(
                f"[DEBUG] Successfully selected Party {partyNumber}. Now starting the mission.")

        # Find the "OK" Button to start the mission.
        self.findButton("ok")

    # TODO: Find a suitable OCR framework that can detect the HP % of the enemies. Until then, this bot will not handle if statements.
    # TODO: Maybe have it be in-line? Example: if(enemy1.hp < 70): character1.useSkill(3),character2.useSkill(1).useSkill(4),character4.useSkill(1),end
    # def executeConditionalStatement(self, i, target, line, lines):
    #     whiteSpaceIndex = line.index(" ")
    #     operator = ""
    #     # Perform conditional matching to find what operator is being used. Account for the whitespaces before and after the operator.
    #     if(line[whiteSpaceIndex:(whiteSpaceIndex + 3)] == " < "):
    #         operator = "<"
    #         print("[DEBUG] Operator is <")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 3)] == " > "):
    #         operator = ">"
    #         print("[DEBUG] Operator is >")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " <= "):
    #         operator = "<="
    #         print("[DEBUG] Operator is <=")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " >= "):
    #         operator = ">="
    #         print("[DEBUG] Operator is >=")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " == "):
    #         operator = "=="
    #         print("[DEBUG] Operator is ==")

    #     # Determine whether or not the conditional is met. If not, return the index right after the end for the if statement.

    #     # If conditional is met, execute each line until you hit end for the if statement.

    #     return i

    # Selects the portrait of the character specified on the screen. Also saves the position of the "Attack" Button.
    def selectCharacter(self, characterNumber):
        # Get the position of the center of the "Attack" button. If already found, don't call this expensive operation again.
        if(self.attackButtonX == None or self.attackButtonY == None):
            attackButtonCenterLocation = self.locate("attack")
            self.attackButtonX, self.attackButtonY = attackButtonCenterLocation

        if(self.debugMode):
            print(
                f"[DEBUG] Attack Button location: ({self.attackButtonX}, {self.attackButtonY})")

        if(characterNumber == 1):
            # Click the portrait of Character 1.
            #self.moveToAndClickPoint(self.attackButtonX - 317, self.attackButtonY + 123, mouseSpeed=self.mouseSpeed)
            self.clickPointInstantly(
                self.attackButtonX - 317, self.attackButtonY + 123)
        elif(characterNumber == 2):
            # Click the portrait of Character 2.
            #self.moveToAndClickPoint(self.attackButtonX - 240, self.attackButtonY + 123, mouseSpeed=self.mouseSpeed)
            self.clickPointInstantly(
                self.attackButtonX - 240, self.attackButtonY + 123)
        elif(characterNumber == 3):
            # Click the portrait of Character 3.
            #self.moveToAndClickPoint(self.attackButtonX - 158, self.attackButtonY + 123, mouseSpeed=self.mouseSpeed)
            self.clickPointInstantly(
                self.attackButtonX - 158, self.attackButtonY + 123)
        elif(characterNumber == 4):
            # Click the portrait of Character 4.
            #self.moveToAndClickPoint(self.attackButtonX - 76, self.attackButtonY + 123, mouseSpeed=self.mouseSpeed)
            self.clickPointInstantly(
                self.attackButtonX - 76, self.attackButtonY + 123)

    # Activate the skill specified for the already selected character.
    def useCharacterSkills(self, x, y, characterSelected, skill):
        if("useSkill(1)" in skill):
            print(f"[COMBAT] Character {characterSelected} uses Skill 1")
            #self.moveToAndClickPoint(x - 213, y + 171, mouseSpeed=self.mouseSpeed)
            self.clickPointInstantly(x - 213, y + 171)
        elif("useSkill(2)" in skill):
            print(f"[COMBAT] Character {characterSelected} uses Skill 2")
            #self.moveToAndClickPoint(x - 132, y + 171, mouseSpeed=self.mouseSpeed)
            self.clickPointInstantly(x - 132, y + 171)
        elif("useSkill(3)" in skill):
            print(f"[COMBAT] Character {characterSelected} uses Skill 3")
            #self.moveToAndClickPoint(x - 51, y + 171, mouseSpeed=self.mouseSpeed)
            self.clickPointInstantly(x - 51, y + 171)
        elif("useSkill(4)" in skill):
            print(f"[COMBAT] Character {characterSelected} uses Skill 4")
            #self.moveToAndClickPoint(x + 39, y + 171, mouseSpeed=self.mouseSpeed)
            self.clickPointInstantly(x + 39, y + 171)

    # Attempt to find the specified dialog window (usually from Lyria or Vyrn).
    def findDialog(self, dialogName, customTries=3):
        location = None
        tries = customTries

        while (location == None):
            location = pyautogui.locateOnScreen(f"images/dialogs/{dialogName.lower()}.png", confidence=self.confidence, region=(
                self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))

            if (location == None):
                tries -= 1

                # If the number of tries has been exhausted, the bot will return None.
                if (tries <= 0):
                    #print(f"[ERROR] Could not find {dialogName.upper()} Dialog after several tries. Returning None...")
                    return None

                if(self.debugMode):
                    print(
                        f"[DEBUG] Locating {dialogName.upper()} Dialog failed. Trying again in 5 seconds...")

                # Sleep for 5 seconds and try again.
                self.accountForPing(5)

        # Center the location and returns a tuple.
        centerLocation = pyautogui.center(location)

        return centerLocation

    # Start the Combat Mode with the given script name. Start reading through the text file line by line and have the bot proceed accordingly.
    # TODO: Readjust x and y window for locate() for faster processing for every error mismatch (maybe).
    def startCombatMode(self, scriptName):
        # Recalibrate the game window.
        self.calibrateGameWindow()

        # Open the text file and read all of the lines.
        try:
            script = open(f"scripts/{scriptName}.txt", "r")
            if(self.debugMode):
                print(f"\n[DEBUG] Now loading up {scriptName} Combat Plan.")
            lines = script.readlines()

            print("\n[COMBAT] Starting combat script.")

            i = 0  # Index for the lines list.
            lineNumber = 1  # Tells what line number the bot is reading.
            # Tells what turn it currently is for the script execution.
            turnNumber = 1

            # Loop through and execute each line in the combat script.
            while(True):
                line = lines[i]

                # Print each line read if debug mode is active.
                if(line[0] != "#" and line[0] != "/" and line.strip() != ""):
                    if(self.debugMode):
                        print(f"[DEBUG] Line {lineNumber}: {line.strip()}")

                # Check if there are dialog boxes from either Lyria or Vyrn and click them away.
                if(self.findDialog("lyriaDialog", customTries=1) != None):
                    print("[DEBUG] Detected Lyria dialog. Closing it now...")
                    lyriaDialogX, lyriaDialogY = self.findDialog(
                        "lyriaDialog", customTries=1)
                    self.clickPointInstantly(
                        lyriaDialogX + 180, lyriaDialogY - 51, delay=False)
                elif(self.findDialog("vyrnDialog", customTries=1) != None):
                    print("[DEBUG] Detected Vyrn dialog. Closing it now...")
                    vyrnDialogX, vyrnDialogY = self.findDialog(
                        "vyrnDialog", customTries=1)
                    self.clickPointInstantly(
                        vyrnDialogX + 180, vyrnDialogY - 51, delay=False)

                # If the execution reached the next turn block and it is currently not the correct turn, keep pressing "Attack" until turnNumber matches.
                if ("turn" in line.lower() and int(line[5]) != turnNumber):
                    if(self.debugMode):
                        print(
                            f"[DEBUG] Current Turn Number {turnNumber} does not match expected Turn Number {line[5]}. Pressing Attack Button until they do.")
                    while (int(line[5]) != turnNumber):
                        attackLocation = self.locate("attack", customTries=1)
                        self.clickPointInstantly(
                            self.attackButtonX, self.attackButtonY, delay=False)
                        self.accountForPing(7)

                        # Try to find the "Next" Button only once per turn.
                        nextLocation = self.locate("next", customTries=1)
                        if(nextLocation != None):
                            if(self.debugMode):
                                print(
                                    f"[DEBUG] Detected the Next Button. Clicking it now...")
                            nextX, nextY = nextLocation
                            self.clickPointInstantly(nextX, nextY, delay=False)
                            self.accountForPing(5)

                        # Increment the turn number by 1.
                        turnNumber += 1

                # If it is the start of the Turn and it is the correct turn currently, grab the next line for execution by incrementing the list index.
                if("turn" in line.lower() and int(line[5]) == turnNumber):
                    print(f"\n[COMBAT] Beginning Turn {line[5]}.\n")
                    i += 1

                    # Strip any leading and trailing whitespaces.
                    line = lines[i].strip()

                    # Determine which character will perform the action.
                    characterSelected = 0
                    if("character1" in line):
                        characterSelected = 1
                    elif("character2" in line):
                        characterSelected = 2
                    elif("character3" in line):
                        characterSelected = 3
                    elif("character4" in line):
                        characterSelected = 4

                    # Now perform the skill specified in the read string.
                    # TODO: Handle enemy targeting here as well.
                    if(characterSelected != 0):
                        # Select the character specified and return the tuple of the (x,y) coordinates of the "Attack" Button.
                        print(f"Character {characterSelected} acts.")
                        self.selectCharacter(characterSelected)

                        # Get all occurrences of "useSkill" and then click the skills specified in order from left to right. Then remove the first element as that is usually the character substring.
                        skills = line.split(".")
                        skills.pop(0)

                        # Loop through all occurrences and use the specified skills.
                        for skill in skills:
                            self.useCharacterSkills(
                                self.attackButtonX, self.attackButtonY, characterSelected, skill)

                        # Now click the Back button and wait 1 second.
                        self.clickPointInstantly(
                            self.attackButtonX - 322, self.attackButtonY, delay=False)
                        self.accountForPing(1)
                elif("end" in line):
                    # Increment by 1 to move to the next line for execution. After that, hit the "Attack" Button to end the turn.
                    # Note: The execution at this point will increment by 2 because of the incrementation after this elif statement so it is imperative that scripts have a space in between "end" and "Turn #:".
                    turnNumber += 1
                    i += 1
                    numberOfChargeAttacks = 0

                    # Check if any character has 100% Charge Bar. If so, add 0.5 seconds per each match.
                    listOfOugis = pyautogui.locateAllOnScreen("images/fullCharge.png", region=(
                        self.attackButtonX - 356, self.attackButtonY + 67, self.attackButtonX - 40, self.attackButtonY + 214))

                    for pos in listOfOugis:
                        numberOfChargeAttacks += 0.5

                    if (self.debugMode):
                        print(
                            f"[DEBUG] Number of Characters ready to ougi: {numberOfChargeAttacks}")
                        print(
                            f"[DEBUG] Clicking Attack Button now and waiting 7 seconds.")
                    self.clickPointInstantly(
                        self.attackButtonX, self.attackButtonY, delay=False)
                    self.accountForPing(7 + numberOfChargeAttacks)

                    # Try to find the "Next" Button only once per turn.
                    nextLocation = self.locate("next", customTries=1)
                    if(nextLocation != None):
                        if(self.debugMode):
                            print(
                                f"[DEBUG] Detected Next Button. Clicking it now...")
                        nextX, nextY = nextLocation
                        self.clickPointInstantly(nextX, nextY, delay=False)
                        self.accountForPing(5)

                # Break out if the user reached the "Quest Results" Screen.
                if (self.confirmLocation("expGained", customTries=1) != False):
                    print(
                        "[INFO] Bot has reached the Quest Results Screen. Breaking out of main loop...")
                    break

                # Increment by 1 to move to the next line for execution.
                lineNumber += 1
                i += 1

                # Break out of the while loop when EOF is reached.
                if(i >= len(lines)):
                    break

            # Keep pressing the location of the "Attack"/"Next" Button until the bot reaches the Quest Results Screen.
            print(
                "\n[COMBAT] Bot has reached end of script. Pressing Attack until battle ends.")
            while (self.confirmLocation("expGained", customTries=1) == False):
                attackLocation = self.locate("attack", customTries=1)
                nextLocation = self.locate("next", customTries=1)
                if(attackLocation != None):
                    self.clickPointInstantly(
                        self.attackButtonX, self.attackButtonY, delay=False)
                elif(nextLocation != None):
                    self.clickPointInstantly(
                        self.attackButtonX + 50, self.attackButtonY, delay=False)
                self.accountForPing(2)

            # Try to click any detected "OK" Buttons several times.
            print("[INFO] Bot has reached the Quest Results Screen.")
            while (True):
                if (self.confirmLocation("lootCollected", customTries=1)):
                    break

                # Check if there are dialog boxes from either Lyria or Vyrn and click them away.
                if(self.findDialog("lyriaDialog", customTries=1) != None):
                    print("[DEBUG] Detected Lyria dialog. Closing it now...")
                    lyriaDialogX, lyriaDialogY = self.findDialog(
                        "lyriaDialog", customTries=1)
                    self.clickPointInstantly(
                        lyriaDialogX + 180, lyriaDialogY - 51, delay=False)
                elif(self.findDialog("vyrnDialog", customTries=1) != None):
                    print("[DEBUG] Detected Vyrn dialog. Closing it now...")
                    vyrnDialogX, vyrnDialogY = self.findDialog(
                        "vyrnDialog", customTries=1)
                    self.clickPointInstantly(
                        vyrnDialogX + 180, vyrnDialogY - 51, delay=False)

                self.findButton("questResultsOK", customTries=3)
                self.accountForPing(1)

            print(
                f"\n[COMBAT] Combat is over.")

        except FileNotFoundError as e:
            print(
                f"[ERROR] Cannot find \"{scriptName}.txt\" inside the /scripts folder.")

    # Test the Combat Mode by starting the Normal difficulty Angel Halo special battle and completing it.
    # This assumes that Angel Halo is at the very bottom of the Special missions list.
    def testCombatMode(self):
        if(self.debugMode):
            print(
                "\n[DEBUG] Testing Combat Mode on Normal Difficulty Angel Halo mission now...")
        self.findButton("quest")
        self.findButton("special")

        # Attempt to fit all the "Select" buttons into the current view.
        self.scrollDown(-300)

        # Initialize a list of found "Select" button locations in the form of (x, y, width, height) tuples.
        if(self.debugMode):
            print("[DEBUG] Moving cursor to Angel Halo...")
        listOfLocations = list(pyautogui.locateAllOnScreen("images/buttons/select.png",
                                                           region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight)))
        angelHaloMissions = listOfLocations.pop()
        self.moveToAndClickPoint(
            angelHaloMissions[0] + 50, angelHaloMissions[1] + 10, mouseSpeed=self.mouseSpeed)

        # Click on Play and head to the Summon Selection Screen.
        if(self.debugMode):
            print("[DEBUG] Moving to Normal Difficulty Angel Halo...")
        listOfLocations = list(pyautogui.locateAllOnScreen("images/buttons/specialPlay.png",
                                                           region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight)))
        normalDifficulty = listOfLocations.pop(0)
        self.moveToAndClickPoint(
            normalDifficulty[0] + 25, normalDifficulty[1] + 10, mouseSpeed=self.mouseSpeed)
        self.confirmLocation("selectSummon")

        # Locate Dark summons and click on the first ULB Bahamut or random otherwise.
        self.findSummonElement("dark")
        self.findSummon("bahamutULB")

        # Select first Group, second Party.
        self.findPartyAndStartMission(1, 2)

        # Start the Combat Mode.
        self.startCombatMode("test")
