import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# --- Configuración ---
CELL = 20
COLS, ROWS = 30, 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
FPS = 10

# Colores
BLACK = (0, 0, 0)
GREEN = (28, 179, 27)
DARK_GREEN = (20, 120, 20)
RED = (145, 16, 16)
WHITE = (255, 255, 255)
BLACK_EYE = (0, 0, 0)

# Ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Serpiente inicial: 3 segmentos centrados
snake = [
    (COLS//2 + 1, ROWS//2),
    (COLS//2,     ROWS//2),
    (COLS//2 - 1, ROWS//2)
]
direction = (1, 0)  # derecha
food = (random.randint(0, COLS-1), random.randint(0, ROWS-1))

def draw():
    screen.fill(BLACK)

    # Dibujar comida (cuadrada y pequeña)
    fx, fy = food
    food_rect = pygame.Rect(fx*CELL + CELL//4, fy*CELL + CELL//4, CELL//2, CELL//2)
    pygame.draw.rect(screen, RED, food_rect)

    # Dibujar cuerpo en línea recta
    for x, y in snake[1:]:
        cx = x * CELL + CELL // 2
        cy = y * CELL + CELL // 2
        pygame.draw.circle(screen, DARK_GREEN, (cx, cy), CELL//2 + 1.5)  # cuerpo pegado

    # Dibujar cabeza encima de todo
    hx, hy = snake[0]
    cx, cy = hx*CELL + CELL//2, hy*CELL + CELL//2
    pygame.draw.circle(screen, GREEN, (cx, cy), CELL//2 + 2.5)

    # Carita de la cabeza
    eye_offset = CELL//4
    eye_radius = 2
    pygame.draw.circle(screen, WHITE, (cx - eye_offset//2, cy - eye_offset//2), eye_radius)
    pygame.draw.circle(screen, WHITE, (cx + eye_offset//2, cy - eye_offset//2), eye_radius)
    pygame.draw.circle(screen, BLACK_EYE, (cx - eye_offset//2, cy - eye_offset//2), 1)
    pygame.draw.circle(screen, BLACK_EYE, (cx + eye_offset//2, cy - eye_offset//2), 1)
    mouth_offset = CELL//6
    pygame.draw.arc(screen, BLACK_EYE, (cx - mouth_offset, cy, mouth_offset*2, mouth_offset), 3.14, 0, 2)

    pygame.display.flip()

def move():
    global snake, food
    head_x, head_y = snake[0]
    dx, dy = direction

    # Wrap-around en bordes
    new_head = ((head_x + dx) % COLS, (head_y + dy) % ROWS)

    # Comer comida
    if new_head == food:
        snake.insert(0, new_head)
        food = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
    else:
        snake.insert(0, new_head)
        snake.pop()

# --- Bucle principal ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and direction != (0, 1):
        direction = (0, -1)
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and direction != (0, -1):
        direction = (0, 1)
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and direction != (1, 0):
        direction = (-1, 0)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and direction != (-1, 0):
        direction = (1, 0)

    move()
    draw()
    clock.tick(FPS)

pygame.quit()
sys.exit()
