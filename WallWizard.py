import pygame
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, color, position):
        super(Player, self).__init__()
        self.color = color
        self.radius = 15 
        self.position = position 
    def move(self, new_x, new_y):
        if (0 <= new_x < columns and 0 <= new_y < rows) and ((abs(new_x-self.position[0]) == 1 and abs(new_y-self.position[1]) == 0) or (abs(new_y-self.position[1]) == 1 and abs(new_x-self.position[0]) == 0)):

            if players[0].position==players[1].position:
                if players[0].position[0]==players[1].position[0]:
                    players[turn].move(new_x, new_y+1)
                if players[0].position[1]==players[1].position[1]:
                    players[turn].move(new_x+1, new_y)
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
from pygame.locals import (
    K_w,
    K_d,
    K_a,
    K_s,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)
def within_bounds(x, y):
        return 0 <= x < 9 and 0 <= y <9


def adjacent_move( x, y,new_x, new_y ):
        return abs(new_x - x) + abs(new_y - y) == 1


#def blocked_by_wall( x, y, new_x, new_y ):
    
 #   for wx, wy, orientation in walls:
  #      if orientation == "H" and wy == max(y, new_y) and wx <= x < wx + 2:
   #         return True
    #    if orientation == "V" and wx == max(x, new_x) and wy <= y < wy + 2:
     #       return True
   # return False


def is_valid_move(player, new_pos):
    
    x, y = players[player].position
    new_x, new_y = new_pos

    if not within_bounds(new_x, new_y ):
        return False

    if not adjacent_move( x, y, new_x, new_y ):
        return False

 #   if blocked_by_wall(x, y, new_x, new_y ):
  #      return False

    return True

def jump (player, new_pos):
    x, y = players[player].position
    new_x, new_y = new_pos

    if not is_valid_move(player, new_pos):
        return False
        
    opp = 1 - player 
    opp_x, opp_y = players[opp].position

    if new_pos == (opp_x, opp_y): 
        dx = opp_x - x
        dy = opp_y - y
        jump_x = opp_x + dx
        jump_y = opp_y + dy

       
        if not within_bounds(jump_x, jump_y ):
            return False
      #  if blocked_by_wall(x, y, jump_x, jump_y ):
       #   return False
        else:
            players[player].position = (jump_x, jump_y) 
            return True

def wall(oriation,wall_start,wall_end):
    print("karen")
running = True
while running:
    screen.fill(BROWN)

    for row in range(rows):
        for column in range(columns):
            pygame.draw.rect(screen, BLUE, [column * cell_size, row * cell_size, cell_size, cell_size], 5)

    for player in players:
        player.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.MOUSEBUTTONDOWN:
            x_mouse,y_mouse=pygame.mouse.get_pos()
            if y_mouse%cell_size<5:
                cell_y = y_mouse//cell_size
                cell_x = x_mouse//cell_size
                wall_type="H"
                wall_start=(cell_y,cell_x)
                wall_end=(cell_y+1,cell_x)
                wall("H",wall_start,wall_end)
            if x_mouse%cell_size<5:
                cell_y = y_mouse//cell_size
                cell_x = x_mouse//cell_size
                wall_type="V"
                wall_start=(cell_y,cell_x)
                wall_end=(cell_y,cell_x+1)
                wall("V",wall_start,wall_end)
            y=y_mouse//cell_size
            x=x_mouse//cell_size
            new_pos = (x,y)
            if new_pos == (players[1-turn].position[0] , players[1-turn].position[1] ):
                   jump(turn , new_pos ) 
                   turn=1-turn
            elif players[turn].move(x,y):
                turn=1-turn
        if event.type == pygame.KEYDOWN:
            x,y=players[turn].position
            if event.key == pygame.K_w: 
                new_pos = (players[turn].position[0],
                          players[turn].position[1] - 1)
                if new_pos == (players[1-turn].position[0] , players[1-turn].position[1] ):
                   jump(turn , new_pos ) 
                   turn=1-turn
                elif is_valid_move(turn, new_pos):
                   players[turn].position = new_pos
                   turn=1-turn
            if event.key == pygame.K_s:
                new_pos = (players[turn].position[0],
                          players[turn].position[1] + 1)
                if new_pos == (players[1-turn].position[0] , players[1-turn].position[1] ):
                   jump(turn , new_pos ) 
                   turn=1-turn
                elif is_valid_move(turn, new_pos):
                   players[turn].position = new_pos
                   turn=1-turn
                
            if event.key == pygame.K_a:
                new_pos = (players[turn].position[0] -1,
                          players[turn].position[1] )
                if new_pos == (players[1-turn].position[0] , players[1-turn].position[1] ):
                   jump(turn , new_pos ) 
                   turn=1-turn
                elif is_valid_move(turn, new_pos):
                   players[turn].position = new_pos
                   turn=1-turn
            if event.key == pygame.K_d: 
                new_pos = (players[turn].position[0] + 1 ,
                          players[turn].position[1] )
                if new_pos == (players[1-turn].position[0] , players[1-turn].position[1] ):
                   jump(turn , new_pos ) 
                   turn=1-turn
                elif is_valid_move(turn, new_pos):
                   players[turn].position = new_pos
                   turn=1-turn
pygame.quit()
sys.exit()
