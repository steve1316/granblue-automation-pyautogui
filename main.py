from game import Game


def main():
    myGame = Game(custom_mouse_speed=0.3, debug_mode=True)
    # myGame.test_combat_mode()
    locations = myGame.image_tools.find_all("select")
    if (locations != None):
        if (len(locations) == 0):
            print("No matches found. Empty list: ", locations)
        else:
            for location in locations:
                print("Match Found: ", location)


if __name__ == "__main__":
    main()
