"""Simple Othello game package."""

from .board import Board, BLACK, WHITE, EMPTY, opponent
from .game import OthelloGame

__all__ = [
    "Board",
    "BLACK",
    "WHITE",
    "EMPTY",
    "opponent",
    "OthelloGame",
]
