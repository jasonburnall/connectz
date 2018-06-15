#
# ConnectZ programming challenge
#
# Author Jason Burnall
#
# The idea is to hold the game in a matrix that can not exceed the board height/width restrictions defined in the
# game file.
# Game outcome is decided by tests against vertices running through the last coin dropped.
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


# Holds and handles anything to do with the ConnectZ game.
class Game(object):

    def __init__(self, conf):
        """
        Game instantiation takes configuration settings.
        :param conf: Game configuration
        """
        # Define instance variables.
        self._board_width = 0  # Maximum board width
        self._board_height = 0  # Maximum board height
        self._counters = 0  # Connect `n`
        # Game matrix
        self._the_game = []  # This is the active board area
        self._game_frequency = []  # Keep track of counter stack heights
        self._max_virtual_height = 0  # This keeps track of the maximum counter stack height
        # Lets keep track of the number of moves made
        self._move_count = 0
        # Game conditions
        self._player_one_win = False
        self._player_two_win = False
        self._draw = False
        self._incomplete = True

        # Split config line and attempt to cast them as ints
        try:
            lst_configs = [int(conf) for conf in conf.rstrip('\n').split()]
        except Exception:
            raise GameException(8)
        # Check config value count
        if len(lst_configs) != 3:
            raise GameException(8)  # Code 8 -- Invalid file
        # And that the game conditions are valid
        if (lst_configs[0] < lst_configs[2]) and (lst_configs[1] < lst_configs[2]):
            raise GameException(7)  # Code 7 -- illegal game
        # Populate board dimensions
        self._board_width = lst_configs[0]
        self._board_height = lst_configs[1]
        self._counters = lst_configs[2]  # And consecutive counter count
        self._game_frequency = [0] * self._board_width  # coin count per column
        self._the_game = [[0] * self._board_width]  # Define first row
        self._max_virtual_height = 1  # Set current height of row

    def get_outcome(self):
        """
        Return the outcome of the game.
        :return: int
        """
        if self._player_one_win:
            return 1
        if self._player_two_win:
            return 2
        if self._draw:
            return 0
        if self._incomplete:
            return 3

    def _process_board(self, coin_row_idx, coin_col_idx):
        """
        This is the main game engine and determines if the game has a winner or if the game is a draw.
        Sets one of the game outcome booleans on a completion state.
        :param coin_row_idx: int  Row index on game where coin landed
        :param coin_col_idx: int  Column index on game where coin landed
        """
        # Check to see if the game is already complete.
        if self._player_one_win or self._player_two_win or self._draw:
            # One too many moves, raise an exception
            raise GameException(4)  # code 4 -- Illegal continue
        # No point running check unless minimum moves reached
        if self._move_count - (self._counters - 1) < self._counters:
            return False
        # Only interested in game vectors through coin of a maximum magnitude of `z` from coin
        list_h = []
        list_v = []
        list_i = []
        list_d = []
        for x in range(-(self._counters - 1), self._counters):
            try:
                if coin_col_idx + x < 0:
                    raise IndexError  # catch[-n] which can be valid in list
                list_h.append(self._the_game[coin_row_idx][coin_col_idx + x])
            except IndexError:
                pass
            try:
                if coin_row_idx + x < 0:
                    raise IndexError
                list_v.append(self._the_game[coin_row_idx + x][coin_col_idx])
            except IndexError:
                pass
            try:
                if coin_row_idx + x < 0:
                    raise IndexError
                if coin_col_idx + x < 0:
                    raise IndexError
                list_i.append(self._the_game[coin_row_idx + x][coin_col_idx + x])
            except IndexError:
                pass
            try:
                if coin_row_idx - x < 0:
                    raise IndexError
                if coin_col_idx + x < 0:
                    raise IndexError
                list_d.append(self._the_game[coin_row_idx - x][coin_col_idx + x])
            except IndexError:
                pass
        # Build strings to use in comparison
        horizontal = ''.join(map(str, list_h))
        vertical = ''.join(map(str, list_v))
        incline = ''.join(map(str, list_i))
        decline = ''.join(map(str, list_d))
        list_p1_win = ['1'] * self._counters  # `z`
        p1_win = ''.join(list_p1_win)
        list_p2_win = ['2'] * self._counters  # `z`
        p2_win = ''.join(list_p2_win)
        # Check for win looking for win condition in vertices strings
        if p1_win in horizontal or p1_win in vertical or p1_win in incline or p1_win in decline:
            # Player 1 wins!
            self._draw = self._player_two_win = self._incomplete = False
            self._player_one_win = True
            return True
        if p2_win in horizontal or p2_win in vertical or p2_win in incline or p2_win in decline:
            # Player 2 wins!
            self._draw = self._player_one_win = self._incomplete = False
            self._player_two_win = True
            return True
        # Check for draw condition
        if self._move_count == (self._board_width * self._board_height):
            # All spaces populated with counters, therefore a draw
            self._player_one_win = self._player_two_win = self._incomplete = False
            self._draw = True
            return True
        return False

    def move(self, column, player):
        """
        What player and which row is used to update the the game board.
        When the board has been updated the `win checker` function is run to determine if the game has finished.
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
        if 0 > column or column > self._board_width:
            raise GameException(6)
        # Now check to see if this is one too many moves.
        if self._player_one_win or self._player_two_win or self._draw:
            # We shouldn't have got to here, too many moves.
            raise GameException(4)  # Illegal continue
        # Move seems valid so make it
        current_row_count = 1
        if max(self._game_frequency):
            current_row_count = max(self._game_frequency)
        self._game_frequency[column - 1] += 1  # Add a column coin count
        if current_row_count < max(self._game_frequency):
            # Need a new game row
            new_row = [0] * self._board_width
            self._the_game.append(new_row)
            self._max_virtual_height += 1  # Update maximum coin stack count
        # Check for too many rows
        if self._max_virtual_height > self._board_height:
            raise GameException(5)  # code 5 -- Illegal row
        # Place the coin
        coin_row_idx = self._game_frequency[column - 1] - 1
        coin_column_idx = column - 1
        self._the_game[coin_row_idx][coin_column_idx] = player
        # And remove bottom row if it is no longer in game play
        if min(self._game_frequency) - self._counters > 0:
            del self._the_game[0]  # Remove bottom row of board
            self._game_frequency[:] = [cell - 1 for cell in self._game_frequency]  # Reduce column count too
            coin_row_idx -= 1  # Update coin index
        self._move_count += 1  # Keep an eye in the number of moves
        # Now the board is updated, lets process the moves made
        return self._process_board(coin_row_idx, coin_column_idx)


class ConnectZ(object):

    def __init__(self, file_input=None):
        """
        Class instantiation requires file to be processed.
        :param file_input: ASCII file on disk
        """
        self._this_file = None  # Game file to be processed
        try:
            # Test if file exists
            self._this_file = Path(file_input)
        except Exception as e:
            raise GameException(9)
        if not self._this_file.is_file():
            # There is no file on disk therefore raise exception
            raise GameException(9)  # code 9 -- File error

    def run_game(self):
        """
        Run through the file provided at instantiation. The file should contain the game configuration on the the first
        row followed by player moves on separate lines.
        :return: int
        :exception: GameException
        """
        obj_game = None
        players_go = 1  # Player 1 goes first
        with open(self._this_file) as f:
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
        # All moves completed with no exceptions made. Return valid game state
        return obj_game.get_outcome()


# Command line execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # Incorrect command line argument count. Alert user
        print('\rconnectz.py: Provide one \033[92minput \033[0mfile')  # Assumes ANSI available (Linux default)
    else:
        try:
            # Run the game. Exceptions raised for game errors otherwise valid outcome found in get_outcome()
            print(ConnectZ(sys.argv[1]).run_game())
        except GameException as e:
            # Game error codes reported to user.
            print(e.code)
        except Exception as e:
            # Not good if got to here.
            raise e
