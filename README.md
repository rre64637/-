# Othello

A simple terminal-based implementation of the classic Othello/Reversi board game. The game includes:

- Core board logic with move validation and disc flipping.
- A light-weight heuristic AI opponent that prioritises strong board positions.
- A command-line interface for human vs. human or human vs. AI matches.

## Playing the game

```bash
python -m othello.cli [--ai {none,black,white}] [--randomness FLOAT]
```

Use coordinates such as `d3` or `4 5` when prompted. Enter `pass` when you have no valid moves.

By default the AI controls the white pieces while you play as black. Use `--ai none` to play a two-player hot-seat match or `--ai black` to let the AI take the first turn.

## Running the tests

```bash
pytest
```
