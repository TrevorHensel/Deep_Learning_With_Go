from dlgo.gotypes import Point


def is_point_an_eye(board, point, color):
    """
    # Very simplistic way of determine if
    # a given Point on a Board is an eye.
    # Should be noted this will miss cases
    # of eyes, but is simplistic implementation
    :param board: Board
    :param point: Point
    :param color: Player
    :return: Boolean
    """
    if board.get(point) is not None:
        return False

    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)

            if neighbor_color != color:
                return False

    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1)
    ]

    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)

            if corner_color == color:
                friendly_corners += 1

        else:
            off_board_corners += 1

    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4

    return friendly_corners >= 3
