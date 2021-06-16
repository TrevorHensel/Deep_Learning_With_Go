import copy
from dlgo.gotypes import Player


class Move:
    """
    # Defines a move
    """

    def __init__(self, point=None, is_pass=False, is_resign=False):
        """
        :param point: Point
        :param is_pass: Boolean
        :param is_resign: Boolean
        :exception AssertionError: If Point isn't a valid move
        """
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        """
        # Returns the current move with an updated Point
        :param point: Point
        :return: Move
        """
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        """
        # Returns the current move as a pass
        :return: Move
        """
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        """
        # Returns the current move as a resign
        :return: Move
        """
        return Move(is_resign=True)


class GoString:
    """
    # A string of connected go pieces
    # it's much easier to keep track of
    # a set of pieces than individual
    # pieces.
    # This keeps track of the string color,
    # all the stones in the string,
    # and all their liberties.
    """

    def __init__(self, color, stones, liberties):
        """
        :param color: Player
        :param stones: List of Points
        :param liberties: List of Points
        """
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        """
        # Removes a liberty from the string
        :param point: Point
        """
        self.liberties.remove(point)

    def add_liberty(self, point):
        """
        # Adds a liberty to the string
        :param point: Point
        """
        self.liberties.add(point)

    def merged_with(self, go_string):
        """
        # Merges two strings together into one
        :param go_string: GoString
        :return: GoString
        :exception AssertionError: If Point isn't a valid move
        """
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(self.color, combined_stones, (self.liberties | go_string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        """
        # Returns amount of liberties a string has
        :return: Integer
        """
        return len(self.liberties)

    def __eq__(self, other):
        """
        # Overrides equal operator
        :param other: GoString
        :return: Boolean
        """
        return isinstance(other, GoString) and \
               self.color == other.color and \
               self.stones == other.stones and \
               self.liberties == other.liberties


class Board:
    """
    # The Go board
    # Keeps track of all stones on the board
    # as well as their associated strings.
    # Will also place new stones on the board
    # and assign them to new strings.
    """

    def __init__(self, num_rows, num_cols):
        """
        :param num_rows: Integer
        :param num_cols: Integer
        """
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    def place_stone(self, player, point):
        """
        # Places a stone on the board.
        :param player: Player
        :param point: Point
        :exception AssertionError: If Point isn't a valid move
        """

        # Checks if Point is a valid and empty point on the board
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []

        # Loop through all neighbors
        for neighbor in point.neighbors():
            # If neighbor is off the grid continue
            if not self.is_on_grid(neighbor):
                continue

            # Gets the string, if any of current neighbor
            neighbor_string = self._grid.get(neighbor)

            # Add liberty to list if no string
            # Else add string to list
            # of same or opposite colored
            # neighbor strings list
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_opposite_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)

        # Create a new string
        new_string = GoString(player, [point], liberties)

        # Adds strings together to make one string of same color
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)

        # Updates strings on the grid
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string

        # Removes liberties from opposite color strings
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)

        # If captured removes string from board
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def is_on_grid(self, point):
        """
        # Checks if a point is on the board
        :param point: Point
        :return: Boolean
        """
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get(self, point):
        """
        # Returns the stone on a given Point
        :param point: Point
        :return: Player
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point):
        """
        # Returns a string of stones at a given Point
        :param point: Point
        :return: GoString
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    def _remove_string(self, string):
        """
        # Removes a string from the Board
        :param string: GoString
        """
        # Loops through all Points in a string
        # Adds liberties to its' neighbors
        # sets all Points in the string to None
        for point in string.stones:

            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)

                if neighbor_string is None:
                    continue

                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)

            self._grid[point] = None


class GameState:
    """
    # Saves previous GameStates
    # This is important for checking some
    # rules of Go
    """

    def __init__(self, board, next_player, previous, move):
        """
        :param board: Board
        :param next_player: Player
        :param previous: Board
        :param move: Move
        """
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):
        """
        # Copies the current Board to a new Board
        # then sets the previous Board to the current
        :param move: Move
        :return: GameState
        """
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board

        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        """
        # Creates a new game of size 'board_size'
        :param board_size: Integer
        :return: GameState
        """
        if isinstance(board_size, int):
            board_size = (board_size, board_size)

        board = Board(*board_size)

        return GameState(board, Player.black, None, None)

    def is_over(self):
        """
        # Determines if a game is over
        :return: Boolean
        """
        if self.last_move is None:
            return False

        if self.last_move.is_resign:
            return True

        second_last_move = self.previous_state.last_move

        if second_last_move is None:
            return False

        return self.last_move.is_pass and second_last_move.is_pass

    def is_move_self_capture(self, player, move):
        """
        # Determines if a move is a self capture
        :param player: Player
        :param move: Move
        :return: Boolean
        """
        if not move.is_play:
            return False

        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)

        return new_string.num_liberties == 0

    @property
    def situation(self):
        """
        # Used for previous board state
        :return: Player, Board
        """
        return self.next_player, self.board

    def does_move_violate_ko(self, player, move):
        """
        # Determines if a move violates the rule of ko
        # "Roughly speaking, the ko rule applies
        # if a move would return the board to the
        # exact previous position" - Deep Learning and the
        # Game of Go
        :param player: Player
        :param move: Move
        :return: Boolean
        """
        if not move.is_play:
            return False

        # Creates a copy of the board and makes the move
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        past_state = self.previous_state

        # Determines if the new move is from a previous
        # GameState
        while past_state is not None:
            if past_state.situation == next_situation:
                return True

            past_state = past_state.previous_state

        return False

    def is_valid_move(self, move):
        """
        # Determines if a given Move is a valid
        # Move on the board
        :param move: Move
        :return: Boolean
        """
        if self.is_over():
            return False

        if move.is_pass or move.is_resign:
            return True

        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move)
        )
