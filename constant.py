import pygame

HEIGHT, WIDTH = 700, 1000
SQUARE_SIZE = 20
ROWS, COLS = HEIGHT // SQUARE_SIZE, WIDTH // SQUARE_SIZE
ALGO_CHOICE_HEIGHT = 50
TOTAL_HEIGHT = HEIGHT + ALGO_CHOICE_HEIGHT
NUM_ALGO = 4
FONT_SIZE = 40
BOX_WIDTH = WIDTH // NUM_ALGO

# RGB colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128,128,128)
ORANGE = (255,165,0)
PURPLE = (128,0,128)

# display text in center
pygame.font.init()
def draw_center_text(text, x, y, colour, win):
    font = pygame.font.SysFont(None, FONT_SIZE)
    text = font.render(text, True, colour)
    text_rect = text.get_rect(center=(x, y))
    win.blit(text, text_rect)