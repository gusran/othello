import pygame
from othello_game import OthelloGame
from othello_ai import OthelloAI

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Define the dimensions of each cell on the board
CELL_WIDTH = 80
CELL_HEIGHT = 80

BOARD_SIZE = 8

# Define the dimensions of the window
WINDOW_WIDTH = BOARD_SIZE * CELL_WIDTH
WINDOW_HEIGHT = BOARD_SIZE * CELL_HEIGHT

# Initialize pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Othello")



# Create the game and AI objects
game = OthelloGame(board_size=BOARD_SIZE)
ai = OthelloAI()


# Define the function to draw the board
def draw_board():
    for board_row in range(game.board_size):
        for board_col in range(game.board_size):
            rect = pygame.Rect(board_col * CELL_WIDTH, board_row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            if game.board[board_row][board_col] == 'b':
                pygame.draw.rect(screen, BLACK, rect, 0, border_radius=1)
            elif game.board[board_row][board_col] == 'w':
                pygame.draw.rect(screen, WHITE, rect, 0, border_radius=1)
                pygame.draw.rect(screen, BLACK, rect, 1, border_radius=1)
            else:
                pygame.draw.rect(screen, GRAY, rect, 0, border_radius=1)
                pygame.draw.rect(screen, BLACK, rect, 1, border_radius=1)


# Define the function to handle user input
def handle_user_input(user_row, user_col):
    if game.is_valid_move(user_row, user_col, 'w'):
        game.make_move(user_row, user_col, game.board, 'w')
        if not game.no_valid_moves('b'):
            ai_row, ai_col = ai.choose_move(game)
            game.make_move(ai_row, ai_col, game.board, 'b')


# Define the function to draw the game over screen
def draw_game_over():
    draw_board()
    font = pygame.font.Font(None, 30)
    text = font.render("Game Over!", True, GREEN)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    if game.get_winner() == 'blck':
        winner_text = font.render("Black Wins!", True, GREEN)
    elif game.get_winner() == 'white':
        winner_text = font.render("White Wins!", True, GREEN)
    else:
        winner_text = font.render("Tie Game!", True, GREEN)
    winner_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    screen.blit(winner_text, winner_rect)
    restart_text = font.render("Press space to restart or q to quit.", True, GREEN)
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
    screen.blit(restart_text, restart_rect)
    pygame.display.update()


# Set up the game loop
running = True
game_over = False
clock = pygame.time.Clock()
while running:
    clock.tick(60)

    if game.no_valid_moves('w'):
        if not game.no_valid_moves('b'):
            ai_row, ai_col = ai.choose_move(game)
            game.make_move(ai_row, ai_col, game.board, 'b')

    for event in pygame.event.get():
        print(f"Got event {event}")
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pos = pygame.mouse.get_pos()
            col = pos[0] // CELL_WIDTH
            row = pos[1] // CELL_HEIGHT
            print(f"Handle mouse down {row} {col}")
            handle_user_input(row, col)
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                game = OthelloGame(board_size = BOARD_SIZE)
                game_over = False
            elif event.key == pygame.K_q:
                running = False

    # Draw the board
    if game_over:
        draw_game_over()
    else:
        screen.fill(GRAY)
        draw_board()

    pygame.display.update()

    # Check if the game is over
    if (game.no_valid_moves('w') and game.no_valid_moves('b')) and not game_over:
        game_over = True
