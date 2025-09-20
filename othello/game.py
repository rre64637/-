"""High level game orchestration for Othello."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .board import BLACK, WHITE, Board, InvalidMoveError, opponent

Move = Tuple[int, int]


def _winner_from_scores(scores: dict[str, int]) -> Optional[str]:
    if scores[BLACK] > scores[WHITE]:
        return BLACK
    if scores[WHITE] > scores[BLACK]:
        return WHITE
    return None


@dataclass
class MoveRecord:
    """A single move performed during the game."""

    player: str
    position: Optional[Move]
    flipped: int = 0


@dataclass
class OthelloGame:
    """Stateful controller for an Othello match."""

    board: Board = field(default_factory=Board)
    current_player: str = BLACK
    history: List[MoveRecord] = field(default_factory=list)
    finished: bool = False
    winner: Optional[str] = None

    def valid_moves(self) -> List[Move]:
        return self.board.valid_moves(self.current_player)

    def play_turn(self, move: Optional[Move]) -> None:
        """Play a move for the current player.

        Pass ``None`` as ``move`` to indicate a voluntary pass. The method
        raises :class:`InvalidMoveError` if the player still has legal moves.
        """

        if self.finished:
            raise RuntimeError("The game is already finished.")

        player = self.current_player

        if move is None:
            if self.board.has_any_valid_move(player):
                raise InvalidMoveError("Cannot pass while moves are available.")
            self.history.append(MoveRecord(player=player, position=None, flipped=0))
        else:
            row, col = move
            flipped = self.board.apply_move(row, col, player)
            self.history.append(MoveRecord(player=player, position=move, flipped=flipped))

        self._advance_turn(player)

    def _advance_turn(self, just_played: str) -> None:
        other = opponent(just_played)

        if self.board.is_full():
            self._finish_game()
            return

        if self.board.has_any_valid_move(other):
            self.current_player = other
            return

        if self.board.has_any_valid_move(just_played):
            # The opponent must pass automatically. Record it for completeness.
            self.history.append(MoveRecord(player=other, position=None, flipped=0))
            self.current_player = just_played
            return

        # No moves available for either player.
        self._finish_game()

    def _finish_game(self) -> None:
        self.finished = True
        scores = self.board.score()
        self.winner = _winner_from_scores(scores)

    def game_result(self) -> str:
        scores = self.board.score()
        if self.winner == BLACK:
            return f"Black wins {scores[BLACK]} - {scores[WHITE]}"
        if self.winner == WHITE:
            return f"White wins {scores[WHITE]} - {scores[BLACK]}"
        return f"Draw {scores[BLACK]} - {scores[WHITE]}"


def format_move(move: Optional[Move]) -> str:
    if move is None:
        return "pass"
    row, col = move
    return f"{chr(ord('a') + col)}{row + 1}"
