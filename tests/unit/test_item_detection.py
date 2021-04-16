import multiprocessing
import unittest

from bot import game


class UnitTest1(unittest.TestCase):
    """
    These unit tests are conducted on the test_item_detection.png image file.
    """

    queue = multiprocessing.Queue()
    is_bot_running = multiprocessing.Value("i", 0)
    game = game.Game(queue, is_bot_running, test_mode = True)

    def test_item_detection1(self):
        self.assertTrue(UnitTest1.game.image_tools.confirm_location("loot_collected"))

        amount = UnitTest1.game.image_tools.find_farmed_items("Horseman's Plate", take_screenshot = False)

        self.assertEqual(amount, 3)

    def test_item_detection2(self):
        self.assertTrue(UnitTest1.game.image_tools.confirm_location("loot_collected"))

        amount = UnitTest1.game.image_tools.find_farmed_items("Wind Orb", take_screenshot = False)

        self.assertEqual(amount, 1)

    def test_item_detection3(self):
        self.assertTrue(UnitTest1.game.image_tools.confirm_location("loot_collected"))

        amount = UnitTest1.game.image_tools.find_farmed_items("Sagittarius Omega Anima", take_screenshot = False)

        self.assertEqual(amount, 4)

    def test_item_detection4(self):
        self.assertTrue(UnitTest1.game.image_tools.confirm_location("loot_collected"))

        amount = UnitTest1.game.image_tools.find_farmed_items("Tiamat Malice Anima", take_screenshot = False)

        self.assertEqual(amount, 0)


if __name__ == "__main__":

    unittest.main()
