"""Core board representation for the Othello game."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

BLACK = "B"
WHITE = "W"
EMPTY = "."

DIRECTIONS: Tuple[Tuple[int, int], ...] = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


class InvalidMoveError(ValueError):
    """Raised when a move cannot legally be played on the board."""


@dataclass
class Board:
    """Representation of an 8x8 Othello board."""

    size: int = 8

    def __post_init__(self) -> None:
        self._grid: List[List[str]] = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.reset()

    def reset(self) -> None:
        """Reset the board to the initial game state."""
        for row in range(self.size):
            for col in range(self.size):
                self._grid[row][col] = EMPTY

        middle = self.size // 2
        self._grid[middle - 1][middle - 1] = WHITE
        self._grid[middle][middle] = WHITE
        self._grid[middle - 1][middle] = BLACK
        self._grid[middle][middle - 1] = BLACK

    def clone(self) -> "Board":
        """Return a copy of the board."""
        new_board = Board(self.size)
        new_board._grid = [row[:] for row in self._grid]
        return new_board

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def get(self, row: int, col: int) -> str:
        if not self.in_bounds(row, col):
            raise IndexError("Position outside of the board")
        return self._grid[row][col]

    def _captures_from(self, row: int, col: int, color: str) -> List[Tuple[int, int]]:
        if self._grid[row][col] != EMPTY:
            return []

        captured: List[Tuple[int, int]] = []
        for d_row, d_col in DIRECTIONS:
            line: List[Tuple[int, int]] = []
            r, c = row + d_row, col + d_col
            while self.in_bounds(r, c) and self._grid[r][c] == opponent(color):
                line.append((r, c))
                r += d_row
                c += d_col
            if line and self.in_bounds(r, c) and self._grid[r][c] == color:
                captured.extend(line)
        return captured

    def valid_moves(self, color: str) -> List[Tuple[int, int]]:
        """Return a list of legal moves for ``color``."""
        moves: List[Tuple[int, int]] = []
        for row in range(self.size):
            for col in range(self.size):
                if self._grid[row][col] != EMPTY:
                    continue
                if self._captures_from(row, col, color):
                    moves.append((row, col))
        return moves

    def apply_move(self, row: int, col: int, color: str) -> int:
        """Place a disc on the board and flip captured discs.

        Args:
            row: Row index of the move (0-based).
            col: Column index of the move (0-based).
            color: Disc colour, ``BLACK`` or ``WHITE``.

        Returns:
            The number of discs flipped by the move.

        Raises:
            InvalidMoveError: If the move is illegal.
        """

        captured = self._captures_from(row, col, color)
        if not captured:
            raise InvalidMoveError(f"Illegal move at ({row}, {col}) for {color}.")

        self._grid[row][col] = color
        for r, c in captured:
            self._grid[r][c] = color
        return len(captured)

    def has_any_valid_move(self, color: str) -> bool:
        for row in range(self.size):
            for col in range(self.size):
                if self._grid[row][col] == EMPTY and self._captures_from(row, col, color):
                    return True
        return False

    def is_full(self) -> bool:
        return all(cell != EMPTY for row in self._grid for cell in row)

    def score(self) -> Dict[str, int]:
        counts = {BLACK: 0, WHITE: 0, EMPTY: 0}
        for row in self._grid:
            for cell in row:
                counts[cell] += 1
        return counts

    def to_lines(self) -> List[str]:
        header = "  " + " ".join(chr(ord("a") + i) for i in range(self.size))
        lines = [header]
        for idx, row in enumerate(self._grid, 1):
            lines.append(f"{idx} " + " ".join(row))
        return lines

    def __str__(self) -> str:  # pragma: no cover - trivial formatting
        return "\n".join(self.to_lines())


def opponent(color: str) -> str:
    if color == BLACK:
        return WHITE
    if color == WHITE:
        return BLACK
    raise ValueError(f"Unknown disc colour: {color}")
