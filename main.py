from game import Game


def main():
    myGame = Game(custom_mouse_speed=0.3, debug_mode=True)
    myGame.test_combat_mode()


if __name__ == "__main__":
    main()
