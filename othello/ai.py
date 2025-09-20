"""Simple heuristic AI for the Othello game."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional, Tuple

from .board import Board, opponent

Move = Tuple[int, int]

# Positional weights encourage the AI to prioritise corners and edges.
POSITION_WEIGHTS: Tuple[Tuple[int, ...], ...] = (
    (100, -20, 10, 5, 5, 10, -20, 100),
    (-20, -50, -2, -2, -2, -2, -50, -20),
    (10, -2, 5, 1, 1, 5, -2, 10),
    (5, -2, 1, 0, 0, 1, -2, 5),
    (5, -2, 1, 0, 0, 1, -2, 5),
    (10, -2, 5, 1, 1, 5, -2, 10),
    (-20, -50, -2, -2, -2, -2, -50, -20),
    (100, -20, 10, 5, 5, 10, -20, 100),
)


@dataclass
class HeuristicAI:
    """A lightweight opponent powered by a static evaluation function."""

    randomness: float = 0.0
    rng: random.Random = field(init=False, repr=False, default_factory=random.Random)

    def choose_move(self, board: Board, color: str) -> Optional[Move]:
        moves = board.valid_moves(color)
        if not moves:
            return None

        scored_moves = [(self._evaluate_move(board, color, move), move) for move in moves]
        scored_moves.sort(key=lambda item: item[0], reverse=True)

        if self.randomness > 0 and len(scored_moves) > 1:
            threshold = max(0.0, min(1.0, self.randomness))
            if self.rng.random() < threshold:
                return self.rng.choice([move for _, move in scored_moves])

        return scored_moves[0][1]

    def _evaluate_move(self, board: Board, color: str, move: Move) -> float:
        row, col = move
        clone = board.clone()
        flipped = clone.apply_move(row, col, color)
        mobility = len(clone.valid_moves(color)) - len(clone.valid_moves(opponent(color)))
        return (
            float(POSITION_WEIGHTS[row][col])
            + flipped * 5.0
            + mobility * 0.5
        )
