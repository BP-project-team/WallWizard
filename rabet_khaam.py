
import pygame
import sys
import json
import uuid
import os


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
    global current_user_id
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
                if current_field == 'username':
                    if event.key == pygame.K_RETURN:
                        if user_exists(username):
                            with open("users.json", "r") as f:
                                users_data = json.load(f)
                            if users_data[username]["password"] == password:
                                print(f"Welcome {username}!")
                                # ذخیره شناسه کاربر
                                current_user_id = users_data[username]["user_id"]
                                is_logging_in = False
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
                                # ذخیره شناسه کاربر
                                current_user_id = users_data[username]["user_id"]
                                is_logging_in = False
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
                if current_field == 'username':
                    if event.key == pygame.K_RETURN:
                        if user_exists(username):
                            print("Username already taken.")
                        else:
                            user_id = str(uuid.uuid4())
                            save_user(username, password, user_id)
                            current_user_id = user_id  # ذخیره شناسه کاربر
                            print(
                                f"User {username} registered successfully with ID: {user_id}")
                            return
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
                            current_user_id = user_id  # ذخیره شناسه کاربر
                            print(
                                f"User {username} registered successfully with ID: {user_id}")
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

            pygame.display.update()


def main_screen():
    pygame.init()

    screen_width = 500
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Login and Signup")
    font = pygame.font.SysFont("Arial", 24)

    # فایل ذخیره‌سازی کاربران

    # چک می‌کنیم که فایل کاربران وجود دارد یا خیر، اگر ندارد، یک فایل خالی می‌سازیم
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({}, f)

    # متغیر سراسری برای نگهداری شناسه کاربر فعلی
    current_user_id = None
    while True:
        screen.fill((255, 255, 255))
        title_text = font.render("Game Login / Signup", True, (0, 0, 0))
        login_text = font.render("Press L to Login", True, (0, 0, 0))
        signup_text = font.render("Press S to Sign Up", True, (0, 0, 0))

        screen.blit(title_text, (150, 50))
        screen.blit(login_text, (150, 150))
        screen.blit(signup_text, (150, 200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    login_screen(screen, font)
                elif event.key == pygame.K_s:
                    signup_screen(screen, font)


if __name__ == "__main__":
    main_screen()
