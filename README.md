# Othello Game

This project is a digital version of the classic Othello (Reversi) board
game. It lets two players take turns placing discs on an 8×8 board while
capturing their opponent's pieces by sandwiching them horizontally,
vertically, or diagonally.

## Features
- Standard 8×8 Othello board with black and white discs
- Valid move highlighting and automatic capture rules
- Move validation, turn tracking, and score display
- Optional hints or AI opponent (if implemented)

## Getting Started
1. Install the required dependencies described in `package.json`.
2. Run the development server with `npm start` or launch the executable if
   available.
3. Open the application and follow the on‑screen prompts to begin playing.

## Gameplay Basics
- Players alternate turns placing a disc of their color.
- A move must capture at least one opponent disc by enclosing it between
  the newly placed disc and another of the player's discs.
- If a player has no valid moves, the turn passes to the opponent.
- The game ends when neither player can move; the player with the most
  discs of their color wins.

## Contributing
Pull requests are welcome. Please create feature branches, include tests
if applicable, and describe the changes clearly in the PR summary.