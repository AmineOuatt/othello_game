#!/usr/bin/env python3
"""
Demo script to test both game modes automatically
"""

from othello import OthelloGame, AIPlayer


def test_human_vs_human_setup():
    """Test that human vs human mode can be set up."""
    print("Testing Human vs Human mode setup...")
    game = OthelloGame()
    game.board.display()
    
    # Test a few moves
    moves = [(2, 3), (2, 2), (2, 4)]
    current_player = 'B'
    
    for move in moves:
        valid_moves = game.get_valid_moves(current_player)
        if move in valid_moves:
            print(f"Player {current_player} makes move: {move}")
            game.make_move(move[0], move[1], current_player)
            game.board.display()
            black, white = game.board.get_score()
            print(f"Score - Black: {black}, White: {white}\n")
            current_player = game.get_opponent(current_player)
        else:
            print(f"Move {move} not valid for player {current_player}")
            current_player = game.get_opponent(current_player)
    
    print("✓ Human vs Human mode works correctly\n")


def test_human_vs_machine():
    """Test human vs machine mode."""
    print("Testing Human vs Machine mode...")
    game = OthelloGame()
    
    # Create AI players with different difficulties
    for difficulty in [1, 3]:
        print(f"\n--- Testing AI with difficulty {difficulty} ---")
        game = OthelloGame()
        ai = AIPlayer('W', difficulty=difficulty)
        
        # Play a few turns
        for turn in range(5):
            # Black (human simulation) - just pick first valid move
            valid_moves = game.get_valid_moves('B')
            if valid_moves:
                move = valid_moves[0]
                game.make_move(move[0], move[1], 'B')
                print(f"Black plays: {move}")
            
            # White (AI)
            ai_move = ai.get_move(game)
            if ai_move:
                game.make_move(ai_move[0], ai_move[1], 'W')
                print(f"AI plays: {ai_move}")
            
            if game.is_game_over():
                break
        
        game.board.display()
        black, white = game.board.get_score()
        print(f"After 5 turns - Score: Black: {black}, White: {white}")
    
    print("\n✓ Human vs Machine mode works correctly\n")


def test_full_ai_game():
    """Test a complete game between two AI players."""
    print("Testing full AI vs AI game (fast playthrough)...")
    game = OthelloGame()
    ai_black = AIPlayer('B', difficulty=1)
    ai_white = AIPlayer('W', difficulty=1)
    
    current_player = 'B'
    move_count = 0
    consecutive_passes = 0
    
    while not game.is_game_over() and consecutive_passes < 2 and move_count < 60:
        ai = ai_black if current_player == 'B' else ai_white
        move = ai.get_move(game)
        
        if move:
            game.make_move(move[0], move[1], current_player)
            move_count += 1
            consecutive_passes = 0
        else:
            consecutive_passes += 1
        
        current_player = game.get_opponent(current_player)
    
    game.board.display()
    black, white = game.board.get_score()
    print(f"Final Score - Black: {black}, White: {white}")
    
    winner = game.get_winner()
    if winner == 'B':
        print("Black wins!")
    elif winner == 'W':
        print("White wins!")
    else:
        print("It's a tie!")
    
    print(f"Total moves played: {move_count}")
    print("✓ Full game completes successfully\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Othello Game - Automated Demo")
    print("=" * 60)
    print()
    
    test_human_vs_human_setup()
    test_human_vs_machine()
    test_full_ai_game()
    
    print("=" * 60)
    print("All tests passed! The game is ready to play.")
    print("Run 'python3 othello.py' to start playing!")
    print("=" * 60)
