#!/usr/bin/env python3
"""
Visual demo for screenshot - shows the game interface
"""

from othello import OthelloGame, AIPlayer


def show_game_demo():
    """Demonstrate the game interface with a few moves."""
    print("=" * 50)
    print("Welcome to Othello (Reversi)!")
    print("=" * 50)
    print("\nGame Rules:")
    print("- Black (B) goes first")
    print("- Place pieces to flip opponent's pieces")
    print("- Winner has the most pieces when no moves remain")
    print()
    
    print("Select game mode:")
    print("1. Human vs Human")
    print("2. Human vs Machine")
    print("3. Quit")
    print("Enter your choice (1-3): 2")
    print()
    print("Select AI difficulty (1=Easy, 3=Medium, 5=Hard): 3")
    print("Do you want to play as Black (goes first)? (y/n): y")
    print()
    print("You are Black (B), AI is White (W).")
    print()
    
    # Initialize game
    game = OthelloGame()
    ai = AIPlayer('W', difficulty=3)
    
    # Show initial board
    game.board.display()
    black, white = game.board.get_score()
    print(f"Score - Black: {black}, White: {white}")
    
    # Black's turn
    print("\nBlack's turn:")
    valid_moves = game.get_valid_moves('B')
    print(f"Valid moves: {valid_moves}")
    print("Enter your move (row col), e.g., '3 4': 2 3")
    
    # Make the move
    game.make_move(2, 3, 'B')
    print("\nBlack played at (2, 3)")
    print()
    game.board.display()
    black, white = game.board.get_score()
    print(f"Score - Black: {black}, White: {white}")
    
    # AI's turn
    print("\nWhite's turn:")
    print("AI is thinking...")
    ai_move = ai.get_move(game)
    game.make_move(ai_move[0], ai_move[1], 'W')
    print(f"AI played at {ai_move}")
    print()
    game.board.display()
    black, white = game.board.get_score()
    print(f"Score - Black: {black}, White: {white}")
    
    # Another round
    print("\nBlack's turn:")
    valid_moves = game.get_valid_moves('B')
    print(f"Valid moves: {valid_moves}")
    print("Enter your move (row col), e.g., '3 4': 5 2")
    
    game.make_move(5, 2, 'B')
    print("\nBlack played at (5, 2)")
    print()
    game.board.display()
    black, white = game.board.get_score()
    print(f"Score - Black: {black}, White: {white}")
    
    print("\n" + "=" * 50)
    print("Game continues...")
    print("Run 'python3 othello.py' to play a full game!")
    print("=" * 50)


if __name__ == "__main__":
    show_game_demo()
