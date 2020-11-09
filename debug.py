import pyautogui
import time
import sys

# This Debug class deals in helping test the pyautogui's capability to find elements on the user's screen.
class Debug:
    def __init__(self, userDefinedMouseSpeed, userDefinedConfidence):
        super().__init__()
        self.mouseSpeed = userDefinedMouseSpeed # The mouse speed that pyautogui will use.
        self.confidence = userDefinedConfidence # The confidence that pyautogui will use to match images on the screen.

    # Test finding the Quest Button on the user's screen.
    def testFindQuestButton(self):
        self.goBackToHome()
        print("\n[DEBUG] Testing finding the Quest Button from Home Screen...")
        x, y = self.locate("quest")
        print("[DEBUG] Found the Quest Button! Now attempting to click on it.")

        pyautogui.moveTo(x, y, self.mouseSpeed, pyautogui.easeInQuad)
        pyautogui.click()
        self.confirmLocation("quest")

        print("[DEBUG] Testing the Quest Button detection completed successfully.")

    # Test finding the Raid Button on the user's screen.
    def testFindRaidButton(self):
        self.testFindQuestButton()
        print("\n[DEBUG] Testing finding the Raid Button from Quest Screen...")
        x, y = self.locate("raid")
        print("[DEBUG] Found the Raid Button! Now attempting to click on it.")

        pyautogui.moveTo(x, y, self.mouseSpeed, pyautogui.easeInQuad)
        pyautogui.click()
        self.confirmLocation("raid")

        print("[DEBUG] Testing the Raid Button detection completed successfully.")

    # Attempt to locate the UI image across the entire screen.
    def locate(self, imageName):
        location = None
        tries = 3

        while (location == None):
            location = pyautogui.locateOnScreen(f"images/buttons/{imageName.lower()}.png", self.confidence)
            if (location == None):
                print(f"[DEBUG] Locating {imageName.upper()} Button failed. Trying again in 5 seconds...")
                tries -= 1
                if (tries == 0):
                    sys.exit(f"[ERROR] Could not find {imageName.upper()} Button after several tries. Exiting Program...")
                time.sleep(5)

        point = pyautogui.center(location)
        return point.x, point.y

    # Wait a few seconds to account for bad ping.
    def accountForPing(self):
        time.sleep(3)

    # Confirm the bot's position.
    def confirmLocation(self, locationName):
        self.accountForPing()
        location = None
        tries = 3

        while (location == None):
                location = pyautogui.locateOnScreen(f"images/headers/{locationName.lower()}Header.png", self.confidence)
                if(location == None):
                    print(f"[DEBUG] Bot's current location is not at {locationName.upper()}. Trying again in 5 seconds...")
                    tries -= 1
                    if (tries == 0):
                        sys.exit(f"[ERROR] Could not find {locationName.upper()} location after 3 tries. Exiting Program...")
                    time.sleep(5)

        print(f"[DEBUG] Bot's current location is at {locationName.upper()}.")

    # Go back to the Home Screen to reset the bot's position.
    def goBackToHome(self):
        print("\n[DEBUG] Now attempting to move back to the Home Screen...")
        x, y = self.locate("home")
        
        pyautogui.moveTo(x, y, self.mouseSpeed, pyautogui.easeInQuad)
        pyautogui.click()

        self.confirmLocation("home")


