import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, color, position, walls_number):
        super(Player, self).__init__()
        self.color = color
        self.radius = 15
        self.position = position
        self.walls_number = walls_number
              
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
           
            pygame.draw.line(screen, color, (origin_x + 5, origin_y),
                             (origin_x + cell_size * 2 - 5, origin_y), 5)
        elif wall_start[1] == wall_end[1]:
            origin_x = wall_start[1] * cell_size
            origin_y = wall_start[0] * cell_size
            
            pygame.draw.line(screen, color, (origin_x, origin_y + 5),
                             (origin_x, origin_y + cell_size * 2 - 5), 5)

    for player in players:
        player.draw(screen)

    pygame.display.flip()