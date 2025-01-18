import pygame
import sys
from pygame.locals import (K_w, K_d, K_a, K_s, 
     K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN
)
class Player(pygame.sprite.Sprite):
    def __init__(self, color, position, walls_number):
        super(Player, self).__init__()
        self.color = color
        self.radius = 15
        self.position = position
        self.walls_number = walls_number
    def move(self, new_x, new_y):
        if valid_move(self.position, new_x, new_y):
            if (new_x, new_y) == players[1 - turn].position:
                return jump(turn, new_x, new_y)    
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
BROWN = (105, 105, 105)
BLUE = (135, 162, 219)

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
turn = 0
players = [
    Player(BLACK, (4, 0), 10),
    Player(WHITE, (4, 8), 10)
]
walls = []
centercells = []
wall_denied = []
def valid_move(position, new_x, new_y):
    if (0 <= new_x < columns and 0 <= new_y < rows):
        current_x = position[0] * cell_size + cell_size // 2
        current_y = position[1] * cell_size + cell_size // 2
        target_x = new_x * cell_size + cell_size // 2
        target_y = new_y * cell_size + cell_size // 2

        for denied in wall_denied:
            x_wall, y_wall, orientation = denied

            if orientation == "V":
                if (current_y > y_wall and current_y < y_wall + 2 * cell_size) and (
                    (current_x < x_wall and target_x >= x_wall) or
                    (current_x > x_wall and target_x <= x_wall)
                ):
                    return False
            elif orientation == "H":
                if (current_x > x_wall and current_x < x_wall + 2 * cell_size) and (
                    (current_y < y_wall and target_y >= y_wall) or
                    (current_y > y_wall and target_y <= y_wall)
                ):
                    return False
        return True
    return False
def jump(player, new_x, new_y):
    x, y = players[player].position
    
    if not valid_move(players[player].position, new_x, new_y):
        return False
    
    opp = 1 - player
    opp_x, opp_y = players[opp].position
    if (new_x, new_y) == (opp_x, opp_y):
        dx = opp_x - x
        dy = opp_y - y
        jump_x = opp_x + dx
        jump_y = opp_y + dy
        
        if not valid_move(players[player].position, jump_x, jump_y):
            return False

        
        if not within_bounds(jump_x, jump_y):
            return False
        else:
            players[player].position = (jump_x, jump_y)
            return True
    return False

def wall(orientation, wall_start, wall_end, centercell):
    if (wall_start, wall_end) in walls or (wall_end, wall_start) in walls:
        return False
    if not (within_bounds(wall_start[1], wall_start[0]) and within_bounds(wall_end[1], wall_end[0])): 
        return False

    if centercell in centercells:
        return False

    if not within_bounds(centercell[1], centercell[0]):
        return False

    y, x = wall_end
    if not within_bounds(x, y):
        return False
    
    if orientation == "H":
        if not within_bounds(wall_start[1] + 1, wall_start[0]):
            return False

        for existing_wall_start, existing_wall_end, _ in walls:
            if existing_wall_start[0] == wall_start[0] and (
                (existing_wall_start[1] == wall_start[1] - 1 and existing_wall_end[1] == wall_end[1] - 1) or
                (existing_wall_start[1] == wall_start[1] + 1 and existing_wall_end[1] == wall_end[1] + 1) or
                existing_wall_start[1] == wall_start[1]
            ):
                return False

    if orientation == "V":
        if not within_bounds(wall_start[1], wall_start[0] + 1):
            return False

        for existing_wall_start, existing_wall_end, _ in walls:
            if existing_wall_start[1] == wall_start[1] and (
                (existing_wall_start[0] == wall_start[0] - 1 and existing_wall_end[0] == wall_end[0] - 1) or
                (existing_wall_start[0] == wall_start[0] + 1 and existing_wall_end[0] == wall_end[0] + 1) or
                existing_wall_start[0] == wall_start[0]
            ):
                return False

    centercells.append(centercell)
    walls.append((wall_start, wall_end, players[turn].color))
    players[turn].walls_number -= 1
    print(f"Player {turn + 1} has {players[turn].walls_number} walls left.")
    return True

def within_bounds(x, y):
    return 0 <= x < 9 and 0 <= y < 9
def winner():
    if players[0].position[1] == 8:
        print("player one has won, jingili jingili ghanarii!!")
        return True
    if players[1].position[1] == 0:
        print("Player two has won, jingili jingili ghanarii!!")
        return True
    return False
running = True
while running:
    screen.fill(BROWN)
    if winner():
        running = False
    for row in range(rows):
        for column in range(columns):
            pygame.draw.rect(
                screen, BLUE, [column * cell_size, row * cell_size, cell_size, cell_size], 5)
                
    for wall_start, wall_end, color in walls:
        if wall_start[0] == wall_end[0]:
            origin_x = wall_start[1] * cell_size
            origin_y = wall_start[0] * cell_size
            wall_denied.append((origin_x, origin_y, "H"))
            pygame.draw.line(screen, color, (origin_x + 5, origin_y),
                             (origin_x + cell_size * 2 - 5, origin_y), 5)
        elif wall_start[1] == wall_end[1]:
            origin_x = wall_start[1] * cell_size
            origin_y = wall_start[0] * cell_size
            wall_denied.append((origin_x, origin_y, "V"))
            pygame.draw.line(screen, color, (origin_x, origin_y + 5),
                             (origin_x, origin_y + cell_size * 2 - 5), 5)

    for player in players:
        player.draw(screen)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            cell_y = y_mouse // cell_size
            cell_x = x_mouse // cell_size
            if players[turn].walls_number != 0:
                if x_mouse % cell_size < 5:
                    wall_start = (cell_y + 0.05, cell_x)
                    wall_end = (cell_y, cell_x)
                    centercell = (cell_y + 1, cell_x)
                    if wall("V", wall_start, wall_end, centercell):
                        turn = 1 - turn
                    else:
                        print(f"Player {1+turn},You can't place a wall in that location.")
                elif y_mouse % cell_size < 5:
                    wall_start = (cell_y, cell_x + 0.05)
                    wall_end = (cell_y, cell_x)
                    centercell = (cell_y, cell_x + 1)
                    if wall("H", wall_start, wall_end, centercell):
                        turn = 1 - turn
                    else:
                        print(f"Player {1+turn},You can't place a wall in that location.")
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
