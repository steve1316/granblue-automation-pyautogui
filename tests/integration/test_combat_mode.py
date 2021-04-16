import multiprocessing
import os
import unittest

from bot import game, combat_mode


class IntegrationTest1(unittest.TestCase):
    """
    This integration test must be started on the game's Home screen.
    """

    queue = multiprocessing.Queue()
    is_bot_running = multiprocessing.Value("i", 0)
    game = game.Game(queue, is_bot_running)
    combat_mode = combat_mode.CombatMode(game, is_bot_running)

    def test_combat_mode1(self):
        # Make sure the bot is at the Home screen and go to the Trial Battles screen.
        IntegrationTest1.game.go_back_home(confirm_location_check = True)
        IntegrationTest1.game.mouse_tools.scroll_screen_from_home_button(-600)
        IntegrationTest1.game.find_and_click_button("gameplay_extras")

        while IntegrationTest1.game.find_and_click_button("trial_battles") is False:
            IntegrationTest1.game.mouse_tools.scroll_screen_from_home_button(-300)

        self.assertTrue(IntegrationTest1.game.image_tools.confirm_location("trial_battles"))
        # Click on the "Old Lignoid" button.
        IntegrationTest1.game.find_and_click_button("trial_battles_old_lignoid")

        # Select any detected "Play" button.
        IntegrationTest1.game.find_and_click_button("play_round_button")

        # Now select the first Summon.
        choose_a_summon_location = IntegrationTest1.game.image_tools.find_button("choose_a_summon")
        IntegrationTest1.game.mouse_tools.move_and_click_point(choose_a_summon_location[0], choose_a_summon_location[1] + 187, "choose_a_summon")

        # Now start the Old Lignoid Trial Battle right away and then wait a few seconds.
        IntegrationTest1.game.find_and_click_button("party_selection_ok")
        IntegrationTest1.game.wait(3)

        if IntegrationTest1.game.image_tools.confirm_location("trial_battles_description"):
            IntegrationTest1.game.find_and_click_button("close")

        os.chdir("tests/integration/")

        self.assertFalse(IntegrationTest1.combat_mode.start_combat_mode(os.path.abspath("test_combat_mode.txt")))

        self.assertTrue(IntegrationTest1.game.image_tools.confirm_location("home"))


if __name__ == "__main__":

    unittest.main()
