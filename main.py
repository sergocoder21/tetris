import pygame
import random

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128), 
]

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = COLORS[random.randint(1, len(COLORS) - 1)]
        return {'shape': shape, 'color': color, 'x': GRID_WIDTH // 2 - len(shape[0]) // 2, 'y': 0}

    def rotate_piece(self):
        self.current_piece['shape'] = [list(row) for row in zip(*self.current_piece['shape'][::-1])]

    def valid_position(self, dx=0, dy=0):
        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block:
                    new_x = self.current_piece['x'] + x + dx
                    new_y = self.current_piece['y'] + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and self.grid[new_y][new_x]):
                        return False
        return True

    def merge_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.valid_position():
            self.reset()

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)
            self.score += 1

    def reset(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(surface, block, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(surface, self.current_piece['color'], ((self.current_piece['x'] + x) * BLOCK_SIZE, (self.current_piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode ((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris Game")
    clock = pygame.time.Clock()
    tetris = Tetris()
    font = pygame.font.Font(None, 36)
    running = True
    show_data = False

    while running:
        screen.fill((0, 0, 0))
        tetris.draw(screen)

        if show_data:    
            fps = clock.get_fps()
            fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
            screen.blit(fps_text, (10, 10))

            position_text = font.render(f"Position: ({tetris.current_piece['x']}, {tetris.current_piece['y']})", True, (255, 255, 255))
            screen.blit(position_text, (10, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and tetris.valid_position(dx=-1):
                    tetris.current_piece['x'] -= 1
                elif event.key == pygame.K_RIGHT and tetris.valid_position(dx=1):
                    tetris.current_piece['x'] += 1
                elif event.key == pygame.K_DOWN and tetris.valid_position(dy=1):
                    tetris.current_piece['y'] += 1
                elif event.key == pygame.K_UP:
                    tetris.rotate_piece()
                    if not tetris.valid_position():
                        tetris.rotate_piece()
                elif event.key == pygame.K_q:
                    show_data = not show_data

        if tetris.valid_position(dy=1):
            tetris.current_piece['y'] += 1
        else:
            tetris.merge_piece()

        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()