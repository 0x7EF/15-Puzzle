import pygame
import random
import sys, time

pygame.init()
pygame.font.init()

########################################################################

WIDTH = HEIGHT = 500
GRID_WIDTH = GRID_HEIGHT = 300
CELL_WIDTH = CELL_HEIGHT = GRID_WIDTH // 4

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic 15 PUZZLE ")
icon = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.display.set_icon(icon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (210, 180, 140)

DIGITS_FONT = pygame.font.SysFont("segoeui", 32)
WIN_FONT = pygame.font.SysFont("comicsans", 84)
SCORE_FONT = pygame.font.SysFont("comicsans", 24)

FPS = 32

########################################################################

GRID = pygame.Rect((WIDTH - GRID_WIDTH)//2, (HEIGHT - GRID_HEIGHT)//2, GRID_WIDTH, GRID_HEIGHT) 

UPPER_BORDER = pygame.Rect((WIDTH - GRID_WIDTH)//2 - 15, (HEIGHT - GRID_HEIGHT)//2 - 15, GRID_WIDTH + 30, 15)
RIGHT_BORDER = pygame.Rect((WIDTH + GRID_WIDTH)//2, (HEIGHT - GRID_HEIGHT)//2, 15, GRID_WIDTH + 15)
DOWN_BORDER = pygame.Rect((WIDTH - GRID_WIDTH)//2 - 15, (HEIGHT + GRID_HEIGHT)//2, GRID_WIDTH + 15, 15)
LEFT_BORDER = pygame.Rect((WIDTH - GRID_WIDTH)//2 - 15, (HEIGHT - GRID_HEIGHT)//2, 15, GRID_HEIGHT)

########################################################################

def generate_solvable_15_puzzle():
    while True:
        puzzle = list(range(16))  
        random.shuffle(puzzle)  

        inversions = 0
        for i in range(15):
            for j in range(i + 1, 16):
                if (puzzle[i] > 1) and (puzzle[j] != 0) and (puzzle[i] > puzzle[j]):
                    inversions += 1

        if ( (inversions % 2) ^ ((4 - puzzle.index(0)//4) % 2) ):
            break  

    return puzzle

########################################################################

def draw_window(foo, elapsed_time):
    WIN.fill(BROWN)

    pygame.draw.rect(WIN, BLACK, UPPER_BORDER)
    pygame.draw.rect(WIN, BLACK, RIGHT_BORDER)
    pygame.draw.rect(WIN, BLACK, DOWN_BORDER)
    pygame.draw.rect(WIN, BLACK, LEFT_BORDER)

    pygame.draw.rect(WIN, WHITE, GRID)

    if elapsed_time is not None:
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = SCORE_FONT.render(f"Time  {minutes:02}:{seconds:02}", 1, BLACK)
        WIN.blit(timer_text, (WIDTH - timer_text.get_width() - 20, 10))  # Place the timer in the same location as Moves
    else:
        timer_text = SCORE_FONT.render("Time  00:00", 1, BLACK)
        WIN.blit(timer_text, (WIDTH - timer_text.get_width() - 20, 10))  # Place the timer in the same location as Moves

    reset = SCORE_FONT.render(" ! Click  R  To RESET ! ", 1, GOLD)
    WIN.blit(reset, (8, 10))

    for i in range(16):
        if (foo[i] != 0):
            digText = DIGITS_FONT.render(str(foo[i]), 1, BLACK)
            WIN.blit(digText, (((WIDTH - GRID_WIDTH)//2 + ((i%4) * CELL_WIDTH) + (CELL_WIDTH//2 - digText.get_width()//2)), ((HEIGHT - GRID_HEIGHT)//2 + ((i//4) * CELL_HEIGHT) + (CELL_HEIGHT//2 - digText.get_height()//2))))
        
        else:
            pygame.draw.rect(WIN, LIGHT_BROWN, pygame.Rect((WIDTH - GRID_WIDTH)//2 + ((i%4) * CELL_WIDTH), (HEIGHT - GRID_HEIGHT)//2 + ((i//4) * CELL_HEIGHT), CELL_WIDTH, CELL_HEIGHT))

    for i in range(1, 4):
        HORIZONTAL_LINE = pygame.Rect((WIDTH - GRID_WIDTH)//2, (HEIGHT - GRID_HEIGHT)//2 + (i * CELL_HEIGHT) - 2, GRID_WIDTH, 4)
        VERTICAL_LINE = pygame.Rect((WIDTH - GRID_WIDTH)//2 + (i * CELL_WIDTH) - 2, (HEIGHT - GRID_HEIGHT)//2, 4, GRID_HEIGHT)

        pygame.draw.rect(WIN, BLACK, HORIZONTAL_LINE)
        pygame.draw.rect(WIN, BLACK, VERTICAL_LINE)

    pygame.display.update()

def Handle_Win(elapsed_time):
    WIN.fill(BROWN)
    winText = WIN_FONT.render("You win !", 1, BLACK)
    timeText = SCORE_FONT.render(f"Time  {elapsed_time // 60:02}:{elapsed_time % 60:02}", 1, BLACK)
    
    # Calculate the position to center the text
    winText_x = (WIDTH - winText.get_width()) // 2
    winText_y = (HEIGHT - winText.get_height() - timeText.get_height()) // 2
    timeText_x = (WIDTH - timeText.get_width()) // 2
    timeText_y = winText_y + winText.get_height()

    WIN.blit(winText, (winText_x, winText_y))
    WIN.blit(timeText, (timeText_x, timeText_y))
    pygame.display.update()

    delay_start_time = pygame.time.get_ticks()
    delay_duration = 4000  # Delay for 4000 milliseconds

    while pygame.time.get_ticks() - delay_start_time < delay_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


########################################################################

def main():

    clock = pygame.time.Clock()

    arr = generate_solvable_15_puzzle()
    start_time = None  # Initialize the start time

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                j = arr.index(0)

                if event.key == pygame.K_r:
                    arr = generate_solvable_15_puzzle()
                    start_time = None  # Reset the timer when the game is reset

                if start_time is None and event.key != pygame.K_r:
                    start_time = time.time()  # Start the timer when the first move is made

                if event.key == pygame.K_UP and j < 12:
                    arr[j + 4], arr[j] = arr[j], arr[j + 4]
                    pygame.time.delay(64)
                    

                elif event.key == pygame.K_DOWN and j > 3:
                    arr[j - 4], arr[j] = arr[j], arr[j - 4]
                    pygame.time.delay(64)
                    

                elif event.key == pygame.K_RIGHT and j % 4 != 0:
                    arr[j - 1], arr[j] = arr[j], arr[j - 1]
                    pygame.time.delay(64)
                    

                elif event.key == pygame.K_LEFT and j not in [3, 7, 11, 15]:
                    arr[j + 1], arr[j] = arr[j], arr[j + 1]
                    pygame.time.delay(64)
                    

        if start_time is not None:
            elapsed_time = int(time.time() - start_time)
        else:
            elapsed_time = None

        draw_window(arr, elapsed_time)

        if (arr[:15] == sorted(arr[:15])):
            pygame.time.delay(1000)
            Handle_Win(elapsed_time)
            start_time = None  # Reset the timer when the game is won
            break

    if run:
        main()
    else:
        pygame.quit()

if __name__ == "__main__":
    main()
