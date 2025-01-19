import pygame
import sys
import json
import uuid
import os

def game_screen(user_id, load_previous_game=False, game_state=None, opponent_id=None,BLACK = (0, 0, 0) ,WHITE = (255, 255, 255)):
    game_id = str(uuid.uuid4())

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

    if load_previous_game and game_state:
        players = [
            Player(BLACK, tuple(game_state["players"][0]["position"]), game_state["players"][0]["walls_number"]),
            Player(WHITE, tuple(game_state["players"][1]["position"]), game_state["players"][1]["walls_number"])
        ]
        walls = game_state["walls"]
        turn = game_state["turn"]
        centercells = game_state["centercells"]
        wall_denied = game_state["wall_denied"]


    else:
        players = [
            Player(BLACK, (4, 0), 10),
            Player(WHITE, (4, 8), 10)
        ]
        walls = []
        turn = 0
        centercells = []
        wall_denied = []
        save_game_data("player1", "player2", (4, 0), (4, 8), [], 0)


    pygame.init()
    screen_width = 500
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("WallWizard")
    rows, columns = 9, 9
    cell_size = screen_width // columns
    BROWN = (105, 105, 105)
    BLUE = (135, 162, 219)


def orib(x, y, new_x, new_y):
        opponent_x, opponent_y = players[1 - turn].position
        dx = abs(x - opponent_x)
        dy = abs(y - opponent_y)
        
        if not ((dx == 1 and dy == 0) or (dy == 1 and dx == 0)):
            return False
        
        if not jump(turn, new_x, new_y):
            if abs(new_x - x) == 1 and abs(new_y - y) == 1:
                if valid_move((x, y), new_x, new_y):
                    opp_x = opponent_x * cell_size + cell_size // 2
                    opp_y = opponent_y * cell_size + cell_size // 2
                      
                    for denied in wall_denied:
                        x_wall, y_wall, orientation = denied

                        if orientation == "V":
                            if (opp_y > y_wall and opp_y < y_wall + 2 * cell_size) and (
                                (opp_x < x_wall and opp_x + cell_size >= x_wall) or
                                (opp_x > x_wall and opp_x - cell_size <= x_wall)
                            ):
                               players[turn].position = (new_x, new_y)
                               return True
                        elif orientation == "H":
                            if (opp_x > x_wall and opp_x < x_wall + 2 * cell_size) and (
                                (opp_y < y_wall and opp_y + cell_size >= y_wall) or
                                (opp_y > y_wall and opp_y - cell_size <= y_wall)
                            ):
                                players[turn].position = (new_x, new_y)
                                return True
                                      
                   
                   
        return False

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

    def is_wall(x,y,nx, ny, walls):
        if (0 <= nx < columns and 0 <= ny < rows):
            current_x = x * cell_size + cell_size // 2
            current_y = y * cell_size + cell_size // 2
            target_x = nx * cell_size + cell_size // 2
            target_y = ny * cell_size + cell_size // 2

            for denied in walls:
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

    def dfs_recursive(current, target_line, visited, wall_denied):
        x, y = current
        if (target_line == 'top' and y == 0) or (target_line == 'bottom' and y == 8):
            return True

        visited[current] = True

        for dx, dy in [(0, 1), (0,-1 ), (-1, 0), (1,0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < columns and 0 <= ny < rows and 
                (nx, ny) not in visited and 
                is_wall(x, y, nx, ny, wall_denied)):
                if dfs_recursive((nx, ny), target_line, visited, wall_denied):
                    return True
        return False


    def valid_wall_placement(orientation, wall_start, wall_end, centercell):
        walls.append((wall_start, wall_end, players[turn].color))

        if wall_start[0] == wall_end[0]:
                origin_x = wall_start[1] * cell_size
                origin_y = wall_start[0] * cell_size
                wall_denied.append((origin_x, origin_y, "H"))
        elif wall_start[1] == wall_end[1]:
                origin_x = wall_start[1] * cell_size
                origin_y = wall_start[0] * cell_size
                wall_denied.append((origin_x, origin_y, "V"))
        visited_1 = {}
        player_1_pos = players[0].position
        player_2_pos = players[1].position

        if not dfs_recursive(player_1_pos, 'bottom', visited_1, wall_denied):
            walls.pop()
            wall_denied.pop()
            return False

        visited_2 = {}

        if not dfs_recursive(player_2_pos, 'top', visited_2, wall_denied):
            walls.pop()
            wall_denied.pop()
            return False
        
        return True

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
        if not valid_wall_placement(orientation, wall_start, wall_end, centercell):
            return False
        
        walls.append((wall_start, wall_end, players[turn].color))
        players[turn].walls_number -= 1
        print(f"Player {turn + 1} has {players[turn].walls_number} walls left.")
        return True

    def within_bounds(x, y):
        return 0 <= x < 9 and 0 <= y < 9

    def adjacent_move(x, y, new_x, new_y):
        return abs(new_x - x) + abs(new_y - y) == 1

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

    def winner():
        global current_user_id
        if players[0].position[1] == 8:
            print("Player one has won, jingili jingili ghanarii!!")
            save_game_history(current_user_id, "Player 1 won")
            return True
        if players[1].position[1] == 0:
            print("Player two has won, jingili jingili ghanarii!!")
            save_game_history(current_user_id, "Player 2 won")
            return True
        return False
    running = True
    while running:
        
        screen.fill(BROWN)
        if winner():
            """
            player_1_pos = players[0].position
            player_2_pos = players[1].position
            save_game_data("player1", "player2", (4, 0), (4, 8), [], 0)
            """

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
                if event.key == pygame.K_q:
                    if orib(x,y,x - 1, y-1):
                        turn = 1 - turn
                if event.key == pygame.K_e:
                    if orib(x,y,x + 1, y-1):
                        turn = 1 - turn
                if event.key == pygame.K_c:
                    if orib(x,y,x + 1, y+1):
                        turn = 1 - turn
                if event.key == pygame.K_z:
                    if orib(x,y,x -1, y+1):
                        turn = 1 - turn
                elif event.key == pygame.K_o: 
                    save_unfinished_game(user_id, game_id, players, walls, turn, opponent_id,centercells,wall_denied)

                    logout()
                    return
            


def save_user(username, password, user_id):
    try:
        with open("users.json", "r") as f:
            users_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        users_data = {}

    users_data[username] = {
        "username": username,
        "password": password,
        "user_id": user_id
    }

    with open("users.json", "w") as f:
        json.dump(users_data, f, indent=4)


def user_exists(username):
    try:
        with open("users.json", "r") as f:
            users_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        users_data = {}

    return username in users_data


def get_input_field(mouse_pos):
    if 100 <= mouse_pos[1] <= 140:
        return 'username'
    elif 150 <= mouse_pos[1] <= 190:
        return 'password'
    return None

# این و سایناپ میفته تو حلقه وایل و بعد لاگین و سایناپ فالس میشه و اگه فالس شد تابعی که اونور تعریف کردم اجرا نمیشه
def login_screen(screen, font):
    global current_user_id , is_logged_in
    username = ""
    password = ""
    current_field = None
    is_logging_in = True
    while is_logging_in:
        screen.fill((255, 255, 255))

        username_text = font.render(f"Username: {username}", True, (0, 0, 0))
        password_text = font.render(f"Password: {password}", True, (0, 0, 0))
        screen.blit(username_text, (50, 100))
        screen.blit(password_text, (50, 150))

        back_text = font.render("Back to Main Menu (B)", True, (255, 0, 0))
        screen.blit(back_text, (50, 250))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: 
                    return False  # بازگشت به منوی اصلی
            if event.type == pygame.MOUSEBUTTONDOWN:
                field = get_input_field(pygame.mouse.get_pos())
                if field:
                    current_field = field

            if event.type == pygame.KEYDOWN:
                if current_field == 'username':
                    if event.key == pygame.K_RETURN:
                        if user_exists(username):
                            with open("users.json", "r") as f:
                                users_data = json.load(f)
                            if users_data[username]["password"] == password:
                                print(f"Welcome {username}!")
                                current_user_id = users_data[username]["user_id"]
                                is_logged_in = True
                                after_login_screen(screen, font, current_user_id)
                                return True
                            else:
                                print("Incorrect password.")
                        else:
                            print("User does not exist.")
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

                elif current_field == 'password':
                    if event.key == pygame.K_RETURN:
                        if user_exists(username):
                            with open("users.json", "r") as f:
                                users_data = json.load(f)
                            if users_data[username]["password"] == password:
                                print(f"Welcome {username}!")
                                current_user_id = users_data[username]["user_id"]
                                is_logged_in = True
                                after_login_screen(screen, font, current_user_id)                               
                                return True  # ورود موفقیت‌آمیز
                            else:
                                print("Incorrect password.")
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

            pygame.display.update()

def signup_screen(screen, font):
    global current_user_id
    username = ""
    password = ""
    current_field = None
    while True:
        screen.fill((255, 255, 255))

        username_text = font.render(f"Username: {username}", True, (0, 0, 0))
        password_text = font.render(f"Password: {password}", True, (0, 0, 0))
        screen.blit(username_text, (50, 100))
        screen.blit(password_text, (50, 150))

        back_text = font.render("Back to Main Menu (B)", True, (255, 0, 0))
        screen.blit(back_text, (50, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                field = get_input_field(pygame.mouse.get_pos())
                if field:
                    current_field = field
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: 
                    return False  # بازگشت به منوی اصلی

            if event.type == pygame.KEYDOWN:
                if current_field == 'username':
                    if event.key == pygame.K_RETURN:
                        if user_exists(username):
                            print("Username already taken.")
                        else:
                            user_id = str(uuid.uuid4())
                            save_user(username, password, user_id)
                            current_user_id = user_id
                            print(f"User {username} registered successfully with ID: {user_id}")
                            return True  # ثبت‌نام موفقیت‌آمیز
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

                elif current_field == 'password':
                    if event.key == pygame.K_RETURN:
                        if user_exists(username):
                            print("Username already taken.")
                        else:
                            user_id = str(uuid.uuid4())
                            save_user(username, password, user_id)
                            current_user_id = user_id
                            print(f"User {username} registered successfully with ID: {user_id}")
                            return True  # ثبت‌نام موفقیت‌آمیز
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

            pygame.display.update()
def logout():
    global is_logged_in, current_user_id
    is_logged_in = False
    current_user_id = None
    print("Logged out successfully.")

def save_game_history(user_id, result):
    try:
        with open("game_history.json", "r") as f:
            game_history = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        game_history = {}

    if user_id not in game_history:
        game_history[user_id] = []

    game_history[user_id].append(result)

    with open("game_history.json", "w") as f:
        json.dump(game_history, f, indent=4)
def view_game_history(user_id):
    try:
        with open("game_history.json", "r") as f:
            game_history = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("No game history found.")
        return

    if user_id in game_history:
        print(f"Game History for User {user_id}:")
        for game in game_history[user_id]:
            print(game)
    else:
        print("No game history found for this user.")

def view_leaderboard():
    try:
        with open("Games-data.json", "r") as f:
            games = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("No games found.")
        return

    leaderboard = {}
    for game in games:
        if game["game_result"]:
            winner = game["game_result"].split()[1]
            if winner in leaderboard:
                leaderboard[winner] += 1
            else:
                leaderboard[winner] = 1

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    print("Leaderboard:")
    for i, (username, score) in enumerate(sorted_leaderboard[:10], 1):
        print(f"{i}. {username} - {score} wins")


def save_game_history(user_id, result):
    try:
        with open("game_history.json", "r") as f:
            game_history = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        game_history = {}

    if user_id not in game_history:
        game_history[user_id] = []

    game_history[user_id].append(result)

    with open("game_history.json", "w") as f:
        json.dump(game_history, f, indent=4)   
        
def save_unfinished_game(user_id, game_id, players, walls, turn, opponent_id,centercells,wall_denied):
    try:
        with open("unfinished_games.json", "r") as f:
            unfinished_games = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        unfinished_games = {}

    if user_id not in unfinished_games:
        unfinished_games[user_id] = {}

    unfinished_games[user_id][game_id] = {
        "players": [
            {"position": player.position, "walls_number": player.walls_number}
            for player in players
        ],
        "walls": walls,
        "turn": turn,
        "opponent_id": opponent_id,
        "centercells" : centercells,
        "wall_denied" : wall_denied
    }

    with open("unfinished_games.json", "w") as f:
        json.dump(unfinished_games, f, indent=4)

def load_unfinished_game(user_id, game_id):
    try:
        with open("unfinished_games.json", "r") as f:
            unfinished_games = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None

    if user_id in unfinished_games and game_id in unfinished_games[user_id]:
        return unfinished_games[user_id][game_id]
    return None

def list_unfinished_games(user_id):
    try:
        with open("unfinished_games.json", "r") as f:
            unfinished_games = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

    if user_id in unfinished_games:
        return list(unfinished_games[user_id].keys())
    return []
import json
import uuid
from datetime import datetime

def save_game_data(player1_username, player2_username, player1_position, player2_position, walls, current_turn, game_result=None,game_id = None):
    game_data = {
        "game_id": game_id,
        "player1_username": player1_username,
        "player2_username": player2_username,
        "player1_position": player1_position,
        "player2_position": player2_position,
        "walls": walls,
        "current_turn": current_turn,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if game_result else None,
        "game_result": game_result
    }

    try:
        with open("Games-data.json", "r") as f:
            games = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        games = []

    games.append(game_data)

    with open("Games-data.json", "w") as f:
        json.dump(games, f, indent=4)

def save_game_result(game_id, result):
    try:
        with open("Games-data.json", "r") as f:
            games = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return

    for game in games:
        if game["game_id"] == game_id:
            game["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            game["game_result"] = result
            break

    with open("Games-data.json", "w") as f:
        json.dump(games, f, indent=4)

def main_screen():
    pygame.init()

    screen_width = 500
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Login and Signup")
    font = pygame.font.SysFont("Arial", 24)

    global is_logged_in, current_user_id

    while True:
        screen.fill((255, 255, 255))
        title_text = font.render("Game Login / Signup", True, (0, 0, 0))
        login_text = font.render("Press L to Login", True, (0, 0, 0))
        signup_text = font.render("Press S to Sign Up", True, (0, 0, 0))

        screen.blit(title_text, (150, 50))
        screen.blit(login_text, (150, 100))
        screen.blit(signup_text, (150, 150))




        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    if login_screen(screen, font):
                        is_logged_in = True  # کاربر لاگین کرد
                        after_login_screen(screen, font, current_user_id)
                elif event.key == pygame.K_s:
                    if signup_screen(screen, font):
                        is_logged_in = True  # کاربر ثبت‌نام و لاگین کرد
                        after_login_screen(screen, font, current_user_id)
                elif event.key == pygame.K_o and is_logged_in:  # فقط اگر لاگین کرده باشد
                    logout()
                    is_logged_in = False  # کاربر از حساب خارج شد
                    current_user_id = None

                elif event.key == pygame.K_h and is_logged_in:  # فقط اگر لاگین کرده باشد
                    view_game_history(current_user_id)

def start_new_game(screen, font, current_user_id):
    username = ""
    password = ""
    current_field = "username"

    while True:
        screen.fill((255, 255, 255))

        username_text = font.render(f"Opponent Username: {username}", True, (0, 0, 0))
        password_text = font.render(f"Opponent Password: {password}", True, (0, 0, 0))
        screen.blit(username_text, (50, 100))
        screen.blit(password_text, (50, 150))

        back_text = font.render("Back to Menu (B)", True, (255, 0, 0))
        screen.blit(back_text, (50, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: 
                    return
                if event.key == pygame.K_RETURN:
                    if current_field == "username":
                        current_field = "password"
                    elif current_field == "password":
                        if user_exists(username):
                            with open("users.json", "r") as f:
                                users_data = json.load(f)
                            if users_data[username]["password"] == password:
                                opponent_id = users_data[username]["user_id"]
                                game_screen(current_user_id, load_previous_game=False, opponent_id=opponent_id)
                                return
                            else:
                                print("Incorrect password.")
                        else:
                            print("User does not exist.")
                elif event.key == pygame.K_BACKSPACE:
                    if current_field == "username":
                        username = username[:-1]
                    elif current_field == "password":
                        password = password[:-1]
                else:
                    if current_field == "username":
                        username += event.unicode
                    elif current_field == "password":
                        password += event.unicode


def continue_unfinished_game(screen, font, current_user_id):
    games = list_unfinished_games(current_user_id)
    if not games:
        print("No unfinished games found.")
        return

    print("Unfinished Games:")
    for i, game_id in enumerate(games, 1):
        print(f"{i}. Game ID: {game_id}")

    game_id = input("Enter the Game ID to continue: ")
    if game_id in games:
        game_state = load_unfinished_game(current_user_id, game_id)
        if game_state:
            opponent_id = game_state["opponent_id"]
            game_screen(current_user_id, load_previous_game=True, game_state=game_state, opponent_id=opponent_id)
        else:
            print("Failed to load game.")
    else:
        print("Invalid Game ID.")



def after_login_screen(screen, font, current_user_id):
    while True:
        screen.fill((255, 255, 255))  

        title_text = font.render("Welcome to the Game!", True, (0, 0, 0))
        new_game_text = font.render("Press N to Start a New Game", True, (0, 0, 0))
        continue_game_text = font.render("Press  m to Continue Unfinished Game", True, (0, 0, 0))
        history_text = font.render("Press H to View Game History", True, (0, 0, 0))
        leaderboard_text = font.render("Press T to View Leaderboard", True, (0, 0, 0))
        logout_text = font.render("Press O to Logout", True, (0, 0, 0))

        screen.blit(title_text, (100, 50))
        screen.blit(new_game_text, (100, 150))
        screen.blit(continue_game_text, (100, 200))
        screen.blit(history_text, (100, 250))
        screen.blit(leaderboard_text, (100, 300))
        screen.blit(logout_text, (100, 350))

        pygame.display.update()  # به‌روزرسانی صفحه نمایش

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # شروع بازی جدید
                    start_new_game(screen, font, current_user_id)
                elif event.key == pygame.K_m:  # ادامه بازی ناتمام
                    continue_unfinished_game(screen, font, current_user_id)
                elif event.key == pygame.K_h:  # مشاهده تاریخچه بازی‌ها
                    view_game_history(current_user_id)
                elif event.key == pygame.K_t:  # مشاهده جدول نفرات برتر
                    view_leaderboard()
                elif event.key == pygame.K_o:  # خروج از حساب
                    logout()
                    return

if __name__ == "__main__":
    main_screen()
