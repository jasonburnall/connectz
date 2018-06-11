#
# ConnectZ programming challenge
#
# Author Jason Burnall
#
# The idea is to hold the game in a matrix that can not exceed the board height/width restrictions defined in the
# game file.
# Game outcome is decided by tests against the `active` board area to save processing. For instance if game coins are
# only within columns 1 to 3, there is no need to test for a game win outside of a virtual board width of '3'.
# Similarly for coin stack height.
#
# No winner tests will be applied until the active board area equals or exceeds the required consecutive counter count.
#
# Tests will consist of horizontal, vertical and diagonal masks against the active board area.
#


import sys
import os
from pathlib import Path


class Error(Exception):
    """Base class"""
    pass


class GameException(Error):
    """Game exception

    codes:
        4 -- Illegal continue
        5 -- Illegal row
        6 -- Illegal column
        7 -- Illegal game
        8 -- Invalid file
        9 -- File error
    """

    def __init__(self, code):
        self.code = code


# Holds the
class Game(object):
    _board_width = 0  # Maximum board width
    _board_height = 0  # Maximum board height
    _counters = 0  # Connect `n`
    # Define active area
    _active_game_start_column = 0
    _active_game_end_column = 0
    # _active_game_start_row = 0
    _active_game_end_row = 0
    # Game matrix
    _the_game = []
    # Lets keep track of the number of moves made
    _move_count = 0
    # Game conditions
    _player_one_win = False
    _player_two_win = False
    _draw = False
    _incomplete = True

    def __init__(self, conf):
        """
        Game instantiation takes configuration settings.
        :param conf: Game configuration
        """
        # Split config line and attempt to cast them as ints
        try:
            lst_configs = [int(conf) for conf in conf.rstrip('\n').split()]
        except Exception:
            raise GameException(8)
        # Check config count
        if len(lst_configs) != 3:
            raise GameException(8)  # Code 8 -- Invalid file
        # And that the game conditions are valid
        if (lst_configs[0] < lst_configs[2]) and (lst_configs[1] < lst_configs[2]):
            raise GameException(7)  # Code 7 -- illegal game
        # Populate board dimensions
        self._board_width = lst_configs[0]
        self._board_height = lst_configs[1]
        self._counters = lst_configs[2]  # And consecutive counter count

    def get_outcome(self):
        """
        Return the outcome of the game.
        :return: int
        """
        if self._player_one_win:
            return 0
        if self._player_two_win:
            return 1
        if self._draw:
            return 2
        if self._incomplete:
            return 3

    def _check_horizontal_win(self):
        return False

    def _check_vertical_win(self):
        return False

    def _check_diagonal_incline_win(self):
        return False

    def _check_diagonal_decline_win(self):
        return False

    def _check_for_win(self):
        """
        This is the main game engine and determines if the game has a winner or it is a draw.
        Sets one of the game booleans on a completion state.
        """
        print(self._the_game)
        # No point running check unless minimum moves exceeded
        if self._move_count/2 > self._counters:
            return False
        # Only interested in active board space
        if ((self._active_game_end_column - self._active_game_start_column) + 1 < self._counters) and (self._active_game_end_row + 1 < self._counters):
            return False  # The active board area can't accommodate a win
        if self._active_game_end_row + 1 < self._counters:
            # Only horizontal wins will work
            return self._check_horizontal_win()
        if (self._active_game_end_column - self._active_game_start_column) + 1 < self._counters:
            # Only vertical wins can work due to horizontal distribution of counters
            return self._check_vertical_win
        # Check them in turn
        if self._check_horizontal_win():
            return True
        if self._check_vertical_win():
            return True
        if self._check_diagonal_incline_win():
            return True
        if self._check_diagonal_decline_win():
            return True
        return False


    def move(self, column, player):
        """
        What player and which row is used to update the the game board.
        When the board has been updated the `completion` function is run to determine if the game has finished.
        :param column: str
        :param player: int 1 or 2
        :return:
        """
        # First check column can cast to int
        try:
            column = int(column)
        except Exception:
            # Not what we expected
            raise GameException(8)
        # Check that player is either 1 or 2
        if player not in [1, 2]:
            raise Exception('Not a valid player')
        # Now check column number is within allowable board dimensions
        if column > self._board_width:
            raise GameException(6)
        # Now check to see if this is one too many moves.
        if self._player_one_win or self._player_two_win or self._draw:
            # We shouldn't have got to here, too many moves.
            raise GameException(4)  # Illegal continue
        # Move seems valid so make it
        if not self._the_game:
            # No moves made yet so create a row
            new_row = [0] * self._board_width
            new_row[column - 1] = 1  # And add counter for player 1
            self._the_game.append(new_row)  # Update the board
            self._active_game_start_column = self._active_game_end_column = column - 1  # And update active game space
            self._active_game_end_row = 0
        else:
            b_coin_placed = False
            row_idx = 0
            # Find a row where the counter will stop
            for row in self._the_game:
                if not row[column - 1]:
                    # No coin in the way
                    self._the_game[row_idx][column - 1] = player
                    b_coin_placed = True
                    break
                else:
                    row_idx += 1  # Move to next row
            if not b_coin_placed:
                # All active rows are taken, need a new one
                new_row = [0] * self._board_width
                new_row[column - 1] = player  # And add counter for player
                self._the_game.append(new_row)
                # Quickly check that row count hasn't been exceeded
                if len(self._the_game) > self._board_height:
                    raise GameException(5)  # code 5 -- Illegal row
            # Update active board space
            if column - 1 < self._active_game_start_column:
                self._active_game_start_column = column - 1
            if self._active_game_end_column < column - 1:
                self._active_game_end_column = column - 1
            if self._active_game_end_row < row_idx:
                self._active_game_end_row = row_idx
        self._move_count += 1  # Keep an eye in the number of moves
        # Now the board is updated, lets check for and end game event
        return self._check_for_win()


class ConnectZ(object):
    _outcome = None

    def __init__(self, file_input=None):
        # Test if file exists
        this_file = Path(file_input)
        if not this_file.is_file():
            # There is no file on disk therefore raise exception
            raise GameException(9)  # code 9 -- File error
        obj_game = None
        players_go = 1  # Player 1 goes first
        with open(file_input) as f:
            for line in f:
                if obj_game is None:
                    # First row contains game config
                    obj_game = Game(line)
                else:
                    # Now we're making moves!
                    obj_game.move(line, players_go)
                    # Change players turn to go
                    if players_go == 1:
                        players_go = 2
                    else:
                        players_go = 1

    def get_outcome(self):
        return self._outcome


# Command line execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # Incorrect command line argument count. Alert user
        sys.stdout.write(
            '\rconnectz.py: Provide one \033[92minput \033[0mfile')  # Assumes ANSI available (Linux default)
        print()  # Tidy command prompt
    else:
        try:
            # Run the game. Exceptions raised for game errors otherwise valid outcome found in get_outcome()
            sys.stdout.write(ConnectZ(sys.argv[1]).get_outcome())
            print()
        except GameException as e:
            # Game error codes reported to user.
            sys.stdout.write(e.code)
            print()
        except Exception as e:
            # Not good if got to here.
            raise e

dir_path = os.path.dirname(os.path.realpath(__file__))
# ConnectZ("{path}/tests/classic.txt".format(path=dir_path))
# ConnectZ("/Users/jason/Documents/My\ Development/connectz/code/tests/classic.txt")
# ConnectZ("/usr/src/app/tests/classic.txt")
# ConnectZ("/usr/src/app/tests/impossible.txt")
ConnectZ("/usr/src/app/tests/too_many_rows.txt")
