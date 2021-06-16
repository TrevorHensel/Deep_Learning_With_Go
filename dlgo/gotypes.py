import enum
from collections import namedtuple


class Player(enum.Enum):
    """
    # Player (color) Enum
    """

    black = 1
    white = 2
    
    @property
    def other(self):
        """
        # Returns opposite of given player
        :return: Player
        """
        return Player.black if self == Player.white else  Player.white


class Point(namedtuple('Point', 'row col')):
    """
    # A single point (namedtuple) on the Go board
    """

    def neighbors(self):
        """
        # Returns the 4 adjacent points from a given point
        :return: List of Points
        """

        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1)
        ]
