#!/usr/bin/env python3
"""
Unit tests for Othello game
"""

import unittest
from othello import OthelloBoard, OthelloGame, AIPlayer


class TestOthelloBoard(unittest.TestCase):
    """Test the OthelloBoard class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.board = OthelloBoard()
    
    def test_initial_setup(self):
        """Test that the board is set up correctly."""
        # Check board size
        self.assertEqual(self.board.size, 8)
        
        # Check initial pieces
        self.assertEqual(self.board.get_piece(3, 3), 'W')
        self.assertEqual(self.board.get_piece(3, 4), 'B')
        self.assertEqual(self.board.get_piece(4, 3), 'B')
        self.assertEqual(self.board.get_piece(4, 4), 'W')
        
        # Check initial score
        black, white = self.board.get_score()
        self.assertEqual(black, 2)
        self.assertEqual(white, 2)
    
    def test_valid_position(self):
        """Test position validation."""
        self.assertTrue(self.board.is_valid_position(0, 0))
        self.assertTrue(self.board.is_valid_position(7, 7))
        self.assertFalse(self.board.is_valid_position(-1, 0))
        self.assertFalse(self.board.is_valid_position(0, 8))
    
    def test_set_and_get_piece(self):
        """Test setting and getting pieces."""
        self.board.set_piece(0, 0, 'B')
        self.assertEqual(self.board.get_piece(0, 0), 'B')
        
        self.board.set_piece(7, 7, 'W')
        self.assertEqual(self.board.get_piece(7, 7), 'W')
    
    def test_count_pieces(self):
        """Test piece counting."""
        self.board.set_piece(0, 0, 'B')
        self.board.set_piece(0, 1, 'B')
        black_count = self.board.count_pieces('B')
        self.assertGreaterEqual(black_count, 4)  # 2 initial + 2 added


class TestOthelloGame(unittest.TestCase):
    """Test the OthelloGame class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = OthelloGame()
    
    def test_initial_valid_moves(self):
        """Test that initial valid moves are correct for Black."""
        valid_moves = self.game.get_valid_moves('B')
        # Black should have 4 valid opening moves
        self.assertEqual(len(valid_moves), 4)
        expected_moves = [(2, 3), (3, 2), (4, 5), (5, 4)]
        for move in expected_moves:
            self.assertIn(move, valid_moves)
    
    def test_valid_move_detection(self):
        """Test valid move detection."""
        # These should be valid opening moves for Black
        self.assertTrue(self.game.is_valid_move(2, 3, 'B'))
        self.assertTrue(self.game.is_valid_move(3, 2, 'B'))
        
        # This should be invalid (no pieces to flip)
        self.assertFalse(self.game.is_valid_move(0, 0, 'B'))
    
    def test_make_move(self):
        """Test making a move."""
        # Make a valid move
        result = self.game.make_move(2, 3, 'B')
        self.assertTrue(result)
        
        # Check that piece was placed
        self.assertEqual(self.game.board.get_piece(2, 3), 'B')
        
        # Check that opponent piece was flipped
        self.assertEqual(self.game.board.get_piece(3, 3), 'B')
    
    def test_invalid_move(self):
        """Test that invalid moves are rejected."""
        # Try to place on an occupied square
        result = self.game.make_move(3, 3, 'B')
        self.assertFalse(result)
        
        # Try to place where no flips occur
        result = self.game.make_move(0, 0, 'B')
        self.assertFalse(result)
    
    def test_get_opponent(self):
        """Test opponent determination."""
        self.assertEqual(self.game.get_opponent('B'), 'W')
        self.assertEqual(self.game.get_opponent('W'), 'B')
    
    def test_game_not_over_initially(self):
        """Test that game is not over at start."""
        self.assertFalse(self.game.is_game_over())
    
    def test_winner_determination(self):
        """Test winner determination."""
        # In initial state, it's a tie
        winner = self.game.get_winner()
        self.assertIsNone(winner)
        
        # Add more black pieces
        self.game.board.set_piece(0, 0, 'B')
        self.game.board.set_piece(0, 1, 'B')
        self.game.board.set_piece(0, 2, 'B')
        
        winner = self.game.get_winner()
        self.assertEqual(winner, 'B')


class TestAIPlayer(unittest.TestCase):
    """Test the AIPlayer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = OthelloGame()
        self.ai = AIPlayer('B', difficulty=2)
    
    def test_ai_initialization(self):
        """Test AI player initialization."""
        self.assertEqual(self.ai.player, 'B')
        self.assertEqual(self.ai.difficulty, 2)
    
    def test_ai_gets_valid_move(self):
        """Test that AI returns a valid move."""
        move = self.ai.get_move(self.game)
        self.assertIsNotNone(move)
        
        # Check that the move is valid
        valid_moves = self.game.get_valid_moves('B')
        self.assertIn(move, valid_moves)
    
    def test_ai_returns_none_when_no_moves(self):
        """Test that AI returns None when no valid moves."""
        # Create a board state where Black has no moves
        # Fill the board mostly with White
        for i in range(8):
            for j in range(8):
                self.game.board.set_piece(i, j, 'W')
        
        move = self.ai.get_move(self.game)
        self.assertIsNone(move)
    
    def test_ai_can_play_full_game(self):
        """Test that AI can play through a full game."""
        game = OthelloGame()
        ai_black = AIPlayer('B', difficulty=1)
        ai_white = AIPlayer('W', difficulty=1)
        
        current_player = 'B'
        moves_made = 0
        max_moves = 60  # Prevent infinite loop
        
        while not game.is_game_over() and moves_made < max_moves:
            ai = ai_black if current_player == 'B' else ai_white
            move = ai.get_move(game)
            
            if move:
                game.make_move(move[0], move[1], current_player)
                moves_made += 1
            
            current_player = game.get_opponent(current_player)
        
        # Game should complete
        self.assertGreater(moves_made, 0)


class TestGameIntegration(unittest.TestCase):
    """Integration tests for complete game scenarios."""
    
    def test_complete_game_sequence(self):
        """Test a complete game sequence."""
        game = OthelloGame()
        
        # Black's turn
        valid_moves = game.get_valid_moves('B')
        self.assertGreater(len(valid_moves), 0)
        
        # Make first move
        first_move = valid_moves[0]
        result = game.make_move(first_move[0], first_move[1], 'B')
        self.assertTrue(result)
        
        # White's turn
        valid_moves = game.get_valid_moves('W')
        self.assertGreater(len(valid_moves), 0)
        
        # Make second move
        second_move = valid_moves[0]
        result = game.make_move(second_move[0], second_move[1], 'W')
        self.assertTrue(result)
        
        # Game should not be over yet
        self.assertFalse(game.is_game_over())
    
    def test_score_tracking(self):
        """Test that scores are tracked correctly."""
        game = OthelloGame()
        initial_black, initial_white = game.board.get_score()
        
        # Make a move
        game.make_move(2, 3, 'B')
        
        new_black, new_white = game.board.get_score()
        
        # Black should have more pieces, white should have fewer
        self.assertGreater(new_black, initial_black)
        self.assertLess(new_white, initial_white)


if __name__ == '__main__':
    unittest.main()
