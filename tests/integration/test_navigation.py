import multiprocessing
import unittest

from bot import game, map_selection


class IntegrationTest2(unittest.TestCase):
    """
    This integration test must be started on the game's Home screen.
    """

    queue = multiprocessing.Queue()
    is_bot_running = multiprocessing.Value("i", 0)
    game = game.Game(queue, is_bot_running)
    map_select = map_selection.MapSelection(game, is_bot_running)

    def test_navigation1(self):
        self.assertTrue(IntegrationTest2.map_select.select_map("Quest", "Port Breeze Archipelago", "Scattered Cargo", ""))

    def test_navigation2(self):
        self.assertTrue(IntegrationTest2.map_select.select_map("Quest", "Amalthea Island", "The Dungeon Diet", ""))

    def test_navigation3(self):
        self.assertTrue(IntegrationTest2.map_select.select_map("Quest", "Albion Citadel", "I Challenge You!", ""))

    def test_navigation4(self):
        self.assertTrue(IntegrationTest2.map_select.select_map("Special", "Shiny Slime Search!", "VH Slimy Slime Search!", "Very Hard"))

    def test_navigation5(self):
        self.assertTrue(IntegrationTest2.map_select.select_map("Raid", "", "Lvl 120 Grimnir", ""))

    def test_navigation6(self):
        self.assertTrue(IntegrationTest2.map_select.select_map("Coop", "", "Time of Revelation", ""))


if __name__ == "__main__":

    unittest.main()
