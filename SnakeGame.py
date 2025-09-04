import pygame
import random

pygame.init()

# --- config ---
WIDTH, HEIGHT = 600, 700
TILE = 20
FPS = 18  # steady speed regardless of snake length

# --- setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)  # for "GAME OVER" text

# snake state
snake = [(200, 200)]
snake_dir = (0, 0)

# food
food = pygame.Rect(
    random.randrange(0, WIDTH - TILE, TILE),
    random.randrange(0, HEIGHT - TILE, TILE),
    TILE, TILE
)

score = 0

# >>> ADD THIS: game state flag
game_over = False

def reset_game():
    global snake, snake_dir, food, score, game_over
    snake = [(200, 200)]
    snake_dir = (0, 0)
    food.topleft = (
        random.randrange(0, WIDTH - TILE, TILE),
        random.randrange(0, HEIGHT - TILE, TILE)
    )
    score = 0
    game_over = False  # clear Game Over

def draw_game_over():
    """Draw the Game Over screen."""
    screen.fill((0, 0, 0))
    title = big_font.render("GAME OVER", True, (255, 50, 50))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    hint = font.render("Press R to Restart or ESC to Quit", True, (180, 180, 180))
    # center them
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 5)))
    screen.blit(hint, hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))
    pygame.display.flip()

running = True
while running:
    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # >>> ADD THIS BLOCK: handle Game Over state (put this near the top of the loop)
    if game_over:
        if keys[pygame.K_r]:
            reset_game()
        if keys[pygame.K_ESCAPE]:
            running = False
        draw_game_over()
        clock.tick(FPS)  # keep loop steady on game over screen
        continue  # skip the rest of the gameplay update/draw

    # --- controls (no instant reverse) ---
    if keys[pygame.K_UP] and snake_dir != (0, TILE):
        snake_dir = (0, -TILE)
    elif keys[pygame.K_DOWN] and snake_dir != (0, -TILE):
        snake_dir = (0, TILE)
    elif keys[pygame.K_LEFT] and snake_dir != (TILE, 0):
        snake_dir = (-TILE, 0)
    elif keys[pygame.K_RIGHT] and snake_dir != (-TILE, 0):
        snake_dir = (TILE, 0)

    # --- update ---
    if snake_dir != (0, 0):
        head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, head)

        # eat food?
        if pygame.Rect(head, (TILE, TILE)).colliderect(food):
            score += 1
            # respawn food
            food.topleft = (
                random.randrange(0, WIDTH - TILE, TILE),
                random.randrange(0, HEIGHT - TILE, TILE)
            )
        else:
            snake.pop()

        # collisions (self or walls)
        if (head in snake[1:]
            or head[0] < 0 or head[0] >= WIDTH
            or head[1] < 0 or head[1] >= HEIGHT):
            # >>> CHANGE THIS: instead of reset_game(), trigger Game Over
            game_over = True

    # --- draw ---
    screen.fill((0, 0, 0))

    # snake
    for x, y in snake:
        pygame.draw.rect(screen, (0, 255, 0), (x, y, TILE, TILE))

    # food (draw once, not inside the snake loop)
    pygame.draw.rect(screen, (255, 0, 0), food)

    # score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # flip one time per frame and tick once per frame (keeps speed steady)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
