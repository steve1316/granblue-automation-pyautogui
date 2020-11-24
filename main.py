from game import Game
from debug import Debug


def main():
    myGame = Game(custom_mouse_speed=0.3, debug_mode=True)
    myDebug = Debug(myGame)
    myDebug.test_combat_mode()


if __name__ == "__main__":
    main()
