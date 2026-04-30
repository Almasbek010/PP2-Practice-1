import pygame
import random

WIN_W, WIN_H = 600, 700
ROAD_X       = 80
ROAD_W       = 440
LANE_COUNT   = 4
LANE_W       = ROAD_W // LANE_COUNT

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (80,  80,  80)
DARK_GRAY  = (40,  40,  40)
YELLOW     = (255, 220, 0)
RED        = (220, 0,   0)
GREEN      = (0,   200, 0)
ORANGE     = (255, 140, 0)
CYAN       = (0,   200, 220)
PURPLE     = (160, 0,   200)
BROWN      = (120, 60,  0)
OLIVE      = (180, 180, 0)

CAR_W, CAR_H       = 40, 70
ENEMY_W, ENEMY_H   = 40, 65
OBS_W, OBS_H       = 40, 25
COIN_R             = 12
POWERUP_W          = 36

BASE_ROAD_SPEED    = 5
NITRO_BONUS        = 4
DIFFICULTY_SPEEDS  = {"easy": 4, "normal": 5, "hard": 7}
 
 
def lane_center_x(lane):
    return ROAD_X + lane * LANE_W + LANE_W // 2
 
 
class Road:
    def __init__(self):
        self.offset = 0
 
    def update(self, speed):
        self.offset = (self.offset + speed) % 60
 
    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, (ROAD_X, 0, ROAD_W, WIN_H))
        pygame.draw.rect(surface, OLIVE, (0, 0, ROAD_X, WIN_H))
        pygame.draw.rect(surface, OLIVE, (ROAD_X + ROAD_W, 0, WIN_W - ROAD_X - ROAD_W, WIN_H))
        pygame.draw.line(surface, WHITE, (ROAD_X, 0), (ROAD_X, WIN_H), 4)
        pygame.draw.line(surface, WHITE, (ROAD_X + ROAD_W, 0), (ROAD_X + ROAD_W, WIN_H), 4)
        for lane in range(1, LANE_COUNT):
            x = ROAD_X + lane * LANE_W
            y = -self.offset
            while y < WIN_H:
                pygame.draw.rect(surface, YELLOW, (x - 2, int(y), 4, 30))
                y += 60
 

class PlayerCar:
    def __init__(self, color):
        self.lane    = 1
        self.x       = float(lane_center_x(self.lane))
        self.y       = WIN_H - 120
        self.color   = color
        self.speed_x = 0
        self.shield  = False
        self.nitro   = False
        self.nitro_end   = 0
        self.shield_hits = 0
 
    @property
    def rect(self):
        return pygame.Rect(int(self.x) - CAR_W // 2,
                           int(self.y) - CAR_H // 2,
                           CAR_W, CAR_H)
 
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
 
    def move_right(self):
        if self.lane < LANE_COUNT - 1:
            self.lane += 1
 
    def update(self):
        target_x = float(lane_center_x(self.lane))
        self.x += (target_x - self.x) * 0.2

        if self.nitro and pygame.time.get_ticks() > self.nitro_end:
            self.nitro = False
 
    def activate_nitro(self, duration_ms=4000):
        self.nitro = True
        self.nitro_end = pygame.time.get_ticks() + duration_ms
 
    def activate_shield(self):
        self.shield = True
        self.shield_hits = 1
 
    def take_hit(self):
        if self.shield and self.shield_hits > 0:
            self.shield_hits -= 1
            if self.shield_hits == 0:
                self.shield = False
            return False
        return True
 
    def draw(self, surface):
        r = self.rect
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        roof = pygame.Rect(r.x + 8, r.y + 12, r.w - 16, r.h - 28)
        pygame.draw.rect(surface, tuple(max(0, c - 60) for c in self.color),
                         roof, border_radius=4)
        for wx, wy in [(r.x - 5, r.y + 8), (r.x + r.w - 3, r.y + 8),
                       (r.x - 5, r.y + r.h - 20), (r.x + r.w - 3, r.y + r.h - 20)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 8, 14), border_radius=2)
        if self.shield:
            pygame.draw.ellipse(surface, CYAN,
                                r.inflate(16, 16), 3)
        if self.nitro:
            flame_x = r.centerx + random.randint(-6, 6)
            flame_y = r.bottom
            pygame.draw.polygon(surface, ORANGE,
                                [(flame_x - 8, flame_y),
                                 (flame_x + 8, flame_y),
                                 (flame_x, flame_y + random.randint(15, 25))])
 

ENEMY_COLORS = [RED, (180, 0, 0), (200, 100, 0), (100, 0, 180), (0, 140, 0)]
 
 
class EnemyCar:
    def __init__(self, speed):
        self.lane  = random.randint(0, LANE_COUNT - 1)
        self.x     = float(lane_center_x(self.lane))
        self.y     = float(-ENEMY_H)
        self.speed = speed
        self.color = random.choice(ENEMY_COLORS)
 
    @property
    def rect(self):
        return pygame.Rect(int(self.x) - ENEMY_W // 2,
                           int(self.y) - ENEMY_H // 2,
                           ENEMY_W, ENEMY_H)
 
    def update(self, road_speed):
        self.y += road_speed + self.speed
 
    def is_off_screen(self):
        return self.y > WIN_H + ENEMY_H
 
    def draw(self, surface):
        r = self.rect
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        roof = pygame.Rect(r.x + 8, r.y + 10, r.w - 16, r.h - 24)
        pygame.draw.rect(surface, tuple(max(0, c - 50) for c in self.color),
                         roof, border_radius=4)
        for wx, wy in [(r.x - 5, r.y + 8), (r.x + r.w - 3, r.y + 8),
                       (r.x - 5, r.y + r.h - 18), (r.x + r.w - 3, r.y + r.h - 18)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 8, 12), border_radius=2)
 

OBS_TYPES = ["oil", "barrier", "bump"]
OBS_COLORS = {"oil": (20, 20, 20), "barrier": (255, 60, 0), "bump": BROWN}
 
 
class Obstacle:
    def __init__(self):
        self.lane = random.randint(0, LANE_COUNT - 1)
        self.x    = float(lane_center_x(self.lane))
        self.y    = float(-OBS_H)
        self.kind = random.choice(OBS_TYPES)
        self.color = OBS_COLORS[self.kind]
 
    @property
    def rect(self):
        return pygame.Rect(int(self.x) - OBS_W // 2,
                           int(self.y) - OBS_H // 2,
                           OBS_W, OBS_H)
 
    def update(self, road_speed):
        self.y += road_speed
 
    def is_off_screen(self):
        return self.y > WIN_H + OBS_H
 
    def draw(self, surface):
        r = self.rect
        if self.kind == "oil":
            pygame.draw.ellipse(surface, self.color, r)
            pygame.draw.ellipse(surface, (60, 60, 80),
                                r.inflate(-10, -6), 2)
        elif self.kind == "barrier":
            pygame.draw.rect(surface, self.color, r, border_radius=4)
            pygame.draw.rect(surface, WHITE, r, 2, border_radius=4)
            # Полосы
            for i in range(3):
                sx = r.x + 4 + i * 12
                pygame.draw.line(surface, WHITE,
                                 (sx, r.y + 4), (sx + 6, r.bottom - 4), 2)
        else:
            pygame.draw.ellipse(surface, self.color, r)
 

COIN_VALUES = {1: YELLOW, 3: ORANGE, 5: CYAN}
 
 
class Coin:
    def __init__(self):
        self.lane  = random.randint(0, LANE_COUNT - 1)
        self.x     = float(lane_center_x(self.lane))
        self.y     = float(-COIN_R)
        self.value = random.choices([1, 3, 5], weights=[60, 30, 10])[0]
        self.color = COIN_VALUES[self.value]
 
    @property
    def rect(self):
        return pygame.Rect(int(self.x) - COIN_R, int(self.y) - COIN_R,
                           COIN_R * 2, COIN_R * 2)
 
    def update(self, road_speed):
        self.y += road_speed
 
    def is_off_screen(self):
        return self.y > WIN_H + COIN_R
 
    def draw(self, surface):
        pygame.draw.circle(surface, self.color,
                           (int(self.x), int(self.y)), COIN_R)
        pygame.draw.circle(surface, WHITE,
                           (int(self.x), int(self.y)), COIN_R, 2)
        f = pygame.font.SysFont("Arial", 11, bold=True)
        lbl = f.render(str(self.value), True, BLACK)
        surface.blit(lbl, (int(self.x) - lbl.get_width() // 2,
                           int(self.y) - lbl.get_height() // 2))
 

PU_NITRO  = "nitro"
PU_SHIELD = "shield"
PU_REPAIR = "repair"
 
PU_COLORS  = {PU_NITRO: ORANGE, PU_SHIELD: CYAN, PU_REPAIR: GREEN}
PU_LABELS  = {PU_NITRO: "N", PU_SHIELD: "S", PU_REPAIR: "R"}
PU_TIMEOUT = 7000
 
 
class PowerUp:
    def __init__(self):
        self.lane  = random.randint(0, LANE_COUNT - 1)
        self.x     = float(lane_center_x(self.lane))
        self.y     = float(-POWERUP_W)
        self.kind  = random.choices(
            [PU_NITRO, PU_SHIELD, PU_REPAIR], weights=[40, 35, 25]
        )[0]
        self.color      = PU_COLORS[self.kind]
        self.spawn_time = pygame.time.get_ticks()
 
    @property
    def rect(self):
        hw = POWERUP_W // 2
        return pygame.Rect(int(self.x) - hw, int(self.y) - hw,
                           POWERUP_W, POWERUP_W)
 
    def update(self, road_speed):
        self.y += road_speed
 
    def is_off_screen(self):
        return self.y > WIN_H + POWERUP_W
 
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > PU_TIMEOUT
 
    def draw(self, surface):
        r = self.rect
        elapsed = pygame.time.get_ticks() - self.spawn_time
        if elapsed > PU_TIMEOUT - 2000 and (elapsed // 200) % 2 == 0:
            return
        pygame.draw.rect(surface, self.color, r, border_radius=8)
        pygame.draw.rect(surface, WHITE, r, 2, border_radius=8)
        f = pygame.font.SysFont("Arial", 16, bold=True)
        lbl = f.render(PU_LABELS[self.kind], True, BLACK)
        surface.blit(lbl, (r.centerx - lbl.get_width() // 2,
                           r.centery - lbl.get_height() // 2))
 

class NitroStrip:
    def __init__(self):
        self.lane  = random.randint(0, LANE_COUNT - 1)
        self.x     = ROAD_X + self.lane * LANE_W
        self.y     = float(-20)
        self.w     = LANE_W
        self.h     = 20
 
    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)
 
    def update(self, road_speed):
        self.y += road_speed
 
    def is_off_screen(self):
        return self.y > WIN_H
 
    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 80),
                         (int(self.x), int(self.y), self.w, self.h))
        f = pygame.font.SysFont("Arial", 11, bold=True)
        lbl = f.render("NITRO", True, BLACK)
        surface.blit(lbl, (int(self.x) + (self.w - lbl.get_width()) // 2,
                           int(self.y) + 3))