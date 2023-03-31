from copy import deepcopy
from random import choice

class OthelloAI:
    def __init__(self, color='b', max_depth=5):
        self.color = color
        self.max_depth = max_depth

    def evaluate_board(self, game, board):
        # Count the number of pieces on the board for each color
        score = {}
        for row in board:
            for piece in row:
                if piece in score:
                    score[piece] += 1
                else:
                    score[piece] = 1

        # If the AI is playing as black, subtract the number of white pieces from the number of black pieces
        if self.color == 'b':
            return score.get('b', 0) - score.get('w', 0)
        else:
            return score.get('w', 0) - score.get('b', 0)

    def get_valid_moves(self, game, board, player):
        valid_moves = []
        for row in range(game.board_size):
            for col in range(game.board_size):
                if board[row][col] == '-':
                    move = (row, col)
                    if game.is_valid_move(row, col, player):
                        valid_moves.append(move)
        return valid_moves

    def minimax(self, game, board, player, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.no_valid_moves(player):
            return None, self.evaluate_board(game, board)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_valid_moves(game, board, player):
                new_board = deepcopy(board)
                game.make_move(move[0], move[1], new_board, player)
                _, eval = self.minimax(game, new_board, game.get_other_player(player), depth-1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval

        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_valid_moves(game, board, game.get_other_player(player)):
                new_board = deepcopy(board)
                game.make_move(move[0], move[1], new_board, game.get_other_player(player))
                _, eval = self.minimax(game, new_board, game.get_other_player(player), depth-1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def choose_move(self, game):
        board = deepcopy(game.board)
        move, _ = self.minimax(game, board, self.color, self.max_depth, float('-inf'), float('inf'), self.color == 'b')
        if move is None:
            return choice(self.get_valid_moves(game, board, self.color))
        else:
            return move
