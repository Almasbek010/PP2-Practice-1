import random
import pygame
from config import *


UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)


class Snake:
    def __init__(self, color):
        
        cx, cy = COLS // 2, ROWS // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.color = color  
        self.shield_active = False

    def set_direction(self, new_dir):
        """Меняет направление, запрещая разворот на 180°."""
        opp = (-self.direction[0], -self.direction[1])
        if new_dir != opp:
            self.next_direction = new_dir

    def move(self):
        """Делает один шаг: добавляет голову, убирает хвост."""
        self.direction = self.next_direction
        head = self.body[0]
        new_head = (head[0] + self.direction[0],
                    head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self, segments=1):
        """Удлиняет змею на N сегментов (добавляет копии хвоста)."""
        for _ in range(segments):
            self.body.append(self.body[-1])

    def shrink(self, segments=2):
        """Укорачивает змею на N сегментов. Возвращает True если змея мертва."""
        for _ in range(segments):
            if len(self.body) > 1:
                self.body.pop()
        return len(self.body) <= 1

    def head(self):
        return self.body[0]

    def check_wall_collision(self):
        hx, hy = self.head()
        return hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS

    def check_self_collision(self):
        return self.head() in self.body[1:]

    def draw(self, surface):
        for i, seg in enumerate(self.body):
            rect = pygame.Rect(seg[0] * CELL_SIZE, seg[1] * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)
            color = self.color if i > 0 else DARK_GREEN
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, DARK_GRAY, rect, 1)


class Food:
    """Обычная еда (иногда бонусная) с таймером исчезновения."""

    def __init__(self, snake_body, obstacles):
        self.pos = self._random_pos(snake_body, obstacles)
        self.bonus = random.random() < 0.25   
        self.points = FOOD_BONUS_POINTS if self.bonus else FOOD_NORMAL_POINTS
        self.color  = YELLOW if self.bonus else RED
        self.spawn_time = pygame.time.get_ticks()

    def _random_pos(self, snake_body, obstacles):
        forbidden = set(snake_body) | set(obstacles)
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in forbidden:
                return pos

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > FOOD_DISAPPEAR_MS

    def draw(self, surface):
        rect = pygame.Rect(self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        
        elapsed = pygame.time.get_ticks() - self.spawn_time
        if elapsed > FOOD_DISAPPEAR_MS - 1000:
            if (elapsed // 200) % 2 == 0:
                pygame.draw.rect(surface, WHITE, rect, 3)



class PoisonFood:
    def __init__(self, snake_body, obstacles, normal_food_pos):
        forbidden = set(snake_body) | set(obstacles) | {normal_food_pos}
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in forbidden:
                self.pos = pos
                break
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > FOOD_DISAPPEAR_MS

    def draw(self, surface):
        rect = pygame.Rect(self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, DARK_RED, rect)
        # Крестик внутри
        x, y = self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE
        s = CELL_SIZE
        pygame.draw.line(surface, WHITE, (x + 3, y + 3),
                         (x + s - 3, y + s - 3), 2)
        pygame.draw.line(surface, WHITE, (x + s - 3, y + 3),
                         (x + 3, y + s - 3), 2)



POWERUP_SPEED  = "speed"
POWERUP_SLOW   = "slow"
POWERUP_SHIELD = "shield"

POWERUP_COLORS = {
    POWERUP_SPEED:  ORANGE,
    POWERUP_SLOW:   BLUE,
    POWERUP_SHIELD: CYAN,
}

POWERUP_LABELS = {
    POWERUP_SPEED:  "⚡",
    POWERUP_SLOW:   "🐢",
    POWERUP_SHIELD: "🛡",
}


class PowerUp:
    def __init__(self, snake_body, obstacles, food_pos, poison_pos=None):
        kind_list = [POWERUP_SPEED, POWERUP_SLOW, POWERUP_SHIELD]
        self.kind = random.choice(kind_list)
        self.color = POWERUP_COLORS[self.kind]
        self.spawn_time = pygame.time.get_ticks()
        forbidden = set(snake_body) | set(obstacles) | {food_pos}
        if poison_pos:
            forbidden.add(poison_pos)
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in forbidden:
                self.pos = pos
                break

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > POWERUP_FIELD_MS

    def draw(self, surface):
        rect = pygame.Rect(self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 2)



def generate_obstacles(level, snake_body):
    """Генерирует случайные стены начиная с 3-го уровня."""
    if level < 3:
        return []
    count = min((level - 2) * 3, 20)
    obstacles = []
    forbidden = set(snake_body)
    
    hx, hy = snake_body[0]
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            forbidden.add((hx + dx, hy + dy))

    attempts = 0
    while len(obstacles) < count and attempts < 500:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in forbidden and pos not in obstacles:
            obstacles.append(pos)
            forbidden.add(pos)
        attempts += 1
    return obstacles


def draw_obstacles(surface, obstacles):
    for pos in obstacles:
        rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, BROWN, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)



def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WINDOW_WIDTH, y))



def draw_hud(surface, font, score, level, personal_best,
             active_effect, effect_end_time, shield_active):
    
    surface.blit(font.render(f"Score: {score}", True, WHITE), (10, 5))
    
    surface.blit(font.render(f"Level: {level}", True, WHITE), (200, 5))
    
    surface.blit(font.render(f"Best: {personal_best}", True, YELLOW), (350, 5))

    
    if active_effect:
        remaining = max(0, (effect_end_time - pygame.time.get_ticks()) // 1000)
        label = {POWERUP_SPEED: "SPEED", POWERUP_SLOW: "SLOW",
                 POWERUP_SHIELD: "SHIELD"}.get(active_effect, "")
        color = POWERUP_COLORS.get(active_effect, WHITE)
        surface.blit(
            font.render(f"{label} {remaining}s", True, color),
            (560, 5)
        )

    if shield_active:
        surface.blit(font.render("🛡 SHIELD", True, CYAN), (560, 5))