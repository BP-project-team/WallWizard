import pygame
import sys
from pygame.locals import (
    K_w, K_d, K_a, K_s, K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN
)
class Player(pygame.sprite.Sprite):
    def __init__(self, color, position):
        super(Player, self).__init__()
        self.color = color
        self.radius = 15
        self.position = position
    def move(self, new_x, new_y):
        if (0 <= new_x < columns and 0 <= new_y < rows) and (
            (abs(new_x-self.position[0]) == 1 and abs(new_y-self.position[1]) == 0) or 
            (abs(new_y-self.position[1]) == 1 and abs(new_x-self.position[0]) == 0)):
            
            if players[0].position == players[1].position:
                if players[0].position[0] == players[1].position[0]:
                    players[turn].move(new_x, new_y + 1)
                if players[0].position[1] == players[1].position[1]:
                    players[turn].move(new_x + 1, new_y)
            self.position = (new_x, new_y)
            return True
        return False
    def draw(self, surface):
        x = self.position[0] * cell_size + cell_size // 2
        y = self.position[1] * cell_size + cell_size // 2
        pygame.draw.circle(surface, self.color, (x, y), self.radius)
pygame.init()
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WallWizard")
rows, columns = 9, 9
cell_size = screen_width // columns
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
turn = 0
players = [
    Player(YELLOW, (4, 0)),
    Player(WHITE, (4, 8))
]
walls = []
centercells = []
def wall(orientation, wall_start, wall_end,centercell):
    if (wall_start, wall_end) in walls or (wall_end, wall_start) in walls:
        return False
    if centercell in centercells:
        return False
    centercells.append(centercell)
    walls.append((wall_start, wall_end))

running = True
while running:
    screen.fill(BROWN)
    for row in range(rows):
        for column in range(columns):
            pygame.draw.rect(
                screen, BLUE, [column * cell_size, row * cell_size, cell_size, cell_size], 5)
    for wall_start, wall_end in walls:
        if wall_start[0] == wall_end[0]:
            origin_x = wall_start[1] * cell_size
            origin_y = wall_start[0] * cell_size
            pygame.draw.line(screen, WHITE, (origin_x, origin_y),
                             (origin_x + cell_size*2, origin_y), 5)
        elif wall_start[1] == wall_end[1]:
            origin_x = wall_start[1] * cell_size
            origin_y = wall_start[0] * cell_size
            pygame.draw.line(screen, WHITE, (origin_x, origin_y),
                             (origin_x, origin_y + 2*cell_size), 5)
    for player in players:
        player.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            if y_mouse % cell_size < 5:
                cell_y = y_mouse // cell_size
                cell_x = x_mouse // cell_size
                wall_type = "H"
                wall_start = (cell_y, cell_x)
                wall_end = (cell_y, cell_x+1)
                centercell = (cell_y, cell_x+ 1)
                if not wall("H", wall_start, wall_end, centercell):
                    print('n')
                wall("H", wall_start, wall_end, centercell)
            if x_mouse % cell_size < 5:
                cell_y = y_mouse // cell_size
                cell_x = x_mouse // cell_size
                wall_type = "V"
                wall_start = (cell_y, cell_x)
                wall_end = (cell_y+1, cell_x)

                centercell = (cell_y + 1, cell_x)
                if not wall("V", wall_start, wall_end,centercell):
                    print('n')
                wall("V", wall_start, wall_end,centercell)
            y = y_mouse // cell_size
            x = x_mouse // cell_size
            if players[turn].move(x, y):
                turn = 1 - turn
        if event.type == pygame.KEYDOWN:
            x, y = players[turn].position
            if event.key == pygame.K_w:
                if players[turn].move(x, y - 1):
                    turn = 1 - turn
            if event.key == pygame.K_s:
                if players[turn].move(x, y + 1):
                    turn = 1 - turn
            if event.key == pygame.K_a:
                if players[turn].move(x - 1, y):
                    turn = 1 - turn
            if event.key == pygame.K_d:
                if players[turn].move(x + 1, y):
                    turn = 1 - turn
pygame.quit()
sys.exit()
