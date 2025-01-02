def wall_placement(wall_location1,wall_location2):
    print("salam")
def movement(kind_of_move):
    print("chetoriayi")
def movement_choice():
    choice=input("To place a wall type(wall) or if you want to move, type(move): ")
    if choice == "move":
        try:
            true=1
            while true:
                kind_of_move=input("type(w) to go forward,(d) to go right,(a) to go left and (s) to go bottom: ")
                if kind_of_move in ["w","d","a","s"]:
                    if kind_of_move=="w":
                        true-=1
                        movement("w")
                    if kind_of_move=="d":
                        true-=1
                        movement("d")
                    if kind_of_move=="a":
                        true-=1
                        movement("a")
                    if kind_of_move=="s":
                        true-=1
                        movement("s")     
                else:
                    print("When you choose to move your choice are limited to go forward(w) or right(d) or left(a) or bottom(s).")
        except:
            print("When you choose to move your choice are limited to go forward(w) or right(d) or left(a) or bottom(s).")
            return movement_choice()
    if choice=="wall":
        try:
            true=1
            while true:
                wall_location1=map(int,input("Enter first coordinate in form of (x y) like 2 0:").split())
                if not wall_location1.isdigit():
                    print("Cordinates should be in form of (x, y) like 0 2.")
                wall_location2=map(int,input("Enter second coordinate in form of (x y) like 2 1:").split())
                if not wall_location2.isdigit():
                    print("Cordinates should be in form of (x, y) like 0 2.")
                else:
                    true-=1
                wall_placement(wall_location1,wall_location2)
        except: 
            print("Cordinates should be in form of (x, y) like 0 2.")
            return movement_choice()turn = 0

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
                y=y_mouse//cell_size
                x=x_mouse//cell_size
                players[turn].move(x,y)
                turn=1-turn
        if event.type == pygame.KEYDOWN:
            x,y=players[turn].position
            if event.key == pygame.K_w: 
                players[turn].move(x,y-1)
                turn=1-turn
            if event.key == pygame.K_s:
                players[turn].move(x,y+1)
                turn=1-turn
            if event.key == pygame.K_a:
                players[turn].move(x-1,y)
                turn=1-turn
            if event.key == pygame.K_d: 
                players[turn].move(x+1,y)
                turn=1-turn
pygame.quit()
sys.exit()
