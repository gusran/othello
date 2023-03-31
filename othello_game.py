class OthelloGame:
    def __init__(self, board_size=8):
        self.WHITE = 'w'
        self.BLACK = 'b'
        self.board_size = board_size
        self.board = [['-' for _ in range(board_size)] for _ in range(board_size)]
        self.board[board_size//2-1][board_size//2-1] = 'w'
        self.board[board_size//2][board_size//2] = 'w'
        self.board[board_size//2-1][board_size//2] = 'b'
        self.board[board_size//2][board_size//2-1] = 'b'

        self.players = ['w', 'b']

    def make_move(self, row, col, board, player):
        if self.is_valid_move(row, col, player):
            board[row][col] = player
            for r, c in self.get_flipped_pieces(row, col, player):
                board[r][c] = player
        else:
            raise Exception(f"Move ({row}, {col}) is not valid for player {player}")

    def is_valid_move(self, row, col, player):
        if self.board[row][col] != '-' and self.within_board_limits(col, row):
            return False
        for r, c in [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]:
            r_pos, c_pos = row + r, col + c
            if self.within_board_limits(c_pos, r_pos) and \
                    self.board[r_pos][c_pos] == self.players[(self.players.index(player) + 1) % 2]:
                while self.within_board_limits(c_pos, r_pos):
                    if self.board[r_pos][c_pos] == '-':
                        break
                    elif self.board[r_pos][c_pos] == player:
                        return True
                    r_pos += r
                    c_pos += c
        return False

    def within_board_limits(self, c_pos, r_pos):
        return 0 <= r_pos < self.board_size and 0 <= c_pos < self.board_size

    def get_flipped_pieces(self, row, col, player):
        flipped_pieces = []
        for r, c in [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]:
            r_pos, c_pos = row + r, col + c
            to_flip = []
            while self.within_board_limits(c_pos, r_pos):
                if self.board[r_pos][c_pos] == '-':
                    break
                elif self.board[r_pos][c_pos] == player:
                    flipped_pieces.extend(to_flip)
                    break
                else:
                    to_flip.append((r_pos, c_pos))
                r_pos += r
                c_pos += c
        return flipped_pieces

    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def no_valid_moves(self, player):
        if len(self.get_valid_moves(player)) > 0:
            return False
        return True

    def print_board(self):
        print('   ', end='')
        for col in range(self.board_size):
            print(chr(65 + col) + ' ', end='')
        print()
        print('  +' + '--'*self.board_size + '+')

        for row in range(self.board_size):
            print(f'{row+1} |', end='')
            for col in range(self.board_size):
                piece = self.board[row][col]
                if piece == 'w':
                    print('\u25cf ', end='')
                elif piece == 'b':
                    print('\u25cb ', end='')
                else:
                    print('- ', end='')
            print(f'| {row+1}')

        print('  +' + '--'*self.board_size + '+')
        print('   ', end='')
        for col in range(self.board_size):
            print(chr(65 + col) + ' ', end='')
        print()

    def get_other_player(self, player):
        return self.players[(self.players.index(player) + 1) % 2]

    def get_winner(self):
        white_count = 0
        black_count = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 'w':
                    white_count += 1
                elif self.board[row][col] == 'b':
                    black_count += 1

        if white_count > black_count:
            return 'white'
        elif black_count > white_count:
            return 'black'
        else:
            return 'tie'

