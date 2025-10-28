#!/usr/bin/env python3
"""
Othello (Reversi) Game Implementation
Supports Human vs Human and Human vs Machine modes
"""

import sys
from typing import List, Tuple, Optional


class OthelloBoard:
    """Represents the Othello game board and its state."""
    
    def __init__(self):
        """Initialize an 8x8 board with starting position."""
        self.size = 8
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        # Initial setup: center 4 squares
        mid = self.size // 2
        self.board[mid-1][mid-1] = 'W'
        self.board[mid-1][mid] = 'B'
        self.board[mid][mid-1] = 'B'
        self.board[mid][mid] = 'W'
        
    def display(self):
        """Display the current board state."""
        print("\n  ", end="")
        for i in range(self.size):
            print(f" {i} ", end="")
        print()
        
        for i in range(self.size):
            print(f"{i} ", end="")
            for j in range(self.size):
                piece = self.board[i][j]
                if piece == ' ':
                    print(" . ", end="")
                else:
                    print(f" {piece} ", end="")
            print()
        print()
        
    def get_piece(self, row: int, col: int) -> str:
        """Get the piece at the specified position."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col]
        return None
    
    def set_piece(self, row: int, col: int, player: str):
        """Place a piece on the board."""
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = player
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds."""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def count_pieces(self, player: str) -> int:
        """Count the number of pieces for a player."""
        count = 0
        for row in self.board:
            count += row.count(player)
        return count
    
    def get_score(self) -> Tuple[int, int]:
        """Get the current score (black, white)."""
        black = self.count_pieces('B')
        white = self.count_pieces('W')
        return black, white


class OthelloGame:
    """Manages the Othello game logic and rules."""
    
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    def __init__(self):
        """Initialize the game."""
        self.board = OthelloBoard()
        
    def get_opponent(self, player: str) -> str:
        """Get the opponent's color."""
        return 'W' if player == 'B' else 'B'
    
    def find_flips_in_direction(self, row: int, col: int, player: str, 
                                 direction: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Find pieces to flip in a specific direction."""
        dr, dc = direction
        flips = []
        r, c = row + dr, col + dc
        opponent = self.get_opponent(player)
        
        # Keep moving in direction while we see opponent pieces
        while self.board.is_valid_position(r, c) and self.board.get_piece(r, c) == opponent:
            flips.append((r, c))
            r += dr
            c += dc
        
        # Valid if we end on our own piece (and found at least one opponent piece)
        if flips and self.board.is_valid_position(r, c) and self.board.get_piece(r, c) == player:
            return flips
        return []
    
    def get_valid_moves(self, player: str) -> List[Tuple[int, int]]:
        """Get all valid moves for a player."""
        valid_moves = []
        
        for row in range(self.board.size):
            for col in range(self.board.size):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        
        return valid_moves
    
    def is_valid_move(self, row: int, col: int, player: str) -> bool:
        """Check if a move is valid."""
        # Must be on empty square
        if not self.board.is_valid_position(row, col) or self.board.get_piece(row, col) != ' ':
            return False
        
        # Must flip at least one opponent piece
        for direction in self.DIRECTIONS:
            if self.find_flips_in_direction(row, col, player, direction):
                return True
        
        return False
    
    def make_move(self, row: int, col: int, player: str) -> bool:
        """Make a move and flip opponent pieces."""
        if not self.is_valid_move(row, col, player):
            return False
        
        # Place the piece
        self.board.set_piece(row, col, player)
        
        # Flip pieces in all directions
        for direction in self.DIRECTIONS:
            flips = self.find_flips_in_direction(row, col, player, direction)
            for flip_row, flip_col in flips:
                self.board.set_piece(flip_row, flip_col, player)
        
        return True
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        # Game is over if neither player has valid moves
        return not self.get_valid_moves('B') and not self.get_valid_moves('W')
    
    def get_winner(self) -> Optional[str]:
        """Get the winner of the game."""
        black, white = self.board.get_score()
        if black > white:
            return 'B'
        elif white > black:
            return 'W'
        else:
            return None  # Tie


class AIPlayer:
    """AI player using minimax algorithm with alpha-beta pruning."""
    
    def __init__(self, player: str, difficulty: int = 3):
        """
        Initialize AI player.
        
        Args:
            player: 'B' or 'W'
            difficulty: Search depth (1-5, higher is smarter but slower)
        """
        self.player = player
        self.difficulty = difficulty
        
    def get_move(self, game: OthelloGame) -> Optional[Tuple[int, int]]:
        """Get the best move using minimax algorithm."""
        valid_moves = game.get_valid_moves(self.player)
        if not valid_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in valid_moves:
            # Create a copy of the game state
            temp_game = self._copy_game(game)
            temp_game.make_move(move[0], move[1], self.player)
            
            # Evaluate this move
            score = self._minimax(temp_game, self.difficulty - 1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
        
        return best_move
    
    def _minimax(self, game: OthelloGame, depth: int, alpha: float, beta: float, 
                 is_maximizing: bool) -> float:
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or game.is_game_over():
            return self._evaluate_board(game)
        
        current_player = self.player if is_maximizing else game.get_opponent(self.player)
        valid_moves = game.get_valid_moves(current_player)
        
        # If no valid moves, pass to opponent
        if not valid_moves:
            return self._minimax(game, depth - 1, alpha, beta, not is_maximizing)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                temp_game = self._copy_game(game)
                temp_game.make_move(move[0], move[1], current_player)
                eval_score = self._minimax(temp_game, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                temp_game = self._copy_game(game)
                temp_game.make_move(move[0], move[1], current_player)
                eval_score = self._minimax(temp_game, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def _evaluate_board(self, game: OthelloGame) -> float:
        """Evaluate the board state for the AI player."""
        # Positional weights (corners and edges are valuable)
        weights = [
            [100, -20, 10,  5,  5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [ 10,  -2, -1, -1, -1, -1,  -2,  10],
            [  5,  -2, -1, -1, -1, -1,  -2,   5],
            [  5,  -2, -1, -1, -1, -1,  -2,   5],
            [ 10,  -2, -1, -1, -1, -1,  -2,  10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10,  5,  5, 10, -20, 100]
        ]
        
        score = 0
        opponent = game.get_opponent(self.player)
        
        for row in range(game.board.size):
            for col in range(game.board.size):
                piece = game.board.get_piece(row, col)
                if piece == self.player:
                    score += weights[row][col]
                elif piece == opponent:
                    score -= weights[row][col]
        
        # Also consider piece count
        my_pieces = game.board.count_pieces(self.player)
        opponent_pieces = game.board.count_pieces(opponent)
        score += (my_pieces - opponent_pieces) * 2
        
        return score
    
    def _copy_game(self, game: OthelloGame) -> OthelloGame:
        """Create a deep copy of the game state."""
        new_game = OthelloGame()
        for row in range(game.board.size):
            for col in range(game.board.size):
                new_game.board.board[row][col] = game.board.board[row][col]
        return new_game


def get_human_move(game: OthelloGame, player: str) -> Optional[Tuple[int, int]]:
    """Get a move from a human player."""
    valid_moves = game.get_valid_moves(player)
    
    if not valid_moves:
        print("No valid moves available. Press Enter to pass turn.")
        input()
        return None
    
    print(f"Valid moves: {valid_moves}")
    
    while True:
        try:
            move_input = input("Enter your move (row col), e.g., '3 4': ").strip()
            if not move_input:
                continue
            
            parts = move_input.split()
            if len(parts) != 2:
                print("Invalid input. Please enter row and column separated by space.")
                continue
            
            row, col = int(parts[0]), int(parts[1])
            
            if (row, col) in valid_moves:
                return (row, col)
            else:
                print(f"Invalid move. Please choose from: {valid_moves}")
        except ValueError:
            print("Invalid input. Please enter numbers only.")
        except KeyboardInterrupt:
            print("\nGame interrupted.")
            sys.exit(0)


def main():
    """Main game loop."""
    print("=" * 50)
    print("Welcome to Othello (Reversi)!")
    print("=" * 50)
    print("\nGame Rules:")
    print("- Black (B) goes first")
    print("- Place pieces to flip opponent's pieces")
    print("- Winner has the most pieces when no moves remain")
    print()
    
    # Game mode selection
    while True:
        print("Select game mode:")
        print("1. Human vs Human")
        print("2. Human vs Machine")
        print("3. Quit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '3':
            print("Thanks for playing!")
            sys.exit(0)
        
        if choice not in ['1', '2']:
            print("Invalid choice. Please try again.\n")
            continue
        
        # Initialize game
        game = OthelloGame()
        ai_player = None
        
        if choice == '2':
            # Select difficulty for AI
            while True:
                try:
                    difficulty = input("Select AI difficulty (1=Easy, 3=Medium, 5=Hard): ").strip()
                    difficulty = int(difficulty)
                    if 1 <= difficulty <= 5:
                        break
                    print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            # Ask who plays as Black
            while True:
                color_choice = input("Do you want to play as Black (goes first)? (y/n): ").strip().lower()
                if color_choice in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'.")
            
            if color_choice == 'y':
                ai_player = AIPlayer('W', difficulty)
                print("\nYou are Black (B), AI is White (W).")
            else:
                ai_player = AIPlayer('B', difficulty)
                print("\nYou are White (W), AI is Black (B).")
        else:
            print("\nPlayer 1 is Black (B), Player 2 is White (W).")
        
        # Game loop
        current_player = 'B'
        consecutive_passes = 0
        
        while not game.is_game_over():
            game.board.display()
            black, white = game.board.get_score()
            print(f"Score - Black: {black}, White: {white}")
            
            player_name = f"{'Black' if current_player == 'B' else 'White'}"
            print(f"\n{player_name}'s turn:")
            
            # Get move based on player type
            if ai_player and ai_player.player == current_player:
                print("AI is thinking...")
                move = ai_player.get_move(game)
            else:
                move = get_human_move(game, current_player)
            
            # Make the move
            if move is None:
                print(f"{player_name} has no valid moves and passes.")
                consecutive_passes += 1
                if consecutive_passes >= 2:
                    break
            else:
                consecutive_passes = 0
                row, col = move
                game.make_move(row, col, current_player)
                print(f"{player_name} played at ({row}, {col})")
            
            # Switch player
            current_player = game.get_opponent(current_player)
        
        # Game over
        game.board.display()
        black, white = game.board.get_score()
        print("=" * 50)
        print("GAME OVER!")
        print(f"Final Score - Black: {black}, White: {white}")
        
        winner = game.get_winner()
        if winner == 'B':
            print("Black wins!")
        elif winner == 'W':
            print("White wins!")
        else:
            print("It's a tie!")
        print("=" * 50)
        print()


if __name__ == "__main__":
    main()
