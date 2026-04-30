import pygame
from collections import deque

class PencilTool:

    def __init__(self):
        self.last_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.last_pos = pos
        pygame.draw.circle(canvas, color, pos, size // 2)

    def on_mouse_move(self, canvas, pos, color, size):
        if self.last_pos:
            pygame.draw.line(canvas, color, self.last_pos, pos, size)
        self.last_pos = pos

    def on_mouse_up(self, canvas, pos, color, size):
        self.last_pos = None

    def draw_preview(self, surface, pos, color, size):
        pass


class LineTool:

    def __init__(self):
        self.start_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.start_pos = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.start_pos:
            pygame.draw.line(canvas, color, self.start_pos, pos, size)
        self.start_pos = None

    def draw_preview(self, surface, pos, color, size):
        if self.start_pos:
            pygame.draw.line(surface, color, self.start_pos, pos, size)


class RectTool:
    def __init__(self):
        self.start_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.start_pos = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.start_pos:
            x = min(self.start_pos[0], pos[0])
            y = min(self.start_pos[1], pos[1])
            w = abs(pos[0] - self.start_pos[0])
            h = abs(pos[1] - self.start_pos[1])
            pygame.draw.rect(canvas, color, (x, y, w, h), size)
        self.start_pos = None

    def draw_preview(self, surface, pos, color, size):
        if self.start_pos:
            x = min(self.start_pos[0], pos[0])
            y = min(self.start_pos[1], pos[1])
            w = abs(pos[0] - self.start_pos[0])
            h = abs(pos[1] - self.start_pos[1])
            pygame.draw.rect(surface, color, (x, y, w, h), size)


class SquareTool:
    def __init__(self):
        self.start_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.start_pos = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.start_pos:
            side = max(abs(pos[0] - self.start_pos[0]),
                       abs(pos[1] - self.start_pos[1]))
            x = min(self.start_pos[0], self.start_pos[0] + (pos[0] - self.start_pos[0]))
            y = min(self.start_pos[1], self.start_pos[1] + (pos[1] - self.start_pos[1]))
            pygame.draw.rect(canvas, color, (x, y, side, side), size)
        self.start_pos = None

    def draw_preview(self, surface, pos, color, size):
        if self.start_pos:
            side = max(abs(pos[0] - self.start_pos[0]),
                       abs(pos[1] - self.start_pos[1]))
            x = min(self.start_pos[0], self.start_pos[0] + (pos[0] - self.start_pos[0]))
            y = min(self.start_pos[1], self.start_pos[1] + (pos[1] - self.start_pos[1]))
            pygame.draw.rect(surface, color, (x, y, side, side), size)


class CircleTool:
    def __init__(self):
        self.start_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.start_pos = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.start_pos:
            radius = int(((pos[0] - self.start_pos[0])**2 +
                          (pos[1] - self.start_pos[1])**2) ** 0.5)
            if radius > 0:
                pygame.draw.circle(canvas, color, self.start_pos, radius, size)
        self.start_pos = None

    def draw_preview(self, surface, pos, color, size):
        if self.start_pos:
            radius = int(((pos[0] - self.start_pos[0])**2 +
                          (pos[1] - self.start_pos[1])**2) ** 0.5)
            if radius > 0:
                pygame.draw.circle(surface, color, self.start_pos, radius, size)


class EraserTool:
    def __init__(self):
        self.last_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.last_pos = pos
        pygame.draw.circle(canvas, (255, 255, 255), pos, size * 2)

    def on_mouse_move(self, canvas, pos, color, size):
        if self.last_pos:
            pygame.draw.line(canvas, (255, 255, 255), self.last_pos, pos, size * 4)
        self.last_pos = pos

    def on_mouse_up(self, canvas, pos, color, size):
        self.last_pos = None

    def draw_preview(self, surface, pos, color, size):
        pygame.draw.circle(surface, (200, 200, 200), pos, size * 2, 1)


class FillTool:

    def on_mouse_down(self, canvas, pos, color, size):
        self._flood_fill(canvas, pos, color)

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        pass

    def draw_preview(self, surface, pos, color, size):
        pass

    def _flood_fill(self, canvas, start_pos, fill_color):

        x, y = start_pos
        w, h = canvas.get_size()

        target_color = canvas.get_at((x, y))[:3]
        fill_rgb = fill_color[:3] if len(fill_color) >= 3 else fill_color

        if target_color == tuple(fill_rgb):
            return

        queue = deque()
        queue.append((x, y))
        visited = set()
        visited.add((x, y))

        while queue:
            cx, cy = queue.popleft()
            if canvas.get_at((cx, cy))[:3] != target_color:
                continue
            canvas.set_at((cx, cy), fill_color)

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))


class RightTriangleTool:
    def __init__(self):
        self.start_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.start_pos = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.start_pos:
            x1, y1 = self.start_pos
            x2, y2 = pos
            pts = [(x1, y1), (x1, y2), (x2, y2)]
            pygame.draw.polygon(canvas, color, pts, size)
        self.start_pos = None

    def draw_preview(self, surface, pos, color, size):
        if self.start_pos:
            x1, y1 = self.start_pos
            x2, y2 = pos
            pts = [(x1, y1), (x1, y2), (x2, y2)]
            pygame.draw.polygon(surface, color, pts, size)


class RhombusTool:
    def __init__(self):
        self.start_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.start_pos = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.start_pos:
            cx = (self.start_pos[0] + pos[0]) // 2
            cy = (self.start_pos[1] + pos[1]) // 2
            pts = [
                (cx, self.start_pos[1]),
                (pos[0], cy),
                (cx, pos[1]),
                (self.start_pos[0], cy),
            ]
            pygame.draw.polygon(canvas, color, pts, size)
        self.start_pos = None

    def draw_preview(self, surface, pos, color, size):
        if self.start_pos:
            cx = (self.start_pos[0] + pos[0]) // 2
            cy = (self.start_pos[1] + pos[1]) // 2
            pts = [
                (cx, self.start_pos[1]),
                (pos[0], cy),
                (cx, pos[1]),
                (self.start_pos[0], cy),
            ]
            pygame.draw.polygon(surface, color, pts, size)