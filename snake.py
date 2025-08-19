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
MAX_SCORE = 10  # puntaje para ganar

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
font = pygame.font.SysFont(None, 30)  # Fuente para marcador

# --- Variables de juego ---
def reset_game():
    global snake, direction, food, score, game_over
    snake = [
        (COLS//2 + 1, ROWS//2),
        (COLS//2,     ROWS//2),
        (COLS//2 - 1, ROWS//2)
    ]
    direction = (1, 0)
    food = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
    score = 0
    game_over = False

reset_game()

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
        pygame.draw.circle(screen, DARK_GREEN, (cx, cy), CELL//2 + 1.5)

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

    # Dibujar marcador
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 140, 10))

    # Si se acabó el juego, mostrar mensaje
    if game_over:
        msg = "¡Felicidades, ganaste!"
        sub_msg = "Presiona R para reiniciar o Q para salir"
        text = font.render(msg, True, WHITE)
        sub_text = font.render(sub_msg, True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()))
        screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()

def move():
    global snake, food, score, game_over
    if game_over:
        return

    head_x, head_y = snake[0]
    dx, dy = direction

    # Wrap-around en bordes
    new_head = ((head_x + dx) % COLS, (head_y + dy) % ROWS)

    # Comer comida
    if new_head == food:
        snake.insert(0, new_head)
        score += 1
        if score >= MAX_SCORE:
            game_over = True
        else:
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

        # Reiniciar o salir si el juego terminó
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_q:
                running = False

    keys = pygame.key.get_pressed()
    if not game_over:
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
