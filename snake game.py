print("Helloooooo")

# =============================================================================
# 🐍 SNAKE GAME — Beginner Python Project
# =============================================================================
# HOW TO RUN:
#   1. Install pygame:  pip install pygame
#   2. Run this file:   python snake.py
# =============================================================================

import pygame
import random

# -----------------------------------------------------------------------------
# MILESTONE 1 — CONSTANTS (the settings of our game world)
# -----------------------------------------------------------------------------
# TODO: Try changing these values and see what happens!

WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 600
CELL_SIZE     = 30          # Each grid square is 30x30 pixels

# How many cells fit across/down the grid?
GRID_COLS = WINDOW_WIDTH  // CELL_SIZE
GRID_ROWS = WINDOW_HEIGHT // CELL_SIZE

FPS = 2                   # Frames per second — controls game speed

# Colours (Red, Green, Blue) — values from 0 to 255
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = ( 50, 205,  50)
DARK_GREEN = ( 34, 139,  34)
RED        = (220,  20,  60)
GRAY       = ( 40,  40,  40)


# -----------------------------------------------------------------------------
# MILESTONE 2 — DRAWING FUNCTIONS
# -----------------------------------------------------------------------------

def draw_grid(surface):
    """Draw faint grid lines so we can see the cells."""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_snake(surface, snake):
    """
    Draw every segment of the snake.

    `snake` is a list of (col, row) tuples, e.g. [(5,5), (4,5), (3,5)]
    The FIRST item is the HEAD, the LAST item is the TAIL.

    TODO: Loop over each segment and draw a filled rectangle.
          Hint: pixel_x = col * CELL_SIZE,  pixel_y = row * CELL_SIZE
          Hint: pygame.draw.rect(surface, colour, (x, y, width, height))
          BONUS: draw the head in a slightly different colour (DARK_GREEN).
    """
    for i, segment in enumerate(snake):
        col, row = segment
        x = col * CELL_SIZE
        y = row * CELL_SIZE

        colour = DARK_GREEN if i == 0 else GREEN  # head vs body
        pygame.draw.rect(surface, colour, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, GREEN,  (x, y, CELL_SIZE, CELL_SIZE), 1)  # border


def draw_food(surface, food):
    """
    Draw the food as a red square.

    TODO: Draw a rectangle at the food's (col, row) position.
          The formula is the same as draw_snake above.
    """
    col, row = food
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    pygame.draw.circle(surface, RED, (x + CELL_SIZE/2, y + CELL_SIZE/2), CELL_SIZE/2)
    pygame.draw.circle(surface, WHITE, (x + CELL_SIZE/2, y + CELL_SIZE/2), CELL_SIZE/2, 1)

def draw_score(surface, score, font):
    """Render the score text in the top-left corner."""
    text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text, (10, 10))


# -----------------------------------------------------------------------------
# MILESTONE 3 — MOVING THE SNAKE  ⬅️ Most important logic in the game!
# -----------------------------------------------------------------------------

def move_snake(snake, direction):
    """
    Move the snake ONE step in `direction`.

    direction is a (dc, dr) tuple:
        UP    = ( 0, -1)
        DOWN  = ( 0, +1)
        LEFT  = (-1,  0)
        RIGHT = (+1,  0)

    HOW MOVEMENT WORKS:
        1. Calculate the new head position (old head + direction).
        2. Insert the new head at the FRONT of the list.
        3. Remove the TAIL (last item) — this makes the snake appear to slide.
           (When the snake eats food, we skip step 3 so it grows!)

    TODO: Complete this function.
          Hint: new_head = (head_col + dc, head_row + dr)
          Hint: snake.insert(0, new_head)   ← adds to the front
          Hint: snake.pop()                 ← removes from the back
          This function should RETURN the new head position.
    """
    head_col, head_row = snake[0]
    dc, dr = direction

    new_head = (head_col + dc, head_row + dr)

    snake.insert(0, new_head)
    snake.pop()             # comment this line out — watch what happens!

    return new_head


def grow_snake(snake, direction):
    """
    Move the snake AND grow it by 1 (called when food is eaten).

    TODO: This is almost identical to move_snake — what's the ONE difference?
          (Answer: don't call snake.pop() — keep the tail!)
    """
    head_col, head_row = snake[0]
    dc, dr = direction

    new_head = (head_col + dc, head_row + dr)
    snake.insert(0, new_head)
    # ← Notice: no snake.pop() here!

    return new_head


# -----------------------------------------------------------------------------
# MILESTONE 5 — FOOD SPAWNING
# -----------------------------------------------------------------------------

def spawn_food(snake):
    """
    Pick a random grid cell that is NOT occupied by the snake.

    TODO: Use a while loop to keep picking random positions until
          you find one that isn't in the snake list.
          Hint: random.randint(0, GRID_COLS - 1)
    """
    while True:
        col = random.randint(0, GRID_COLS - 1)
        row = random.randint(0, GRID_ROWS - 1)
        if (col, row) not in snake:
            return (col, row)


# -----------------------------------------------------------------------------
# MILESTONE 6 — COLLISION DETECTION
# -----------------------------------------------------------------------------

def is_wall_collision(head):
    """
    Return True if the head has gone outside the grid boundaries.

    TODO: Check if head_col < 0, head_col >= GRID_COLS,
                  head_row < 0, head_row >= GRID_ROWS.
    """
    col, row = head
    return col < 0 or col >= GRID_COLS or row < 0 or row >= GRID_ROWS


def is_self_collision(snake):
    """
    Return True if the head has collided with any part of the body.

    TODO: Check if snake[0] appears anywhere in snake[1:]
          Hint: the `in` keyword works on lists!
    """
    return snake[0] in snake[1:]


# -----------------------------------------------------------------------------
# MILESTONE 4 — HANDLING KEYBOARD INPUT
# -----------------------------------------------------------------------------

def handle_direction_change(event, current_direction):
    """
    Return a new direction based on the arrow key pressed.
    Prevents the snake from reversing into itself.

    TODO: Map each arrow key to a direction tuple.
          Add a guard: you can't go LEFT if you're currently going RIGHT, etc.

    Pygame key constants: pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
    """
    UP    = ( 0, -1)
    DOWN  = ( 0, +1)
    LEFT  = (-1,  0)
    RIGHT = (+1,  0)

    opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

    key_map = {
        pygame.K_UP:    UP,
        pygame.K_DOWN:  DOWN,
        pygame.K_LEFT:  LEFT,
        pygame.K_RIGHT: RIGHT,
    }

    if event.key in key_map:
        new_direction = key_map[event.key]
        # TODO: add the guard clause here — block reversal
        if new_direction != opposite[current_direction]:
            return new_direction

    return current_direction   # no valid key pressed — keep going


# -----------------------------------------------------------------------------
# GAME OVER SCREEN
# -----------------------------------------------------------------------------

def show_game_over(surface, score, font_big, font_small):
    """Display a game-over message and wait for the player to press R or Q."""
    surface.fill(BLACK)

    msg1 = font_big.render("GAME OVER", True, RED)
    msg2 = font_small.render(f"Score: {score}", True, WHITE)
    msg3 = font_small.render("Press R to restart  |  Q to quit", True, GRAY)

    surface.blit(msg1, msg1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60)))
    surface.blit(msg2, msg2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)))
    surface.blit(msg3, msg3.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)))

    pygame.display.flip()

    # Wait for R (restart) or Q (quit)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True     # restart
                if event.key == pygame.K_q:
                    return False    # quit


# -----------------------------------------------------------------------------
# MAIN — The Game Loop  🔁
# -----------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("🐍 Snake")
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont("monospace", 52, bold=True)
    font_small = pygame.font.SysFont("monospace", 26)

    # ── Game state ──────────────────────────────────────────────────────────
    # The snake starts as 3 segments in the middle of the grid, facing right.
    # TODO: What does this list represent? Discuss with your teacher!
    start_col = GRID_COLS // 2
    start_row = GRID_ROWS // 2
    snake     = [(start_col, start_row),
                 (start_col - 1, start_row),
                 (start_col - 2, start_row)]

    direction = (1, 0)      # starting direction: RIGHT
    food      = spawn_food(snake)
    score     = 0
    running   = True

    # ── Game loop ────────────────────────────────────────────────────────────
    while running:

        # 1. HANDLE EVENTS (keyboard, window close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                direction = handle_direction_change(event, direction)

        # 2. UPDATE GAME STATE
        if food == snake[0]:
            # TODO: Why do we check BEFORE moving? Try moving this check
            #       to AFTER the move and see what breaks.
            pass

        ate_food = (food == snake[0])   # will the head land on food?

        if ate_food:
            new_head = grow_snake(snake, direction)
            food  = spawn_food(snake)
            score += 1
        else:
            new_head = move_snake(snake, direction)

        # 3. CHECK COLLISIONS
        if is_wall_collision(new_head) or is_self_collision(snake):
            restart = show_game_over(screen, score, font_big, font_small)
            if restart:
                main()      # restart by calling main() again
            return

        # 4. DRAW EVERYTHING
        screen.fill(BLACK)
        draw_grid(screen)
        draw_food(screen, food)
        draw_snake(screen, snake)
        draw_score(screen, score, font_small)
        pygame.display.flip()

        # 5. TICK — control game speed
        # BONUS TODO: make the snake speed up as score increases!
        clock.tick(FPS)

    pygame.quit()


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
