from dlgo import gotypes

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' . ',
    gotypes.Player.black: ' x ',
    gotypes.Player.white: ' o '
}


def print_move(player, move):
    """
    # Prints the move that is being made on the Board
    :param player: Player
    :param move: Move
    """
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)

    print('%s %s' % (player, move_str))

def print_board(board):
    """
    # Prints the current state of the Board
    :param board: Board
    """
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []

        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])

        print('%s%d %s' % (bump, row, ''.join(line)))
        
    print('    ' + '  '.join(COLS[:board.num_cols]))

def point_from_coords(coords):
    """
    # Reads given coordinates into game coordinates
    :param coords: String
    :return: Point
    """
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)
