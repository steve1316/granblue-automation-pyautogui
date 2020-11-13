import pyautogui
import time
import sys
import cv2  # opencv-python package is necessary for the confidence (accuracy) argument for pyautogui's locating functions.

# This Debug class deals in helping test the pyautogui's capability to find elements on the user's screen.
class Debug:
    def __init__(self, userDefinedMouseSpeed, userDefinedConfidence, debugMode = False):
        super().__init__()
        self.mouseSpeed = userDefinedMouseSpeed  # The mouse speed that pyautogui will use.
        self.confidence = userDefinedConfidence  # The accuracy that pyautogui will use to match images on the screen.
        self.debugMode = debugMode # Controls whether or not the [DEBUG] messages should be displayed.
        
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
    def findButton(self, buttonName, checkLocation=False):
        # If the bot needs to go to the Quest Screen, head back to the Home Screen.
        if (buttonName.lower() == "quest"):
            self.goBackToHome()

        if(self.debugMode): print(f"\n[DEBUG] Now attempting to find the {buttonName.upper()} Button from current position...")
        
        x, y = self.locate(buttonName)
        
        if(self.debugMode): print(f"[DEBUG] Found the {buttonName.upper()} Button at ({x}, {y})!")
        
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
                location = pyautogui.locateOnScreen(f"images/buttons/{imageName.lower()}.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            else:
                location = pyautogui.locateOnScreen(f"images/buttons/{imageName.lower()}.png", confidence=self.confidence)
            
            if (location == None):
                tries -= 1
                
                # If the number of tries has been exhausted, the bot will return None.
                if (tries == 0):
                    print(f"[ERROR] Could not find {imageName.upper()} Button after several tries. Returning None...")
                    return None
                
                if(self.debugMode): print(f"[DEBUG] Locating {imageName.upper()} Button failed. Trying again in 5 seconds...")
                
                # Sleep for 5 seconds and try again.
                self.accountForPing(5)
        
        # Center the location and returns a tuple.
        centerLocation = pyautogui.center(location)
        
        return centerLocation

    # Wait the specified seconds to account for bad ping or loading.
    def accountForPing(self, seconds=3):
        time.sleep(seconds)

    # Confirm the bot's position.
    def confirmLocation(self, locationName):
        self.accountForPing(1)
        location = None
        tries = 3

        while (location == None):
            location = pyautogui.locateOnScreen(f"images/headers/{locationName.lower()}Header.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            if (location == None):
                tries -= 1
                
                # Break out of the while loop with an error message.
                if (tries == 0):
                    print(f"[ERROR] Could not confirm location for {locationName.upper()}.")
                    break
                
                if(self.debugMode): print(f"[DEBUG] Bot's current location is not at {locationName.upper()}. Trying again in 5 seconds...")
                
                # Sleep for 5 seconds and try again.
                self.accountForPing(5)

        if(self.debugMode and location != None): print(f"[DEBUG] Bot's current location is at {locationName.upper()} Screen.")

    # Go back to the Home Screen to reset the bot's position. Also recalibrates the region size of the game window if necessary.
    def goBackToHome(self, confirmLocationCheck = False):
        if(self.debugMode): print("\n[DEBUG] Now attempting to move back to the Home Screen...")
        
        # Avoid expensive CPU operations on finding the "Home" Button if you already found it before. Update the dimensions of the game window as well.
        if(self.homeButtonX == None or self.homeButtonY == None):
            self.homeButtonX, self.homeButtonY = self.locate("home")
            print(f"[DEBUG] Found Home Button at ({self.homeButtonX}, {self.homeButtonY})!")
            
            # Recalibrate the region size of the game window for pyautogui.
            # TODO: Recalibrate based on "News" Button together with "Home" Button potentially for smaller sized screens. Need to get to Home Screen first.
            self.windowLeft = self.homeButtonX - 439
            self.windowTop = self.homeButtonY - 890
            self.windowWidth = self.windowLeft + 480
            self.windowHeight = self.windowTop + 917
        
        self.moveToAndClickPoint(self.homeButtonX, self.homeButtonY, mouseSpeed=self.mouseSpeed)
        
        if(confirmLocationCheck):
            self.confirmLocation("home")

    # Attempt to drag the screen down to reveal more UI elements by locating the Home button at the bottom.
    def scrollDown(self, scrollClicks):
        # Find the Home button on the bottom right of the bar at the base of the window.
        #self.findButton("home")

        # Now move the cursor slightly up and then scroll down based on the number of scrollClicks.
        if(self.debugMode): print("\n[DEBUG] Now scrolling the screen down...")
        pyautogui.moveTo(self.homeButtonX, self.homeButtonY - 100, self.mouseSpeed)
        pyautogui.scroll(scrollClicks)
        
        self.accountForPing(1)

    # Move the cursor to the specified point on the screen, click it, and then account for ping.
    def moveToAndClickPoint(self, x, y, mouseSpeed=1):
        pyautogui.moveTo(x, y, mouseSpeed)
        pyautogui.click()
        self.accountForPing(2)

    # Click the specified point on the screen instantly and then account for ping.
    def clickPointInstantly(self, x, y):
        pyautogui.click(x, y)
        self.accountForPing(2)

    # Select the specified element tab for summons. Search selected tabs first, then unselected tabs.
    # TODO: ALL images need to be segmented into Lite, Regular, and High to account for different Graphics Settings.
    def findSummonElement(self, summonElementName):
        summonElementLocation = None
        tries = 3
        if(self.debugMode): print(f"\n[DEBUG] Now attempting to find selected {summonElementName.upper()} Summon Element tab...")

        while (summonElementLocation == None):
            # Search for selected Fire Element Summon tab.
            if (summonElementName.lower() == "fire"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonFireSelected.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Water Element Summon tab.
            elif (summonElementName.lower() == "water"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonWaterSelected.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Earth Element Summon tab.
            elif (summonElementName.lower() == "earth"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonEarthSelected.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Wind Element Summon tab.
            elif (summonElementName.lower() == "wind"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonWindSelected.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Light Element Summon tab.
            elif (summonElementName.lower() == "light"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonLightSelected.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Dark Element Summon tab.
            elif (summonElementName.lower() == "dark"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonDarkSelected.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            # Search for selected Misc Element Summon tab.
            elif (summonElementName.lower() == "misc"):
                summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonMiscSelected.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))

            # If searching for selected tabs did not work, search for unselected tabs.
            if (summonElementLocation == None):
                if(self.debugMode): print(f"[DEBUG] Locating selected {summonElementName.upper()} Summon Element tab failed. Trying again for unselected tab...")

                # Search for unselected Fire Element Summon tab.
                if (summonElementName.lower() == "fire"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonFire.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Water Element Summon tab.
                elif (summonElementName.lower() == "water"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonWater.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Earth Element Summon tab.
                elif (summonElementName.lower() == "earth"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonEarth.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Wind Element Summon tab.
                elif (summonElementName.lower() == "wind"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonWind.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Light Element Summon tab.
                elif (summonElementName.lower() == "light"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonLight.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Dark Element Summon tab.
                elif (summonElementName.lower() == "dark"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonDark.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                # Search for unselected Misc Element Summon tab.
                elif (summonElementName.lower() == "misc"):
                    summonElementLocation = pyautogui.locateOnScreen("images/buttons/summonMisc.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))

                # If searching both selected and unselected Summon Element tabs failed, try again until tries are depleted.
                if (summonElementLocation == None):
                    tries -= 1
                    if (tries == 0):
                        sys.exit(
                            f"[ERROR] Could not find {summonElementName.upper()} Summon Element tab after several tries. Exiting Program...")

        if(self.debugMode): print(f"[DEBUG] Locating {summonElementName.upper()} Summon Element tab was successful. Clicking it now...")
        
        # After locating the Summon Element Tab, click it.
        summonElementCenterLocation = pyautogui.center(summonElementLocation)
        x, y = summonElementCenterLocation
        self.moveToAndClickPoint(x, y, mouseSpeed=self.mouseSpeed)

    # Find the specified Summon on the Summon Selection Screen. This is called after the findSummonElement() method in order to select the correct Summon Element tab.
    def findSummon(self, summonName):
        summonLocation = None
        tries = 3
        if(self.debugMode): print(f"\n[DEBUG] Now attempting to find {summonName.upper()} Summon...")

        while (summonLocation == None):
            summonLocation = pyautogui.locateOnScreen(f"images/summons/{summonName.lower()}.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
            if (summonLocation == None):
                if(self.debugMode): print(f"[DEBUG] Locating {summonName.upper()} Summon failed. Trying again in 2 seconds...")
                tries -= 1
                
                # If matching failed, scroll the screen down to see more Summons.
                self.scrollDown(-400)
                
                if (tries == 0):
                    sys.exit(
                        f"[ERROR] Could not find {summonName.upper()} Summon after several tries. Exiting Program...")

        if(self.debugMode): print(f"[DEBUG] Located {summonName.upper()} Summon successfully. Clicking it now...")
        
        # If the Summon was located, click it.
        x, y = pyautogui.center(summonLocation)
        self.moveToAndClickPoint(x, y, mouseSpeed=self.mouseSpeed)

    # Select the specified group and party. It will then start the mission.
    def findPartyAndStartMission(self, groupNumber, partyNumber):
        groupLocation = None
        tries = 3

        # Find the Group first. If the selected group number is less than 8, it is in Set A. Otherwise, it is in Set B.
        if(groupNumber < 8):
            if(self.debugMode): print(f"\n[DEBUG] Now attempting to find Set A, Group {groupNumber}...")

            while (groupLocation == None):
                groupLocation = pyautogui.locateOnScreen(f"images/buttons/partySetA.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                if (groupLocation == None):
                    if(self.debugMode): print(f"[DEBUG] Locating Group {groupNumber} failed. Trying again in 5 seconds...")
                    
                    # See if the user had Set B active instead of Set A if matching failed.
                    groupLocation = pyautogui.locateOnScreen(f"images/buttons/partySetB.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                    tries -= 1
                    
                    if (tries == 0):
                        sys.exit(
                        f"[ERROR] Could not find Group {groupNumber} after several tries. Exiting Program...")
                        
                    self.accountForPing(5)
        else:
            if(self.debugMode): print(f"\n[DEBUG] Now attempting to find Set B, Group {groupNumber}...")

            while (groupLocation == None):
                groupLocation = pyautogui.locateOnScreen(f"images/buttons/partySetB.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                if (groupLocation == None):
                    if(self.debugMode): print(f"[DEBUG] Locating Group {groupNumber} failed. Trying again in 5 seconds...")
                    
                    # See if the user had Set A active instead of Set B if matching failed.
                    groupLocation = pyautogui.locateOnScreen(f"images/buttons/partySetA.png", confidence=self.confidence, region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight))
                    tries -= 1
                    
                    if (tries == 0):
                        sys.exit(
                        f"[ERROR] Could not find Group {groupNumber} after several tries. Exiting Program...")
                    
                    self.accountForPing(5)

        # Center on the Set button and click the correct Group Number Tab.
        if(self.debugMode): print(f"[DEBUG] Successfully found the correct Set. Now selecting Group {groupNumber}...")
        if(groupNumber == 1):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(x - 350, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 2):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(x - 290, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 3):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(x - 230, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 4):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(x - 170, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 5):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(x - 110, y + 50, mouseSpeed=self.mouseSpeed)
        elif(groupNumber == 6):
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(x - 50, y + 50, mouseSpeed=self.mouseSpeed)
        else:
            x, y = pyautogui.center(groupLocation)
            self.moveToAndClickPoint(x + 10, y + 50, mouseSpeed=self.mouseSpeed)

        # Now select the correct Party.
        if(self.debugMode): print(f"[DEBUG] Successfully found Group {groupNumber}. Now selecting Party {partyNumber}...")
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

        #self.accountForPing(2)
        
        if(self.debugMode): print(f"[DEBUG] Successfully selected Party {partyNumber}. Now starting the mission.")
        
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
            
        if(self.debugMode): print(f"[DEBUG] Attack Button location: ({self.attackButtonX}, {self.attackButtonY})")
        
        if(characterNumber == 1):
            # Click the portrait of Character 1.
            self.moveToAndClickPoint(self.attackButtonX - 317, self.attackButtonY + 123, mouseSpeed=self.mouseSpeed)
        elif(characterNumber == 2):
            # Click the portrait of Character 2.
            self.moveToAndClickPoint(self.attackButtonX - 240, self.attackButtonY + 123, mouseSpeed=self.mouseSpeed)
        elif(characterNumber == 3):
            # Click the portrait of Character 3.
            self.moveToAndClickPoint(self.attackButtonX - 158, self.attackButtonY + 123, mouseSpeed=self.mouseSpeed)
        elif(characterNumber == 4):
            # Click the portrait of Character 4.
            self.moveToAndClickPoint(self.attackButtonX - 76, self.attackButtonY + 123, mouseSpeed=self.mouseSpeed)
    
    # Activate the skill specified for the already selected character.
    def useCharacterSkills(self, x, y, skill):
        if("useSkill(1)" in skill):
            print("[COMBAT] Character 1 uses Skill 1")
            self.moveToAndClickPoint(x - 213, y + 171, mouseSpeed=self.mouseSpeed)
        elif("useSkill(2)" in skill):
            print("[COMBAT] Character 1 uses Skill 2")
            self.moveToAndClickPoint(x - 132, y + 171, mouseSpeed=self.mouseSpeed)
        elif("useSkill(3)" in skill):
            print("[COMBAT] Character 1 uses Skill 3")
            self.moveToAndClickPoint(x - 51, y + 171, mouseSpeed=self.mouseSpeed)
        elif("useSkill(4)" in skill):
            print("[COMBAT] Character 1 uses Skill 4")
            self.moveToAndClickPoint(x + 39, y + 171, mouseSpeed=self.mouseSpeed)
    
    # Start the Combat Mode with the given script name. Start reading through the text file line by line and have the bot proceed accordingly.
    # TODO: Readjust x and y window for locate() for faster processing for first time and every error mismatch (maybe).
    def startCombatMode(self, scriptName):
        if(self.debugMode): print(f"\n[DEBUG] Now loading up {scriptName} Combat Plan.")

        # Open the text file and read all of the lines.
        try:
            script = open(f"scripts/{scriptName}.txt", "r")
            lines = script.readlines()
            
            i = 0
            lineNumber = 1
            turnNumber = 1
            #conditionalCheck = False
            
            print("\n[COMBAT] Starting script.")
            
            # Loop through and execute each line in the combat script.
            while(True):
                # Check for the "Next" Button.
                if(self.locate("next", customTries=1) != None):
                    break
                
                line = lines[i]
                
                # Print each line read if debug mode is active.
                if(line[0] != "#" and line[0] != "/" and line.strip() != ""):
                    if(self.debugMode):
                        print(f"[DEBUG] Line {lineNumber}: {line.strip()}")
                        lineNumber += 1
                
                # If it is the start of the Turn, grab the next line for execution.
                if("turn" in line.lower()):
                    print(f"\n[COMBAT] Beginning Turn {line[5]}.\n")
                    i += 1
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
                    print(f"\nCharacter {characterSelected} acts.")
                    # Select the character specified and return the tuple of the (x,y) coordinates of the "Attack" Button.
                    self.selectCharacter(characterSelected)
                    
                    # Get all occurrences of "useSkill" and then click the skills specified in order from left to right.
                    skills = line.split(".")
                    skills.pop(0) # Remove the first element as that is usually the character substring.
                    
                    # Loop through all occurrences and use the specified skills.
                    for skill in skills:
                        self.useCharacterSkills(self.attackButtonX, self.attackButtonY, skill)
                    
                    # Now click the Back button 
                    self.clickPointInstantly(self.attackButtonX - 322, self.attackButtonY)
                    self.accountForPing()
                
                # If the bot reaches the end of the turn in the script, click the "Attack" button and scan for the "Next" button indicating that the enemies are dead.
                if("end" in line):
                    turnNumber += 1
                    self.moveToAndClickPoint(self.attackButtonX, self.attackButtonY, mouseSpeed=self.mouseSpeed)
                    self.accountForPing(7) # 7 seconds seems to be the average for the time the party's attack ends and the "Attack" or "Next" Buttons show up.
                    
                    # Try to find the "Next" Button only once per turn.
                    nextLocation = self.locate("next", customTries=1)
                    if(nextLocation != None):
                        nextX, nextY = nextLocation
                        self.moveToAndClickPoint(nextX, nextY, mouseSpeed=self.mouseSpeed)
                
                # Increment by 1 to move to the next line for execution.
                i += 1
                
                # Break out of the while loop when EOF is reached.
                if(i >= len(lines)):
                    break
                
            # Once the bot reaches EOF, continue clicking the "Attack" Button until it is over.
        except FileNotFoundError as e:
            print(f"[ERROR] Cannot find \"{scriptName}.txt\" inside the /scripts folder.")
        
        # Close out the battle.
        x, y = self.locate("next")
        self.moveToAndClickPoint(x, y, mouseSpeed=self.mouseSpeed)


    # Test the Combat Mode by starting the Normal difficulty Angel Halo special battle and completing it.
    # This assumes that Angel Halo is at the very bottom of the Special missions list.
    def testCombatMode(self):
        if(self.debugMode): print("\n[DEBUG] Testing Combat Mode on Normal Difficulty Angel Halo mission now...")
        self.findButton("quest")
        self.findButton("special")

        # Attempt to fit all the "Select" buttons into the current view.
        self.scrollDown(-300)

        # Initialize a list of found "Select" button locations in the form of (x, y, width, height) tuples.
        if(self.debugMode): print("[DEBUG] Moving cursor to Angel Halo...")
        listOfLocations = list(pyautogui.locateAllOnScreen("images/buttons/select.png", region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight)))
        angelHaloMissions = listOfLocations.pop()
        self.moveToAndClickPoint(angelHaloMissions[0] + 50, angelHaloMissions[1] + 10, mouseSpeed=self.mouseSpeed)

        # Click on Play and head to the Summon Selection Screen.
        if(self.debugMode): print("[DEBUG] Moving to Normal Difficulty Angel Halo...")
        listOfLocations = list(pyautogui.locateAllOnScreen("images/buttons/specialPlay.png", region=(self.windowLeft, self.windowTop, self.windowWidth, self.windowHeight)))
        normalDifficulty = listOfLocations.pop(0)
        self.moveToAndClickPoint(normalDifficulty[0] + 25, normalDifficulty[1] + 10, mouseSpeed=self.mouseSpeed)
        self.confirmLocation("selectSummon")

        # Locate Dark summons and click on the first ULB Bahamut or random otherwise.
        self.findSummonElement("dark")
        self.findSummon("bahamutULB")

        # Select first Group, second Party.
        self.findPartyAndStartMission(1, 2)
        
        # Start the Combat Mode.
        self.startCombatMode("test")
