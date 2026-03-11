#!/usr/bin/env python3
"""Connect Four — minimax AI with alpha-beta pruning."""
import sys, random

ROWS, COLS = 6, 7

def new_board(): return [[' ']*COLS for _ in range(ROWS)]

def drop(board, col, piece):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = piece; return r
    return -1

def undo(board, row, col): board[row][col] = ' '

def check_win(board, piece):
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
                if all(0<=r+i*dr<ROWS and 0<=c+i*dc<COLS and board[r+i*dr][c+i*dc]==piece for i in range(4)):
                    return True
    return False

def evaluate(board):
    if check_win(board, 'X'): return 1000
    if check_win(board, 'O'): return -1000
    score = 0
    for r in range(ROWS):
        for c in range(COLS-3):
            window = [board[r][c+i] for i in range(4)]
            score += window.count('X')**2 - window.count('O')**2
    return score

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or check_win(board, 'X') or check_win(board, 'O'):
        return evaluate(board), -1
    valid = [c for c in range(COLS) if board[0][c] == ' ']
    if not valid: return 0, -1
    best_col = random.choice(valid)
    if maximizing:
        best = -9999
        for c in valid:
            r = drop(board, c, 'X')
            score, _ = minimax(board, depth-1, alpha, beta, False)
            undo(board, r, c)
            if score > best: best = score; best_col = c
            alpha = max(alpha, best)
            if alpha >= beta: break
        return best, best_col
    else:
        best = 9999
        for c in valid:
            r = drop(board, c, 'O')
            score, _ = minimax(board, depth-1, alpha, beta, True)
            undo(board, r, c)
            if score < best: best = score; best_col = c
            beta = min(beta, best)
            if alpha >= beta: break
        return best, best_col

def render(board):
    print("  " + " ".join(str(i) for i in range(COLS)))
    for row in board:
        print("  " + "|".join(row))
    print("  " + "-" * (COLS*2-1))

if __name__ == "__main__":
    board = new_board()
    print("Connect Four: You=O, AI=X")
    render(board)
    while True:
        try: col = int(input("Column (0-6): "))
        except (ValueError, EOFError): col = random.choice([c for c in range(COLS) if board[0][c]==' '])
        if 0 <= col < COLS and board[0][col] == ' ':
            drop(board, col, 'O'); render(board)
            if check_win(board, 'O'): print("You win!"); break
        _, ai_col = minimax(board, 5, -9999, 9999, True)
        drop(board, ai_col, 'X'); print(f"AI plays column {ai_col}"); render(board)
        if check_win(board, 'X'): print("AI wins!"); break
        if all(board[0][c] != ' ' for c in range(COLS)): print("Draw!"); break
