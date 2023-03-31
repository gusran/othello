import pygame
from pygame.locals import *

from othello_game import OthelloGame
from othello_ai import OthelloAI

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)


class OthelloGui:
    def __init__(self, game: OthelloGame, ai: OthelloAI):
        pygame.init()
        self.game = game
        self.ai = ai

        self.font = pygame.font.SysFont("Arial", 30)
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Othello")
        self.clock = pygame.time.Clock()

        self.black_button = pygame.Surface((50, 50))
        self.black_button.fill(BLACK)
        self.white_button = pygame.Surface((50, 50))
        self.white_button.fill(WHITE)
        self.empty_button = pygame.Surface((50, 50))
        self.empty_button.fill(GRAY)

        self.message = ""
        self.game_over = False
        self.winner = None

    def draw_board(self):
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                color = self.empty_button
                if self.game.board[i][j] == self.game.BLACK:
                    color = self.black_button
                elif self.game.board[i][j] == self.game.WHITE:
                    color = self.white_button
                rect = pygame.Rect(j * 50 + 50, i * 50 + 50, 50, 50)
                pygame.draw.rect(self.screen, BLUE, rect, 2)
                self.screen.blit(color, (j * 50 + 50, i * 50 + 50))

    def draw_message(self):
        if self.game_over:
            text = self.font.render(f"Game over! {self.winner} wins!", True, BLACK)
            self.screen.blit(text, (50, 10))
            text = self.font.render("Press r to restart, q to quit", True, BLACK)
            self.screen.blit(text, (50, 350))
        else:
            text = self.font.render(self.message, True, BLACK)
            self.screen.blit(text, (50, 10))

    def handle_user_move(self, row, col):
        if self.game.is_valid_move(self.game.WHITE, row, col):
            self.game.make_move(self.game.WHITE, row, col)
            self.message = ""
            self.ai_move()
        else:
            self.message = "Invalid move!"

    def ai_move(self):
        move = self.ai.choose_move(self.game)
        if move is None:
            self.message = "AI passed"
        else:
            self.game.place(self.game.BLACK, move[0], move[1])
            self.message = ""

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN and not self.game_over:
                pos = pygame.mouse.get_pos()
                col = (pos[0] - 50) // 50
                row = (pos[1] - 50) // 50
                if 0 <= col < self.game.size and 0 <= row < self.game.size:
                    self.handle_user_move(row, col)
