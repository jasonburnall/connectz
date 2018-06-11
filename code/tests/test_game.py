import os
import sys
import unittest

sys.path.append(os.path.dirname(__file__) + '..')
from connectz import Game
from connectz import ConnectZ


class TestGame(unittest.TestCase):

    def test_game_invalid_init(self):
        """
        Game accepts three string values, two given should raise exception
        """
        try:
            Game('7 6')
        except Exception as e:
            self.assertEqual(e.code, 8)

    def test_game_invalid_init_type(self):
        """
        Game accepts three string values that should cast to int.
        """
        try:
            Game('a 7 6')
        except Exception as e:
            self.assertEqual(e.code, 8)

    def test_incorrect_column_event(self):
        """
        Column outside of board dimensions
        """
        try:
            obj_game = Game('2 2 2')
            obj_game.move(3, 1)
        except Exception as e:
            self.assertEqual(e.code, 6)

    def test_for_missing_file(self):
        try:
            ConnectZ("/does/not/exist/file.txt")
        except Exception as e:
            self.assertEqual(e.code, 9)

    def test_classic_connect(self):
        """
        Run classic connect four game where players alternate columns
        """
        self.assertEqual(ConnectZ("/usr/src/app/tests/classic.txt").run_game(), 1)

    def test_draw(self):
        """
        Run draw game
        """
        self.assertEqual(ConnectZ("/usr/src/app/tests/draw.txt").run_game(), 0)

    def test_illegal_column(self):
        """
        Run illegal column game
        """
        try:
            ConnectZ("/usr/src/app/tests/illegal_column.txt").run_game()
        except Exception as e:
            self.assertEqual(e.code, 6)

    def test_illegal_continue(self):
        """
        Run illegal continue game
        """
        try:
            ConnectZ("/usr/src/app/tests/illegal_continue.txt").run_game()
        except Exception as e:
            self.assertEqual(e.code, 4)

    def test_illegal_game(self):
        """
        Run illegal game
        """
        try:
            ConnectZ("/usr/src/app/tests/illegal_game.txt").run_game()
        except Exception as e:
            self.assertEqual(e.code, 7)

    def test_illegal_row(self):
        """
        Run illegal row
        """
        try:
            ConnectZ("/usr/src/app/tests/illegal_row.txt").run_game()
        except Exception as e:
            self.assertEqual(e.code, 5)

    def test_incomplete(self):
        """
        Run incomplete game
        """
        self.assertEqual(ConnectZ("/usr/src/app/tests/incomplete.txt").run_game(), 3)

    def test_invalid_file(self):
        """
        Test an invalid file
        """
        try:
            ConnectZ("/usr/src/app/tests/invalid_file.txt").run_game()
        except Exception as e:
            self.assertEqual(e.code, 8)

    def test_player_one_win(self):
        """
        Run player 1 wins scenario
        """
        self.assertEqual(ConnectZ("/usr/src/app/tests/player_one_win.txt").run_game(), 1)

    def test_player_two_win(self):
        """
        Run player 2 wins scenario
        """
        self.assertEqual(ConnectZ("/usr/src/app/tests/player_two_win.txt").run_game(), 2)

    def test_player_one_win_diagonal_up(self):
        """
        Run player 1 wins with diagonal scenario
        """
        self.assertEqual(ConnectZ("/usr/src/app/tests/player_one_win_incline.txt").run_game(), 1)

    def test_player_one_win_diagonal_down(self):
        """
        Run player 1 wins with diagonal scenario
        """
        self.assertEqual(ConnectZ("/usr/src/app/tests/player_one_win_decline.txt").run_game(), 1)


if __name__ == '__main__':
    unittest.main()
