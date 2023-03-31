from othello_game import OthelloGame
from othello_ai import OthelloAI

# Initialize the game with a 4x4 board and the OthelloAI as the black player
game = OthelloGame(board_size=4)
ai = OthelloAI()

player = 'w'

# Play the game until it's over
while not game.no_valid_moves(player):
    print('Current Board:')
    game.print_board()

    if player == 'w':
        # Human player makes a move
        row = int(input('Enter row: '))
        col = int(input('Enter column: '))
        while not game.is_valid_move(row - 1, col - 1, player):
            row = int(input('Enter row: '))
            col = int(input('Enter column: '))
        game.make_move(row - 1, col - 1, game.board, player)
    else:
        # AI player makes a move
        row, col = ai.choose_move(game)
        print(f"AI move ({row}, {col})")
        game.make_move(row, col, game.board, player)

    player = game.get_other_player(player)

# Print the final board and the winner
print('Final Board:')
game.print_board()
print('Winner:', game.get_winner())
