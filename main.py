from game import Game
from debug import Debug

DEBUG = False


def main():
    my_game = Game(custom_mouse_speed=0.3, debug_mode=DEBUG)
    my_debug = Debug(my_game)

    # Test finding all summon element tabs in Summon Selection Screen.
    # my_debug.test_find_summon_element_tabs()

    # Test Combat Mode.
    # my_debug.test_combat_mode()


if __name__ == "__main__":
    main()
