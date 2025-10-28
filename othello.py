import tkinter as tk
from tkinter import messagebox, simpledialog
import copy

#  GAME CONSTANTS ===============================

ROWS, COLS = 8, 8
CELL_SIZE = 65
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1),
              (-1, -1), (-1, 1), (1, -1), (1, 1)]
EMPTY = "."
BLACK = "B"
WHITE = "W"

# GAME LOGIC FUNCTIONS ===============================

def is_valid_move(row, col, player, board):
    """Check if placing a piece here is valid according to Othello rules."""
    if board[row][col] != EMPTY:
        return False

    opponent = WHITE if player == BLACK else BLACK

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        has_opponent = False

        # move along the direction while opponent pieces are found
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == opponent:
            has_opponent = True
            r += dr
            c += dc

        # if line ends with player's piece, it's a valid move
        if has_opponent and 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            return True
    return False

def get_valid_moves(player, board):
    moves = []
    for r in range(ROWS):
        for c in range(COLS):
            if is_valid_move(r, c, player, board):
                moves.append((r, c))
    return moves

def make_move(row, col, player, board):
    opponent = WHITE if player == BLACK else BLACK
    board[row][col] = player

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        to_flip = []

        # collect all opponent pieces in this direction
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == opponent:
            to_flip.append((r, c))
            r += dr
            c += dc

        # flip if line ends with player's own piece
        if to_flip and 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            for rr, cc in to_flip:
                board[rr][cc] = player


def count_pieces(board):
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)
    return black_count, white_count


def check_game_over(board, root):
    black_moves = get_valid_moves(BLACK, board)
    white_moves = get_valid_moves(WHITE, board)

    if not black_moves and not white_moves:
        black_count, white_count = count_pieces(board)

        if black_count > white_count:
            result = "Black wins!"
        elif white_count > black_count:
            result = "White wins!"
        else:
            result = "It's a draw!"

        # Update the board before showing result
        root.update()

        # Show winner message
        messagebox.showinfo("Game Over", result)

        # Close game window and return to menu
        root.destroy()
        open_main_menu()

#  DRAWING FUNCTIONS ======================================================

def draw_board(canvas, current_player, board):
    possible_moves = get_valid_moves(current_player, board)
    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            if (row, col) in possible_moves:
                color = "lightgreen"
            else:
                color = "darkgreen"

            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)

    draw_pieces(canvas, board)


def draw_piece(canvas, row, col, color):
    x = col * CELL_SIZE + CELL_SIZE / 2
    y = row * CELL_SIZE + CELL_SIZE / 2
    r = CELL_SIZE / 2 - 5
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black", tags="piece")


def draw_pieces(canvas, board):
    canvas.delete("piece")
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == BLACK:
                draw_piece(canvas, row, col, "black")
            elif board[row][col] == WHITE:
                draw_piece(canvas, row, col, "white")



# minimax AI functions ===============================

def evaluate(board):
    """Simple evaluation: difference between black and white pieces"""
    black, white = count_pieces(board)
    return white - black

def simulate_move(board,move,player):
    new_board = copy.deepcopy(board)
    make_move(move[0],move[1],player,new_board)
    return new_board

# we know that white(ai) is maximizing player and black (human) is minimizing player
# create a max function that calls minimax recursively

def max_value(board, depth):
    if depth == 0 or not (get_valid_moves(BLACK, board) or get_valid_moves(WHITE, board)):
        return evaluate(board)
    best_score = float('-inf')
    for move in get_valid_moves(WHITE, board):
        new_board = simulate_move(board, move, WHITE)
        eval = min_value(new_board, depth - 1)
        best_score = max(best_score, eval)
    return best_score

# min function that calls minimax recursively

def min_value(board, depth):
    if depth == 0 or not (get_valid_moves(BLACK, board) or get_valid_moves(WHITE, board)):
        return evaluate(board)
    best_score = float('inf')
    for move in get_valid_moves(BLACK, board):
        new_board = simulate_move(board, move, BLACK)
        eval = max_value(new_board, depth - 1)
        best_score = min(best_score, eval)
    return best_score

def get_ai_move(board, depth):
    """Return the best move for the AI (white) using minimax search."""
    best_move = None
    best_score = float('-inf')

    moves = get_valid_moves(WHITE, board)
    if not moves:
        return None  # no move possible

    for move in moves:
        # simulate this move for the AI
        new_board = simulate_move(board, move, WHITE)
        
        # evaluate how the opponent would respond
        score = min_value(new_board, depth - 1)

        # choose the move with the highest evaluation
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def highlight_ai_move(canvas, row, col):
   
    """Draw a colored border around the AI's chosen move"""
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    
    # Draw a thick red border around the cell
    canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=4, tags="ai_highlight")


# human vs machine minimax function ===============================

def human_vs_machine_minimax():
    depth = simpledialog.askinteger("AI Depth", "Enter AI search depth (e.g., 1–6):", minvalue=1, maxvalue=6)
    
    game_window = tk.Tk()
    game_window.title("Othello - Human vs Machine")
    board = []
    for _ in range(ROWS):
        data_row = []
        for _ in range(COLS):
            data_row.append(EMPTY)
        board.append(data_row)
    board[3][3], board[3][4] = WHITE, BLACK
    board[4][3], board[4][4] = BLACK, WHITE
    current_player = BLACK

    canvas = tk.Canvas(game_window, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
    canvas.pack()

    def click_event(event):
        nonlocal current_player

        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        # Ignore clicks outside board
        if not (0 <= row < ROWS and 0 <= col < COLS):
            return

        # --- HUMAN TURN (Black) ---
        if current_player == BLACK:

            valid_moves = get_valid_moves(BLACK, board)

            #  Case 1: Human has no valid moves
            if not valid_moves:
                messagebox.showinfo("Skip", "Black has no valid moves! AI plays.")
                current_player = WHITE
            else:
                #  Case 2: Human clicked a valid move
                if (row, col) in valid_moves:
                    make_move(row, col, BLACK, board)
                    current_player = WHITE
                else:
                    #  Case 3: Human clicked invalid cell
                    messagebox.showwarning("Invalid Move", "That move is not valid!")
                    return

            draw_board(canvas, current_player, board)
            game_window.update()

        # --- AI TURN (White) ---
        if current_player == WHITE:

            valid_moves = get_valid_moves(WHITE, board)

            #  Case 1: AI has no valid moves
            if not valid_moves:
                if get_valid_moves(BLACK, board):
                    messagebox.showinfo("Skip", "AI has no valid moves! Your turn.")
                    current_player = BLACK
                else:
                    check_game_over(board, game_window)
                    return
            else:
                #  Case 2: AI chooses best move
                ai_move = get_ai_move(board, depth)
                if ai_move:
                    make_move(ai_move[0], ai_move[1], WHITE, board)
                    
                    current_player = BLACK

            draw_board(canvas, current_player, board)
            highlight_ai_move(canvas, ai_move[0], ai_move[1])
            game_window.update()

            #  Case 3: Check if game is over
            if not get_valid_moves(BLACK, board) and not get_valid_moves(WHITE, board):
                check_game_over(board, game_window)


    canvas.bind("<Button-1>", click_event)
    draw_board(canvas, current_player, board)


#  HUMAN VS HUMAN GAME ================================

def human_vs_human():
    # Create a new window for the game
    game_window = tk.Tk()
    game_window.title("Othello - Human vs Human")
    
    # Initialize board
    board =[]
    for _ in range(ROWS):
        data_row = []
        for _ in range(COLS):
            data_row.append(EMPTY)
        board.append(data_row)

    board[3][3], board[3][4] = WHITE, BLACK
    board[4][3], board[4][4] = BLACK, WHITE
    current_player = BLACK

    canvas = tk.Canvas(game_window, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
    canvas.pack()

    def click_event(event):
        nonlocal current_player
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            if is_valid_move(row, col, current_player, board):
                make_move(row, col, current_player, board)
                current_player = WHITE if current_player == BLACK else BLACK

                if not get_valid_moves(current_player, board):
                    opponent = WHITE if current_player == BLACK else BLACK
                    if get_valid_moves(opponent, board):
                        messagebox.showinfo("Skip", f"{'White' if current_player == WHITE else 'Black'} has no valid moves! Turn skipped.")
                        current_player = opponent
                    else:
                        check_game_over(board, game_window)

        draw_board(canvas, current_player, board)

    canvas.bind("<Button-1>", click_event)
    draw_board(canvas, current_player, board)


def start_human_vs_human(menu):
    menu.destroy()
    human_vs_human()
def start_human_vs_machine(menu):
    menu.destroy()
    human_vs_machine_minimax()


#  MAIN MENU WINDOW ===============================

def open_main_menu():
    menu = tk.Tk()
    menu.title("Othello Main Menu")
    menu.geometry("400x300")

    tk.Label(menu, text="Othello Game", font=("Arial", 20, "bold")).pack(pady=30)

    tk.Button(menu, text="Human vs Human", width=20, height=2,
          command=lambda: start_human_vs_human(menu)).pack(pady=10)


    tk.Button(menu, text="Human vs Machine", width=20, height=2,
              command=lambda: start_human_vs_machine(menu)).pack(pady=10)

    tk.Button(menu, text="Quit", width=20, height=2, command=menu.destroy).pack(pady=30)

    menu.mainloop()



#  START PROGRAM ===============================

open_main_menu()