# import the modules
import random
import pygame
import sys

from pygame.locals import *


snake_speed = 5
windows_width = 800
windows_height = 600
cell_size = 20       #segment_size


map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)

# color
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue =(0,0, 139)


BG_COLOR = black  # back_ground

# directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

HEAD = 0  # snake_head


def main():
	pygame.init()
	snake_speed_clock = pygame.time.Clock()
	screen = pygame.display.set_mode((windows_width, windows_height))
	screen.fill(white)

	pygame.display.set_caption("Snake Game --by Harvey ") #title
	show_start_info(screen)
	while True:
		running_game(screen, snake_speed_clock)
		show_gameover_info(screen)


def running_game(screen,snake_speed_clock):
	startx = random.randint(3, map_width - 8)
	starty = random.randint(3, map_height - 8)
	snake_coords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

	direction = RIGHT

	food = get_random_location()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
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
					terminate()

		move_snake(direction, snake_coords)

		ret = snake_is_alive(snake_coords)
		if not ret:
			break
		snake_is_eat_food(snake_coords, food)

		screen.fill(BG_COLOR)
		draw_snake(screen, snake_coords)
		draw_food(screen, food)
		draw_score(screen, len(snake_coords) - 3)
		pygame.display.update()
		snake_speed_clock.tick(snake_speed)


def draw_food(screen, food):
	x = food['x'] * cell_size
	y = food['y'] * cell_size
	appleRect = pygame.Rect(x, y, cell_size, cell_size)
	pygame.draw.rect(screen, Red, appleRect)


def draw_snake(screen, snake_coords):
	for coord in snake_coords:
		x = coord['x'] * cell_size
		y = coord['y'] * cell_size
		wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
		pygame.draw.rect(screen, dark_blue, wormSegmentRect)
		wormInnerSegmentRect = pygame.Rect(
			x + 4, y + 4, cell_size - 8, cell_size - 8)
		pygame.draw.rect(screen, blue, wormInnerSegmentRect)


def draw_grid(screen):
	for x in range(0, windows_width, cell_size):
		pygame.draw.line(screen, dark_gray, (x, 0), (x, windows_height))
	for y in range(0, windows_height, cell_size):
		pygame.draw.line(screen, dark_gray, (0, y), (windows_width, y))


def move_snake(direction, snake_coords):
    if direction == UP:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': snake_coords[HEAD]['x'] - 1, 'y': snake_coords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}

    snake_coords.insert(0, newHead)


def snake_is_alive(snake_coords):
	tag = True
	if snake_coords[HEAD]['x'] == -1 or snake_coords[HEAD]['x'] == map_width or snake_coords[HEAD]['y'] == -1 or \
			snake_coords[HEAD]['y'] == map_height:
		tag = False # snake hit the wall
	for snake_body in snake_coords[1:]:
		if snake_body['x'] == snake_coords[HEAD]['x'] and snake_body['y'] == snake_coords[HEAD]['y']:
			tag = False # snake bites itself
	return tag


def snake_is_eat_food(snake_coords, food):
	if snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']:
		'''food refresh '''
		food['x'] = random.randint(0, map_width - 1)
		food['y'] = random.randint(0, map_height - 1)
	else:
		del snake_coords[-1]


def get_random_location():
	return {'x': random.randint(0, map_width - 1), 'y': random.randint(0, map_height - 1)}


def show_start_info(screen):
	font = pygame.font.SysFont("Courier", 40, bold=True)
	tip = font.render('Press any key to start...', True, (65, 105, 225))
	gamestart = pygame.image.load('gamestart.jpg')
	screen.blit(gamestart, (140, 30))
	screen.blit(tip, (110, 550))
	pygame.display.update()

	while True:
		for event in pygame.event.get():  # event handling loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_ESCAPE):
					terminate()
				else:
					return  # start


def show_gameover_info(screen):
	font = pygame.font.SysFont("Courier", 40, bold=True)
	tip = font.render('Any key to continue...', True, (65, 105, 225))
	gamestart = pygame.image.load('gameover.png')
	screen.blit(gamestart, (60, 0))
	screen.blit(tip, (140, 480))
	pygame.display.update()

	while True:
		for event in pygame.event.get():  # event handling loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					terminate()
				else:
					return


def draw_score(screen,score):
	font = pygame.font.Font("myfont.ttf", 30)
	scoreSurf = font.render('Score: %s' % score, True, "green")
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (windows_width - 120, 10)
	screen.blit(scoreSurf, scoreRect)


def terminate():
	pygame.quit()
	sys.exit()


main()