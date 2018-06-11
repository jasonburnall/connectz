import unittest
# from ../connectz import Game
# from ../.G import GameException
from connectz import GameException
from connectz import Game
from connectz import ConnectZ


class TestGame(unittest.TestCase):

    def test_game_valid_init(self):
        """
        Game accepts three values
        """
        self.assertTrue(Game(7, 6, 4))

    def test_game_invalid_init(self):
        """
        Game accepts tree int values, two given should raise exception
        """
        try:
            Game(7, 6)
        except Exception as e:
            self.assertEquals(e.code, 8)

    def test_game_invalid_init_type(self):
        """
        Game accepts tree int values, strings given
        """
        try:
            Game('a', 7, 6)
        except Exception as e:
            self.assertEquals(e.code, 8)

    def test_incorrect_column_event(self):
        """
        Column outside of board dimensions
        """
        try:
            obj_game = Game(2, 2, 2)
            obj_game.move(3, 1)
        except Exception as e:
            self.assertEquals(e.code, 6)

    def test_for_missing_file(self):
        try:
            ConnectZ("/does/not/exist/file.txt")
        except Exception as e:
            self.assertEquals(e.code, 9)

    def test_classic_connect(self):
        """
        Run classic connect four game where players alternate columns
        """
        self.assertEquals(ConnectZ("/usr/src/app/classic.txt"), 1)


if __name__ == '__main__':
    unittest.main()
