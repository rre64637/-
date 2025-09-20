"""Command line interface for playing Othello."""
from __future__ import annotations

import argparse
from typing import Iterable, List, Optional

from .ai import HeuristicAI
from .board import BLACK, WHITE, Board
from .game import OthelloGame, format_move

Move = tuple[int, int]


def parse_move(text: str) -> Optional[Move]:
    cleaned = text.strip().lower()
    if cleaned in {"pass", "p"}:
        return None

    if len(cleaned) == 2 and cleaned[0].isalpha() and cleaned[1].isdigit():
        col = ord(cleaned[0]) - ord("a")
        row = int(cleaned[1]) - 1
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)

    if "," in cleaned:
        parts = cleaned.split(",")
    else:
        parts = cleaned.split()

    if len(parts) == 2 and all(part.isdigit() for part in parts):
        row, col = (int(parts[0]) - 1, int(parts[1]) - 1)
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)

    raise ValueError("Invalid move format. Use e.g. 'd3' or '4 5'.")


def colour_name(colour: str) -> str:
    return "Black" if colour == BLACK else "White"


def display_board(board: Board) -> None:
    print()
    for line in board.to_lines():
        print(line)
    scores = board.score()
    print(f"Black: {scores[BLACK]}    White: {scores[WHITE]}")


def human_turn(colour: str, moves: Iterable[Move]) -> Optional[Move]:
    move_list = sorted(moves)
    readable_moves = ", ".join(format_move(move) for move in move_list)
    prompt = f"{colour_name(colour)} to move. Enter a move ({readable_moves}) or 'pass': "
    while True:
        try:
            raw = input(prompt)
        except EOFError:  # pragma: no cover - interactive guard
            raise SystemExit(0)
        try:
            move = parse_move(raw)
        except ValueError as exc:
            print(exc)
            continue

        if move is None:
            if move_list:
                print("You still have legal moves and cannot pass.")
                continue
            return None
        if move not in move_list:
            print("That move is not legal. Try again.")
            continue
        return move


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play a game of Othello in the terminal.")
    parser.add_argument(
        "--ai",
        choices=["none", "black", "white"],
        default="white",
        help="Choose which side is played by the computer.",
    )
    parser.add_argument(
        "--randomness",
        type=float,
        default=0.2,
        help="Probability of the AI selecting a sub-optimal move.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    ai = HeuristicAI(randomness=args.randomness)
    ai_sides = {
        "black": {BLACK},
        "white": {WHITE},
        "none": set(),
    }[args.ai]

    game = OthelloGame()
    print("Welcome to Othello! Coordinates are entered as column+row (e.g. d3).")

    while not game.finished:
        display_board(game.board)
        colour = game.current_player
        moves = game.valid_moves()

        if not moves:
            print(f"{colour_name(colour)} has no legal moves and must pass.")
            game.play_turn(None)
            continue

        if colour in ai_sides:
            move = ai.choose_move(game.board, colour)
            if move is None:
                print(f"{colour_name(colour)} cannot move and passes.")
            else:
                print(f"{colour_name(colour)} (AI) plays {format_move(move)}")
        else:
            move = human_turn(colour, moves)
        game.play_turn(move)

        last = game.history[-1]
        if last.position is None and last.player != game.current_player:
            print(f"{colour_name(last.player)} has no moves and passes.")

    display_board(game.board)
    print(game.game_result())


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
