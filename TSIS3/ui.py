import pygame
from persistence import load_leaderboard, save_settings

WIN_W, WIN_H = 600, 700

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
DARK_GRAY  = (25,  25,  25)
GRAY       = (80,  80,  80)
LIGHT_GRAY = (180, 180, 180)
GREEN      = (0,   200, 0)
YELLOW     = (255, 220, 0)
RED        = (220, 0,   0)
BLUE       = (0,   120, 255)
ORANGE     = (255, 140, 0)



def draw_text_centered(surface, font, text, y, color=WHITE):
    surf = font.render(text, True, color)
    x = (WIN_W - surf.get_width()) // 2
    surface.blit(surf, (x, y))


def draw_button(surface, font, text, rect, hover=False):
    bg = (70, 70, 70) if hover else (40, 40, 40)
    pygame.draw.rect(surface, bg, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
    lbl = font.render(text, True, WHITE)
    surface.blit(lbl, (rect.centerx - lbl.get_width() // 2,
                       rect.centery - lbl.get_height() // 2))


def draw_road_bg(surface):
    surface.fill((30, 80, 30))
    pygame.draw.rect(surface, (70, 70, 70), (80, 0, 440, WIN_H))
    for lane in range(1, 4):
        x = 80 + lane * 110
        for y in range(0, WIN_H, 60):
            pygame.draw.rect(surface, YELLOW, (x - 2, y, 4, 30))



def screen_main_menu(screen, clock, fonts):
    font_big   = fonts["big"]
    font_mid   = fonts["mid"]
    font_small = fonts["small"]

    username     = ""
    input_active = True

    buttons = {
        "play":        pygame.Rect(200, 310, 200, 44),
        "leaderboard": pygame.Rect(200, 365, 200, 44),
        "settings":    pygame.Rect(200, 420, 200, 44),
        "quit":        pygame.Rect(200, 475, 200, 44),
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
                    elif len(username) < 18 and event.unicode.isprintable():
                        username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        if name == "play":
                            return ("play", username.strip() or "Driver")
                        elif name == "quit":
                            return ("quit",)
                        else:
                            return (name,)

        draw_road_bg(screen)

        draw_text_centered(screen, font_big, "RACER", 60, YELLOW)
        draw_text_centered(screen, font_small, "TSIS 3 — Arcade Driving", 115, LIGHT_GRAY)

        draw_text_centered(screen, font_small, "Введи имя гонщика:", 200, LIGHT_GRAY)
        inp_rect = pygame.Rect(150, 225, 300, 38)
        pygame.draw.rect(screen, (20, 20, 20), inp_rect, border_radius=6)
        pygame.draw.rect(screen, GREEN if input_active else LIGHT_GRAY,
                         inp_rect, 2, border_radius=6)
        name_surf = font_mid.render(username or "Driver", True,
                                    WHITE if username else GRAY)
        screen.blit(name_surf, (inp_rect.x + 8, inp_rect.y + 6))

        hint = "Enter чтобы подтвердить" if input_active else f"Привет, {username or 'Driver'}!"
        draw_text_centered(screen, font_small, hint, 268,
                           GRAY if input_active else GREEN)

        labels = {"play": "  Играть", "leaderboard": "  Рейтинг",
                  "settings": "  Настройки", "quit": "  Выход"}
        for name, rect in buttons.items():
            draw_button(screen, font_mid, labels[name], rect,
                        hover=rect.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)



def screen_leaderboard(screen, clock, fonts):
    font_big   = fonts["big"]
    font_mid   = fonts["mid"]
    font_small = fonts["small"]

    entries  = load_leaderboard()
    btn_back = pygame.Rect(200, 630, 200, 44)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(mx, my):
                    return

        draw_road_bg(screen)
        draw_text_centered(screen, font_big, "Топ-10", 25, YELLOW)

        header = f"{'#':<4}{'Имя':<16}{'Счёт':<10}{'Дист.':<10}{'Монет'}"
        screen.blit(font_small.render(header, True, LIGHT_GRAY), (40, 80))
        pygame.draw.line(screen, GRAY, (35, 100), (565, 100))

        if not entries:
            draw_text_centered(screen, font_mid, "Пока нет записей", 300, GRAY)
        else:
            for i, e in enumerate(entries):
                y = 108 + i * 46
                rank  = i + 1
                color = YELLOW if rank == 1 else (ORANGE if rank <= 3 else WHITE)
                row = (f"{rank:<4}{e['name']:<16}"
                       f"{e['score']:<10}{e['distance']:<10}{e['coins']}")
                screen.blit(font_small.render(row, True, color), (40, y))

        draw_button(screen, font_mid, "Назад", btn_back,
                    hover=btn_back.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)



def screen_settings(screen, clock, fonts, settings):
    font_big   = fonts["big"]
    font_mid   = fonts["mid"]
    font_small = fonts["small"]

    car_color_options = [
        ("Синий",     [0,   120, 255]),
        ("Красный",   [220, 0,   0]),
        ("Зелёный",   [0,   180, 0]),
        ("Оранжевый", [255, 140, 0]),
        ("Белый",     [220, 220, 220]),
    ]
    diff_options = ["easy", "normal", "hard"]
    diff_labels  = {"easy": "Легко", "normal": "Нормально", "hard": "Сложно"}

    btn_sound  = pygame.Rect(200, 200, 200, 44)
    btn_save   = pygame.Rect(200, 610, 200, 44)

    color_rects = [pygame.Rect(30 + i * 110, 310, 100, 44)
                   for i in range(len(car_color_options))]
    diff_rects  = [pygame.Rect(60 + i * 165, 430, 150, 44)
                   for i in range(len(diff_options))]

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
                if btn_sound.collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]
                for i, rect in enumerate(color_rects):
                    if rect.collidepoint(mx, my):
                        settings["car_color"] = car_color_options[i][1]
                for i, rect in enumerate(diff_rects):
                    if rect.collidepoint(mx, my):
                        settings["difficulty"] = diff_options[i]
                if btn_save.collidepoint(mx, my):
                    save_settings(settings)
                    return settings

        draw_road_bg(screen)
        draw_text_centered(screen, font_big, "Настройки", 30, WHITE)

        sound_txt = f"Звук: {'ВКЛ' if settings['sound'] else 'ВЫКЛ'}"
        draw_button(screen, font_mid, sound_txt, btn_sound,
                    hover=btn_sound.collidepoint(mx, my))

        draw_text_centered(screen, font_mid, "Цвет машины:", 270, LIGHT_GRAY)
        for i, (name, rgb) in enumerate(car_color_options):
            rect = color_rects[i]
            sel  = (rgb == settings["car_color"])
            pygame.draw.rect(screen, rgb, rect, border_radius=8)
            pygame.draw.rect(screen, WHITE if sel else GRAY,
                             rect, 3 if sel else 1, border_radius=8)
            lbl = font_small.render(name, True, WHITE)
            screen.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.bottom + 4))

        draw_text_centered(screen, font_mid, "Сложность:", 395, LIGHT_GRAY)
        for i, diff in enumerate(diff_options):
            rect = diff_rects[i]
            sel  = (diff == settings["difficulty"])
            bg   = (60, 60, 60) if sel else (30, 30, 30)
            pygame.draw.rect(screen, bg, rect, border_radius=8)
            pygame.draw.rect(screen, YELLOW if sel else GRAY,
                             rect, 2, border_radius=8)
            lbl = font_mid.render(diff_labels[diff], True, YELLOW if sel else WHITE)
            screen.blit(lbl, (rect.centerx - lbl.get_width() // 2,
                               rect.centery - lbl.get_height() // 2))

        cur_color = tuple(settings["car_color"])
        pygame.draw.rect(screen, cur_color,
                         pygame.Rect(270, 505, 60, 80), border_radius=8)
        draw_text_centered(screen, font_small, "Превью", 590, LIGHT_GRAY)

        draw_button(screen, font_mid, "Сохранить и выйти", btn_save,
                    hover=btn_save.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)



def screen_game_over(screen, clock, fonts, score, distance, coins):
    font_big   = fonts["big"]
    font_mid   = fonts["mid"]

    btn_retry = pygame.Rect(100, 480, 170, 44)
    btn_menu  = pygame.Rect(330, 480, 170, 44)

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

        draw_road_bg(screen)
        draw_text_centered(screen, font_big,  "АВАРИЯ!", 120, RED)
        draw_text_centered(screen, font_mid,  f"Счёт:      {score}",    230, WHITE)
        draw_text_centered(screen, font_mid,  f"Дистанция: {distance} м", 275, WHITE)
        draw_text_centered(screen, font_mid,  f"Монеты:    {coins}",    320, YELLOW)

        draw_button(screen, font_mid, "Заново (R)", btn_retry,
                    hover=btn_retry.collidepoint(mx, my))
        draw_button(screen, font_mid, "Меню (Esc)", btn_menu,
                    hover=btn_menu.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)



def draw_hud(surface, fonts, score, distance, coins,
             active_pu, pu_end_time, shield_active):
    font = fonts["small"]
    # Фон HUD
    pygame.draw.rect(surface, (0, 0, 0, 160), (0, 0, WIN_W, 36))

    surface.blit(font.render(f"Счёт: {score}", True, WHITE), (10, 8))
    surface.blit(font.render(f"Дист: {distance}м", True, WHITE), (180, 8))
    surface.blit(font.render(f"Монет: {coins}", True, YELLOW), (360, 8))

    if active_pu:
        remaining = max(0, (pu_end_time - pygame.time.get_ticks()) // 1000)
        pu_labels = {"nitro": "NITRO", "shield": "SHIELD", "repair": "REPAIR"}
        pu_colors = {"nitro": ORANGE, "shield": (0, 200, 220), "repair": GREEN}
        txt   = f"{pu_labels.get(active_pu, '')} {remaining}s"
        color = pu_colors.get(active_pu, WHITE)
        lbl   = font.render(txt, True, color)
        surface.blit(lbl, (WIN_W - lbl.get_width() - 10, 8))