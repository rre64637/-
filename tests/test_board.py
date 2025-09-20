import pytest

from othello.board import BLACK, WHITE, Board, EMPTY, InvalidMoveError


def test_initial_board_setup():
    board = Board()
    assert board.get(3, 3) == WHITE
    assert board.get(3, 4) == BLACK
    assert board.get(4, 3) == BLACK
    assert board.get(4, 4) == WHITE

    scores = board.score()
    assert scores[BLACK] == 2
    assert scores[WHITE] == 2
    assert scores[EMPTY] == board.size * board.size - 4


def test_initial_valid_moves_for_black():
    board = Board()
    moves = sorted(board.valid_moves(BLACK))
    assert moves == [(2, 3), (3, 2), (4, 5), (5, 4)]


def test_initial_valid_moves_for_white():
    board = Board()
    moves = sorted(board.valid_moves(WHITE))
    assert moves == [(2, 4), (3, 5), (4, 2), (5, 3)]


def test_apply_move_flips_discs():
    board = Board()
    flipped = board.apply_move(2, 3, BLACK)
    assert flipped == 1
    assert board.get(2, 3) == BLACK
    assert board.get(3, 3) == BLACK


def test_invalid_move_raises():
    board = Board()
    with pytest.raises(InvalidMoveError):
        board.apply_move(0, 0, BLACK)


def test_has_any_valid_move():
    board = Board()
    assert board.has_any_valid_move(BLACK)
    assert board.has_any_valid_move(WHITE)

    for row in range(board.size):
        for col in range(board.size):
            board._grid[row][col] = BLACK
    board._grid[3][3] = WHITE
    board._grid[3][4] = EMPTY

    assert board.has_any_valid_move(BLACK)
    assert not board.has_any_valid_move(WHITE)


def test_clone_creates_independent_board():
    board = Board()
    clone = board.clone()
    clone.apply_move(2, 3, BLACK)
    assert board.get(2, 3) == EMPTY
    assert clone.get(2, 3) == BLACK
