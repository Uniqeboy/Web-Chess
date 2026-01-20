def create_game():
    return {
        "board": [
            ['r','n','b','q','k','b','n','r'],
            ['p','p','p','p','p','p','p','p'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['P','P','P','P','P','P','P','P'],
            ['R','N','B','Q','K','B','N','R']
        ],
        "has_moved": {
            'white_king': False,
            'white_rook_a': False,
            'white_rook_h': False,
            'black_king': False,
            'black_rook_a': False,
            'black_rook_h': False
        }
    }


def is_valid_pawn_move(board, r1, c1, r2, c2, piece):
    direction = -1 if piece == 'P' else 1
    # -------- Forward move --------
    if c1 == c2 and board[r2][c2] == '.':
        # one step
        if r2 == r1 + direction:
            return True
        # two steps (first move only)
        if piece == 'P' and r1 == 6 and r2 == 4 and board[5][c1] == '.':
            return True
        if piece == 'p' and r1 == 1 and r2 == 3 and board[2][c1] == '.':
            return True
    # -------- Capture --------
    if abs(c2 - c1) == 1 and r2 == r1 + direction:
        if board[r2][c2] != '.' and board[r2][c2].islower() != piece.islower():
            return True
    return False


def is_rook_path_clear(board, r1, c1, r2, c2):
    # Horizontal move
    if r1 == r2:
        step = 1 if c2 > c1 else -1
        for c in range(c1 + step, c2, step):
            if board[r1][c] != '.':
                return False
    # Vertical move
    elif c1 == c2:
        step = 1 if r2 > r1 else -1
        for r in range(r1 + step, r2, step):
            if board[r][c1] != '.':
                return False
    return True


def is_valid_rook_move(board, r1, c1, r2, c2, piece):
    # Rook moves only in straight line
    if r1 != r2 and c1 != c2:
        return False
    # Rook cannot jump over pieces
    if not is_rook_path_clear(board, r1, c1, r2, c2):
        return False
    # Destination must be empty or opponent
    if board[r2][c2] == '.' or board[r2][c2].islower() != piece.islower():
        return True
    return False


def is_valid_knight_move(board, r1, c1, r2, c2, piece):
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    # L-shape move
    if not ((dr == 2 and dc == 1) or (dr == 1 and dc == 2)):
        return False
    # Destination must be empty or opponent
    if board[r2][c2] == '.' or board[r2][c2].islower() != piece.islower():
        return True
    return False


def is_bishop_path_clear(board, r1, c1, r2, c2):
    row_step = 1 if r2 > r1 else -1
    col_step = 1 if c2 > c1 else -1
    r = r1 + row_step
    c = c1 + col_step
    while r != r2 and c != c2:
        if board[r][c] != '.':
            return False
        r += row_step
        c += col_step
    return True


def is_valid_bishop_move(board, r1, c1, r2, c2, piece):
    # Must be diagonal
    if abs(r2 - r1) != abs(c2 - c1):
        return False
    # Path must be clear
    if not is_bishop_path_clear(board, r1, c1, r2, c2):
        return False
    # Destination must be empty or opponent
    if board[r2][c2] == '.' or board[r2][c2].islower() != piece.islower():
        return True
    return False


def is_valid_queen_move(board, r1, c1, r2, c2, piece):
    # Queen moves like rook OR bishop
    if is_valid_rook_move(board, r1, c1, r2, c2, piece):
        return True
    if is_valid_bishop_move(board, r1, c1, r2, c2, piece):
        return True
    return False


def is_valid_king_move(board, r1, c1, r2, c2, piece):
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    # King moves only one square
    if dr > 1 or dc > 1:
        return False
    # Destination must be empty or opponent
    if board[r2][c2] == '.' or board[r2][c2].islower() != piece.islower():
        return True
    return False


def find_king(board, turn):
    king = 'K' if turn == 'white' else 'k'
    for r in range(8):
        for c in range(8):
            if board[r][c] == king:
                return r, c
    return None


def is_square_attacked(board, r, c, turn):
    enemy_is_white = (turn == 'black')
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == '.':
                continue
            if enemy_is_white and piece.isupper():
                if can_piece_attack_square(board, i, j, r, c, piece):
                    return True

            if not enemy_is_white and piece.islower():
                if can_piece_attack_square(board, i, j, r, c, piece):
                    return True
    return False


def is_king_in_check(board, turn):
    pos = find_king(board, turn)
    if pos is None:
        return True   # king missing = game over
    r, c = pos
    return is_square_attacked(board, r, c, turn)


def does_move_leave_king_in_check(board, r1, c1, r2, c2, turn):
    temp = board[r2][c2]
    board[r2][c2] = board[r1][c1]
    board[r1][c1] = '.'
    in_check = is_king_in_check(board, turn)
    board[r1][c1] = board[r2][c2]
    board[r2][c2] = temp
    return in_check


def has_any_legal_move(game, turn):
    board = game["board"]
    for r1 in range(8):
        for c1 in range(8):
            piece = board[r1][c1]
            if piece == '.':
                continue
            if turn == 'white' and piece.islower():
                continue
            if turn == 'black' and piece.isupper():
                continue
            for r2 in range(8):
                for c2 in range(8):
                    if is_valid_move(game, r1, c1, r2, c2, turn):
                        return True
    return False


def check_game_status(game, turn):
    board = game["board"]
    if is_king_in_check(board, turn):
        if not has_any_legal_move(game, turn):
            return 'checkmate'
        elif turn == 'white':
            return 'check_white'
        elif turn == 'black':
            return 'check_black'
    else:
        if not has_any_legal_move(game, turn):
            return 'stalemate'
    return 'ok'


def make_move(game, r1, c1, r2, c2, promotion=None):
    board = game["board"]
    moved = game["has_moved"]
    piece = board[r1][c1]
    # ---- Castling move ----
    if piece.upper() == 'K' and abs(c2 - c1) == 2:
        side = 'king' if c2 > c1 else 'queen'
        do_castling(game, 'white' if piece.isupper() else 'black', side)
        return
    board[r2][c2] = piece
    board[r1][c1] = '.'
    # ---- Update moved flags ----
    if piece == 'K':
        moved['white_king'] = True
    elif piece == 'k':
        moved['black_king'] = True
    elif piece == 'R' and r1 == 7 and c1 == 0:
        moved['white_rook_a'] = True
    elif piece == 'R' and r1 == 7 and c1 == 7:
        moved['white_rook_h'] = True
    elif piece == 'r' and r1 == 0 and c1 == 0:
        moved['black_rook_a'] = True
    elif piece == 'r' and r1 == 0 and c1 == 7:
        moved['black_rook_h'] = True
    # ---- Pawn promotion ----
    if piece == 'P' and r2 == 0:
        board[r2][c2] = promotion if promotion else 'Q'
    elif piece == 'p' and r2 == 7:
        board[r2][c2] = promotion if promotion else 'q'



def is_valid_castling(game, turn, side):
    board = game["board"]
    moved = game["has_moved"]
    row = 7 if turn == 'white' else 0
    if side == 'king':  # kingside
        between = [5, 6]
    else:               # queenside
        between = [1, 2, 3]
    # Check if king or rook moved
    if turn == 'white':
        if moved['white_king']:
            return False
        if side == 'king' and moved['white_rook_h']:
            return False
        if side == 'queen' and moved['white_rook_a']:
            return False
    else:
        if moved['black_king']:
            return False
        if side == 'king' and moved['black_rook_h']:
            return False
        if side == 'queen' and moved['black_rook_a']:
            return False
    # Squares between must be empty
    for c in between:
        if board[row][c] != '.':
            return False
    # Cannot castle through or out of check
    if is_square_attacked(board, row, 4, turn):
        return False
    for c in between:
        if is_square_attacked(board, row, c, turn):
            return False
    return True


def do_castling(game, turn, side):
    board = game["board"]
    moved = game["has_moved"]
    row = 7 if turn == 'white' else 0
    if side == 'king':
        board[row][6] = board[row][4]
        board[row][4] = '.'
        board[row][5] = board[row][7]
        board[row][7] = '.'
    else:
        board[row][2] = board[row][4]
        board[row][4] = '.'
        board[row][3] = board[row][0]
        board[row][0] = '.'
    if turn == 'white':
        moved['white_king'] = True
        if side == 'king':
            moved['white_rook_h'] = True
        else:
            moved['white_rook_a'] = True
    else:
        moved['black_king'] = True
        if side == 'king':
            moved['black_rook_h'] = True
        else:
            moved['black_rook_a'] = True


def is_valid_move(game, r1, c1, r2, c2, turn):
    board = game["board"]
    if not (0 <= r1 < 8 and 0 <= c1 < 8 and 0 <= r2 < 8 and 0 <= c2 < 8):
        return False
    if r1 == r2 and c1 == c2:
        return False
    piece = board[r1][c1]
    if piece == '.':
        return False
    dest = board[r2][c2]
    if dest != '.' and dest.isupper() == piece.isupper():
        return False
    if turn == 'white' and piece.islower():
        return False
    if turn == 'black' and piece.isupper():
        return False
    # ---- Castling via king move ----
    if piece.upper() == 'K' and abs(c2 - c1) == 2:
        side = 'king' if c2 > c1 else 'queen'
        return is_valid_castling(game, turn, side)
    if piece.upper() == 'P':
        valid = is_valid_pawn_move(board, r1, c1, r2, c2, piece)
    elif piece.upper() == 'R':
        valid = is_valid_rook_move(board, r1, c1, r2, c2, piece)
    elif piece.upper() == 'N':
        valid = is_valid_knight_move(board, r1, c1, r2, c2, piece)
    elif piece.upper() == 'B':
        valid = is_valid_bishop_move(board, r1, c1, r2, c2, piece)
    elif piece.upper() == 'Q':
        valid = is_valid_queen_move(board, r1, c1, r2, c2, piece)
    elif piece.upper() == 'K':
        valid = is_valid_king_move(board, r1, c1, r2, c2, piece)
    else:
        return False
    if not valid:
        return False
    if does_move_leave_king_in_check(board, r1, c1, r2, c2, turn):
        return False
    return True


def can_piece_attack_square(board, r1, c1, r2, c2, piece):
    if piece.upper() == 'P':
        direction = -1 if piece == 'P' else 1
        return abs(c2 - c1) == 1 and r2 == r1 + direction
    elif piece.upper() == 'R':
        if r1 != r2 and c1 != c2:
            return False
        return is_rook_path_clear(board, r1, c1, r2, c2)
    elif piece.upper() == 'N':
        dr = abs(r2 - r1)
        dc = abs(c2 - c1)
        return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)
    elif piece.upper() == 'B':
        if abs(r2 - r1) != abs(c2 - c1):
            return False
        return is_bishop_path_clear(board, r1, c1, r2, c2)
    elif piece.upper() == 'Q':
        if r1 == r2 or c1 == c2:
            return is_rook_path_clear(board, r1, c1, r2, c2)
        if abs(r2 - r1) == abs(c2 - c1):
            return is_bishop_path_clear(board, r1, c1, r2, c2)
        return False
    elif piece.upper() == 'K':
        return abs(r2 - r1) <= 1 and abs(c2 - c1) <= 1
    return False




"""
play()
 │
 ├─ print_board(board)
 │
 ├─ check_game_status(board, turn)
 │    ├─ is_king_in_check(board, turn)
 │    │     ├─ find_king(board, turn)
 │    │     └─ is_square_attacked(board, r, c, turn)
 │    │            └─ is_valid_move(board, i, j, r, c, enemy_turn)   <- recursive check
 │    └─ has_any_legal_move(board, turn)
 │           └─ is_valid_move(board, r1, c1, r2, c2, turn)
 │                  ├─ Pawn: is_valid_pawn_move(...)
 │                  ├─ Rook: is_valid_rook_move(...)
 │                  │       └─ is_rook_path_clear(...)
 │                  ├─ Knight: is_valid_knight_move(...)
 │                  ├─ Bishop: is_valid_bishop_move(...)
 │                  │       └─ is_bishop_path_clear(...)
 │                  ├─ Queen: is_valid_queen_move(...)
 │                  │       ├─ is_valid_rook_move(...)
 │                  │       └─ is_valid_bishop_move(...)
 │                  └─ King: is_valid_king_move(...)
 │
 ├─ Castling Handling
 │     ├─ is_valid_castling(board, turn, side)
 │     └─ do_castling(board, turn, side)
 │
 ├─ Move Parsing / Execution
 │     ├─ parse_move(move) -> (r1, c1, r2, c2)
 │     ├─ is_valid_move(board, r1, c1, r2, c2, turn)
 │     └─ make_move(board, r1, c1, r2, c2)
 │            └─ Pawn Promotion Handling
 │
 └─ Turn Switching
       turn = 'black' if turn == 'white' else 'white'
"""