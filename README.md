# Othello Game

A command-line implementation of the classic Othello (Reversi) board game in Python, featuring both Human vs Human and Human vs Machine gameplay modes.

## Features

- **Two Game Modes:**
  - Human vs Human: Play against a friend locally
  - Human vs Machine: Challenge an AI opponent with adjustable difficulty

- **Smart AI Player:**
  - Uses minimax algorithm with alpha-beta pruning
  - Configurable difficulty levels (1-5)
  - Strategic positional evaluation

- **User-Friendly Interface:**
  - Clear board visualization
  - Valid move suggestions
  - Real-time score tracking
  - Game rules display

## Requirements

- Python 3.6 or higher
- No external dependencies required

## How to Play

### Running the Game

```bash
python3 othello.py
```

### Game Rules

1. **Objective:** Have the most pieces of your color on the board when the game ends
2. **Starting Position:** The game begins with 4 pieces in the center (2 black, 2 white)
3. **Gameplay:**
   - Black always goes first
   - Players alternate turns placing pieces on the board
   - A valid move must flip at least one opponent piece
   - Pieces are flipped when sandwiched between your pieces
   - If a player has no valid moves, they must pass
   - Game ends when neither player can make a move

4. **Winning:** The player with the most pieces wins

### Making Moves

When it's your turn, enter your move as two numbers separated by a space:
```
Enter your move (row col), e.g., '3 4': 2 3
```

The board uses 0-based indexing (0-7 for both rows and columns).

### Game Modes

#### Human vs Human
- Two players take turns on the same computer
- Perfect for local multiplayer

#### Human vs Machine
- Play against an AI opponent
- Choose difficulty level:
  - 1 = Easy (quick decisions, basic strategy)
  - 3 = Medium (balanced performance)
  - 5 = Hard (advanced strategy, slower)
- Choose your color (Black goes first)

## Project Structure

```
othello_game/
├── othello.py          # Main game implementation
├── test_othello.py     # Unit tests
└── README.md          # This file
```

## Running Tests

Run the test suite to verify the game logic:

```bash
python3 -m unittest test_othello -v
```

All tests should pass, covering:
- Board initialization and manipulation
- Move validation
- Game logic and rules
- AI player behavior
- Full game scenarios

## Implementation Details

### Classes

- **OthelloBoard**: Manages the 8x8 game board and piece placement
- **OthelloGame**: Implements game rules, move validation, and win conditions
- **AIPlayer**: Provides computer opponent using minimax with alpha-beta pruning

### AI Strategy

The AI evaluates board positions using:
- **Positional weights**: Corners and edges are highly valued
- **Piece count**: Number of pieces for each player
- **Minimax search**: Looks ahead multiple moves to find optimal play

## Example Game Session

```
==================================================
Welcome to Othello (Reversi)!
==================================================

Game Rules:
- Black (B) goes first
- Place pieces to flip opponent's pieces
- Winner has the most pieces when no moves remain

Select game mode:
1. Human vs Human
2. Human vs Machine
3. Quit
Enter your choice (1-3): 2

Select AI difficulty (1=Easy, 3=Medium, 5=Hard): 3
Do you want to play as Black (goes first)? (y/n): y

You are Black (B), AI is White (W).

     0  1  2  3  4  5  6  7 
0  .  .  .  .  .  .  .  . 
1  .  .  .  .  .  .  .  . 
2  .  .  .  .  .  .  .  . 
3  .  .  .  W  B  .  .  . 
4  .  .  .  B  W  .  .  . 
5  .  .  .  .  .  .  .  . 
6  .  .  .  .  .  .  .  . 
7  .  .  .  .  .  .  .  . 

Score - Black: 2, White: 2

Black's turn:
Valid moves: [(2, 3), (3, 2), (4, 5), (5, 4)]
Enter your move (row col), e.g., '3 4': 2 3
...
```

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Author

Created as a demonstration of game AI and object-oriented programming in Python.