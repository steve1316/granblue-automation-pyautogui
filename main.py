from game import Game
from debug import Debug


def main():
    my_game = Game(custom_mouse_speed=0.3, debug_mode=True)
    my_debug = Debug(my_game)
    my_debug.test_combat_mode()


if __name__ == "__main__":
    main()
