import random, pygame, sys
from pygame.locals import *

pygame.init()

FPS = 5
WIDTH = 640
HEIGHT = 480
CELLSIZE = 20

HEAD = 0

# To make sure is going to be a rounded number
assert WIDTH % CELLSIZE == 0
assert HEIGHT % CELLSIZE == 0
CELLWIDTH = int(WIDTH / CELLSIZE)
CELLHEIGHT = int(HEIGHT / CELLSIZE)

print(CELLWIDTH)
print(CELLHEIGHT)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

global FPSCLOCK, DISPLAYSURF, BASICFONT

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
pygame.display.set_caption('BEGgie the snake')

# Create random coordinates for the snake
startx = random.randint(5, CELLWIDTH - 6)
starty = random.randint(5, CELLHEIGHT - 6)
snakeCoords = [{'x': startx, 'y': starty},
               {'x': startx - 1, 'y': starty},
               {'x': startx - 2, 'y': starty}]
# Default snake direction
direction = RIGHT


food = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

# Random Food
def randomFood(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    foodRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GREEN, foodRect)


# Loop that creates a snake body everytime it runs
def drawSnakeBody():
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        # To draw the borders and the blocks
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, "Gray", snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, snakeInnerSegmentRect)

while True:  # main game loop
    for event in pygame.event.get():  # event handling loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Set up direction
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                direction = LEFT
            elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                direction = RIGHT
            elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                direction = UP
            elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                direction = DOWN
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Growing by eating food
    if snakeCoords[HEAD]['x'] == food['x'] and snakeCoords[HEAD]['y'] == food['y']:
        food = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
        snakeCoords.insert(0, newHead)

        # Increasing speed
        FPS = len(snakeCoords) - 1


    # Create a new block at the beginning of the main dict
    if direction == UP:
        newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
    snakeCoords.insert(0, newHead)

    del snakeCoords[-1]  # remove snake's tail segment

    DISPLAYSURF.fill(BGCOLOR)

    # Check if snake ate its own tail
    for snakeBody in snakeCoords[1:]:
        if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
            pygame.quit()
            sys.exit()


    # getting outside of the screen
    if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
        pygame.quit()
        sys.exit()


    drawSnakeBody()
    scoreSurf = BASICFONT.render('Speed: %s' % len(snakeCoords), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    randomFood(food)

    pygame.display.update()
    FPSCLOCK.tick(FPS)

