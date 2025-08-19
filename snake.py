import sys
import pygame

# --- Configuración ---
CELL = 20
COLS, ROWS = 30, 20                # tablero 30x20 celdas
WIDTH, HEIGHT = COLS*CELL, ROWS*CELL
FPS = 10                           # velocidad del juego (pasos por segundo)

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Movimiento")
clock = pygame.time.Clock()

# Serpiente: 3 segmentos centrados, moviéndose a la derecha
snake = [(COLS//2 + 1, ROWS//2),
         (COLS//2,     ROWS//2),
         (COLS//2 - 1, ROWS//2)]
direction = (1, 0)  # (dx, dy): derecha

def move_snake(snake, direction):
    head_x, head_y = snake[0]
    dx, dy = direction
    # Por ahora hacemos "wrap-around" (sale por un lado y entra por el otro)
    new_head = ((head_x + dx) % COLS, (head_y + dy) % ROWS)
    new_snake = [new_head] + snake[:-1]  # avanza sin crecer
    return new_snake

running = True
while running:
    # --- Eventos (teclado/cerrar ventana) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Evitar reversa inmediata
            if event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                direction = (-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                direction = (1, 0)
            elif event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                direction = (0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                direction = (0, 1)

    # --- Actualización ---
    snake = move_snake(snake, direction)

    # --- Dibujo ---
    screen.fill(BLACK)
    for (x, y) in snake:
        rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)
        pygame.draw.rect(screen, GREEN, rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
