import pygame
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, color, position):
        super(Player, self).__init__()
        self.color = color
        self.radius = 15 
        self.position = position 
        self.rect = pygame.Rect(position[0] * cell_size, position[1] * cell_size, self.radius * 2, self.radius * 2)

    def move(self, dx, dy):
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        if 0 <= new_x < columns and 0 <= new_y < rows:  
            self.position = (new_x, new_y)

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
        elif event.type == pygame.KEYDOWN:
            dx, dy = 0, 0
            if event.key == pygame.K_w: 
                dy = -1
            elif event.key == pygame.K_s: 
                dy = 1
            elif event.key == pygame.K_a:  
                dx = -1
            elif event.key == pygame.K_d: 
                dx = 1

            if dx != 0 or dy != 0:
                players[turn].move(dx, dy)
                turn = 1 - turn 

pygame.quit()
sys.exit()