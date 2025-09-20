import pytest

from othello.board import BLACK, WHITE, EMPTY, InvalidMoveError
from othello.game import OthelloGame


def test_switch_turns_after_regular_move():
    game = OthelloGame()
    move = sorted(game.valid_moves())[0]
    game.play_turn(move)
    assert game.current_player == WHITE
    assert game.history[-1].position == move


def test_cannot_pass_when_moves_exist():
    game = OthelloGame()
    with pytest.raises(InvalidMoveError):
        game.play_turn(None)


def test_forced_pass_is_recorded():
    game = OthelloGame()
    board = game.board
    for row in range(board.size):
        for col in range(board.size):
            board._grid[row][col] = BLACK
    board._grid[4][5] = WHITE
    board._grid[5][3] = WHITE
    board._grid[5][4] = EMPTY
    board._grid[5][5] = EMPTY

    game.current_player = BLACK
    game.history.clear()

    move = (5, 5)
    game.play_turn(move)

    assert game.current_player == BLACK
    assert len(game.history) == 2
    assert game.history[-1].position is None
    assert game.history[-1].player == WHITE


def test_game_finishes_when_board_full():
    game = OthelloGame()
    board = game.board
    for row in range(board.size):
        for col in range(board.size):
            board._grid[row][col] = BLACK
    board._grid[0][0] = WHITE
    board._grid[0][1] = EMPTY
    board._grid[0][2] = BLACK
    board._grid[0][3] = WHITE

    game.current_player = WHITE
    game.finished = False
    game.history.clear()

    game.play_turn((0, 1))
    assert game.finished
    assert game.winner in {BLACK, WHITE, None}
