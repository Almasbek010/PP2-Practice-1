import sys
import json
import random
import pygame

from config import *
from game import (Snake, Food, PoisonFood, PowerUp,
                  generate_obstacles, draw_obstacles,
                  draw_grid, draw_hud,
                  UP, DOWN, LEFT, RIGHT,
                  POWERUP_SPEED, POWERUP_SLOW, POWERUP_SHIELD)
import db


SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 0],
    "grid_overlay": True,
    "sound": False,
}


def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            
            for k, v in DEFAULT_SETTINGS.items():
                data.setdefault(k, v)
            return data
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)



def draw_text_centered(surface, font, text, y, color=WHITE):
    surf = font.render(text, True, color)
    x = (WINDOW_WIDTH - surf.get_width()) // 2
    surface.blit(surf, (x, y))


def draw_button(surface, font, text, rect, hover=False):
    color = (80, 80, 80) if hover else (40, 40, 40)
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
    label = font.render(text, True, WHITE)
    lx = rect.x + (rect.width - label.get_width()) // 2
    ly = rect.y + (rect.height - label.get_height()) // 2
    surface.blit(label, (lx, ly))



def screen_main_menu(screen, clock, fonts):
    """
    Показывает главное меню.
    Возвращает ('play', username) или ('leaderboard',) или ('settings',) или ('quit',)
    """
    font_big   = fonts["big"]
    font_mid   = fonts["mid"]
    font_small = fonts["small"]

    username = ""
    input_active = True

    buttons = {
        "play":        pygame.Rect(300, 300, 200, 45),
        "leaderboard": pygame.Rect(300, 360, 200, 45),
        "settings":    pygame.Rect(300, 420, 200, 45),
        "quit":        pygame.Rect(300, 480, 200, 45),
    }

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ("quit",)

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_active = False
                    elif len(username) < 20 and event.unicode.isprintable():
                        username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        if name == "play":
                            u = username.strip() or "Player"
                            return ("play", u)
                        elif name == "quit":
                            return ("quit",)
                        else:
                            return (name,)

        screen.fill(DARK_GRAY)

        
        draw_text_centered(screen, font_big, "SNAKE GAME", 60, GREEN)
        draw_text_centered(screen, font_small, "Принципы программирования 2 — TSIS 4",
                           120, LIGHT_GRAY)

        
        draw_text_centered(screen, font_mid, "Введи имя:", 195, LIGHT_GRAY)
        input_rect = pygame.Rect(250, 225, 300, 40)
        border_color = GREEN if input_active else LIGHT_GRAY
        pygame.draw.rect(screen, (20, 20, 20), input_rect, border_radius=6)
        pygame.draw.rect(screen, border_color, input_rect, 2, border_radius=6)
        name_surf = font_mid.render(username or "Player", True,
                                    WHITE if username else GRAY)
        screen.blit(name_surf, (input_rect.x + 8, input_rect.y + 6))

        hint = "нажми Enter чтобы зафиксировать имя" if input_active else f"✓ Привет, {username or 'Player'}!"
        draw_text_centered(screen, font_small, hint, 272,
                           GRAY if input_active else GREEN)

        
        labels = {"play": "Играть", "leaderboard": "Рейтинг",
                  "settings": "Настройки", "quit": "Выход"}
        for name, rect in buttons.items():
            draw_button(screen, font_mid, labels[name], rect,
                        hover=rect.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(FPS)



def screen_leaderboard(screen, clock, fonts):
    font_big   = fonts["big"]
    font_mid   = fonts["mid"]
    font_small = fonts["small"]

    rows = db.get_top10()
    btn_back = pygame.Rect(300, 545, 200, 40)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(mx, my):
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(DARK_GRAY)
        draw_text_centered(screen, font_big, "🏆 Топ-10 игроков", 20, YELLOW)

        
        header = f"{'#':<4} {'Имя':<15} {'Счёт':<8} {'Уровень':<10} {'Дата'}"
        screen.blit(font_small.render(header, True, LIGHT_GRAY), (40, 80))
        pygame.draw.line(screen, GRAY, (40, 100), (760, 100))

        if not rows:
            draw_text_centered(screen, font_mid, "Пока нет записей 😢", 280, GRAY)
        else:
            for i, (rank, username, score, level, date) in enumerate(rows):
                y = 110 + i * 38
                color = YELLOW if rank == 1 else (LIGHT_GRAY if rank <= 3 else WHITE)
                line = f"{rank:<4} {username:<15} {score:<8} {level:<10} {date}"
                screen.blit(font_small.render(line, True, color), (40, y))

        draw_button(screen, font_mid, "← Назад", btn_back,
                    hover=btn_back.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(FPS)



def screen_settings(screen, clock, fonts, settings):
    font_big   = fonts["big"]
    font_mid   = fonts["mid"]

    color_options = [
        ("Зелёный",   [0, 200, 0]),
        ("Синий",     [0, 120, 255]),
        ("Оранжевый", [255, 140, 0]),
        ("Фиолетовый",[160, 0, 200]),
        ("Белый",     [220, 220, 220]),
    ]

    btn_grid  = pygame.Rect(300, 200, 200, 45)
    btn_sound = pygame.Rect(300, 265, 200, 45)
    btn_save  = pygame.Rect(300, 480, 200, 45)

    
    color_rects = []
    for i, (name, _) in enumerate(color_options):
        color_rects.append(pygame.Rect(150 + i * 105, 370, 95, 45))

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return settings
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings)
                return settings
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_grid.collidepoint(mx, my):
                    settings["grid_overlay"] = not settings["grid_overlay"]
                if btn_sound.collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]
                for i, rect in enumerate(color_rects):
                    if rect.collidepoint(mx, my):
                        settings["snake_color"] = color_options[i][1]
                if btn_save.collidepoint(mx, my):
                    save_settings(settings)
                    return settings

        screen.fill(DARK_GRAY)
        draw_text_centered(screen, font_big, "⚙ Настройки", 40, WHITE)

        
        grid_text = f"Сетка: {'ВКЛ' if settings['grid_overlay'] else 'ВЫКЛ'}"
        draw_button(screen, font_mid, grid_text, btn_grid,
                    hover=btn_grid.collidepoint(mx, my))

        
        sound_text = f"Звук: {'ВКЛ' if settings['sound'] else 'ВЫКЛ'}"
        draw_button(screen, font_mid, sound_text, btn_sound,
                    hover=btn_sound.collidepoint(mx, my))

        
        draw_text_centered(screen, font_mid, "Цвет змеи:", 330, LIGHT_GRAY)
        cur_color = tuple(settings["snake_color"])
        for i, (name, rgb) in enumerate(color_options):
            rect = color_rects[i]
            selected = (rgb == settings["snake_color"])
            pygame.draw.rect(screen, rgb, rect, border_radius=8)
            border = WHITE if selected else GRAY
            pygame.draw.rect(screen, border, rect,
                             3 if selected else 1, border_radius=8)
            lbl = fonts["small"].render(name, True, WHITE)
            screen.blit(lbl, (rect.x + (rect.width - lbl.get_width()) // 2,
                               rect.y + rect.height + 5))

        
        preview_rect = pygame.Rect(330, 430, 140, 30)
        pygame.draw.rect(screen, cur_color, preview_rect, border_radius=6)
        draw_text_centered(screen, fonts["small"], "Превью цвета", 465, LIGHT_GRAY)

        draw_button(screen, font_mid, "💾 Сохранить и выйти", btn_save,
                    hover=btn_save.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(FPS)



def screen_game_over(screen, clock, fonts, score, level, personal_best):
    font_big   = fonts["big"]
    font_mid   = fonts["mid"]

    btn_retry = pygame.Rect(200, 400, 160, 45)
    btn_menu  = pygame.Rect(440, 400, 160, 45)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(mx, my):
                    return "retry"
                if btn_menu.collidepoint(mx, my):
                    return "menu"

        screen.fill(DARK_GRAY)
        draw_text_centered(screen, font_big, "💀 КОНЕЦ ИГРЫ", 120, RED)
        draw_text_centered(screen, font_mid, f"Твой счёт:  {score}", 220, WHITE)
        draw_text_centered(screen, font_mid, f"Уровень:    {level}", 265, WHITE)
        new_best = score >= personal_best and score > 0
        best_color = YELLOW if new_best else LIGHT_GRAY
        best_text  = f"Рекорд: {max(score, personal_best)}"
        if new_best:
            best_text += "  🎉 Новый рекорд!"
        draw_text_centered(screen, font_mid, best_text, 310, best_color)

        draw_button(screen, font_mid, "▶  Заново (R)", btn_retry,
                    hover=btn_retry.collidepoint(mx, my))
        draw_button(screen, font_mid, "🏠  Меню (Esc)", btn_menu,
                    hover=btn_menu.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(FPS)



def run_game(screen, clock, fonts, username, player_id, personal_best, settings):
    """
    Запускает одну игровую сессию.
    Возвращает (score, level_reached).
    """
    snake_color = tuple(settings["snake_color"])
    snake = Snake(snake_color)

    score = 0
    level = 1
    food_eaten = 0

    obstacles = []
    food = Food(snake.body, obstacles)
    poison = None
    powerup = None

    
    active_effect = None
    effect_end_time = 0

    
    step_timer = 0
    current_speed = BASE_SPEED

    
    poison_timer  = pygame.time.get_ticks()
    powerup_timer = pygame.time.get_ticks()
    POISON_INTERVAL  = 7000   
    POWERUP_INTERVAL = 12000  

    running = True
    while running:
        now = pygame.time.get_ticks()
        dt = clock.tick(FPS)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, level
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP,    pygame.K_w): snake.set_direction(UP)
                if event.key in (pygame.K_DOWN,  pygame.K_s): snake.set_direction(DOWN)
                if event.key in (pygame.K_LEFT,  pygame.K_a): snake.set_direction(LEFT)
                if event.key in (pygame.K_RIGHT, pygame.K_d): snake.set_direction(RIGHT)
                if event.key == pygame.K_ESCAPE:
                    return score, level

        
        base = max(40, BASE_SPEED - (level - 1) * SPEED_PER_LVLEVEL)
        if active_effect == POWERUP_SPEED:
            current_speed = max(40, base - 60)
        elif active_effect == POWERUP_SLOW:
            current_speed = base + 80
        else:
            current_speed = base

        
        if active_effect and now >= effect_end_time:
            active_effect = None
            snake.shield_active = False

        
        step_timer += dt
        if step_timer >= current_speed:
            step_timer = 0
            snake.move()

            
            if snake.check_wall_collision():
                if snake.shield_active:
                    snake.shield_active = False
                    active_effect = None
                    
                    hx = max(0, min(COLS - 1, snake.body[0][0]))
                    hy = max(0, min(ROWS - 1, snake.body[0][1]))
                    snake.body[0] = (hx, hy)
                else:
                    running = False
                    break

            
            if snake.check_self_collision():
                if snake.shield_active:
                    snake.shield_active = False
                    active_effect = None
                else:
                    running = False
                    break

            
            if snake.head() in obstacles:
                if snake.shield_active:
                    snake.shield_active = False
                    active_effect = None
                    
                    obstacles.remove(snake.head())
                else:
                    running = False
                    break

            
            if snake.head() == food.pos:
                score += food.points
                food_eaten += 1
                snake.grow()
                food = Food(snake.body, obstacles)

                
                if food_eaten % FOOD_PER_LEVEL == 0:
                    level += 1
                    obstacles = generate_obstacles(level, snake.body)
                    
                    food = Food(snake.body, obstacles)
                    poison = None
                    powerup = None

            
            if food.is_expired():
                food = Food(snake.body, obstacles)

            
            if poison and snake.head() == poison.pos:
                dead = snake.shrink(2)
                poison = None
                if dead:
                    running = False
                    break

            
            if poison and poison.is_expired():
                poison = None

            
            if powerup and snake.head() == powerup.pos:
                kind = powerup.kind
                powerup = None
                active_effect = kind
                effect_end_time = now + POWERUP_EFFECT_MS
                if kind == POWERUP_SHIELD:
                    snake.shield_active = True

            
            if powerup and powerup.is_expired():
                powerup = None

        
        if poison is None and now - poison_timer > POISON_INTERVAL:
            poison_timer = now
            if random.random() < 0.6:
                fp = food.pos
                obs = obstacles
                poison = PoisonFood(snake.body, obs, fp)

        
        if powerup is None and now - powerup_timer > POWERUP_INTERVAL:
            powerup_timer = now
            if random.random() < 0.5:
                fp = food.pos
                pp = poison.pos if poison else None
                powerup = PowerUp(snake.body, obstacles, fp, pp)

        
        screen.fill(BLACK)

        if settings["grid_overlay"]:
            draw_grid(screen)

        draw_obstacles(screen, obstacles)
        food.draw(screen)
        if poison:
            poison.draw(screen)
        if powerup:
            powerup.draw(screen)
        snake.draw(screen)

        draw_hud(screen, fonts["small"], score, level, personal_best,
                 active_effect, effect_end_time, snake.shield_active)

        pygame.display.flip()

    return score, level



def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("🐍 Snake Game — TSIS 4")
    clock = pygame.time.Clock()

    
    fonts = {
        "big":   pygame.font.SysFont("Arial", 48, bold=True),
        "mid":   pygame.font.SysFont("Arial", 28),
        "small": pygame.font.SysFont("Consolas", 18),
    }

    
    try:
        db.init_db()
        db_available = True
    except Exception as e:
        print(f"[WARN] БД недоступна: {e}. Игра работает без сохранения.")
        db_available = False

    settings = load_settings()
    current_user = None
    player_id = -1
    personal_best = 0

    
    while True:
        result = screen_main_menu(screen, clock, fonts)

        if result[0] == "quit":
            break

        elif result[0] == "leaderboard":
            screen_leaderboard(screen, clock, fonts)

        elif result[0] == "settings":
            settings = screen_settings(screen, clock, fonts, settings)

        elif result[0] == "play":
            username = result[1]
            if db_available:
                player_id = db.get_or_create_player(username)
                personal_best = db.get_personal_best(player_id)
            else:
                player_id = -1
                personal_best = 0

            
            while True:
                score, level = run_game(
                    screen, clock, fonts,
                    username, player_id, personal_best, settings
                )

                
                if score > personal_best:
                    personal_best = score

                
                if db_available and player_id != -1:
                    db.save_session(player_id, score, level)

                action = screen_game_over(
                    screen, clock, fonts, score, level, personal_best
                )

                if action == "retry":
                    continue
                elif action == "menu":
                    break
                else:
                    pygame.quit()
                    sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()