import pygame
import random
import sys
from collections import deque

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 448
SCREEN_HEIGHT = 576
FPS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pac-Man AI')

# Clock to control frame rate
clock = pygame.time.Clock()

# Maze layout
MAZE_TEMPLATE_PLAYER = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#......##....##....##......#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

MAZE_TEMPLATE_AI = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#......##....##....##......#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# Convert maze to a list of lists for mutability
def create_maze(template):
    return [list(row) for row in template]

# Create Pac-Man class
class Pacman:
    def __init__(self, x, y, color=YELLOW):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.lives = 3
        self.score = 0
        self.color = color

    def move(self, maze):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]

        if maze[new_y][new_x] != '#':
            self.x = new_x
            self.y = new_y

            # Check if Pac-Man consumes a dot
            if maze[self.y][self.x] == '.':
                maze[self.y][self.x] = ' '  # Consumed dot
                self.score += 10  # Increment score

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x * 16 + 8, self.y * 16 + 8), 8)

    def reset_position(self):
        """Reset Pac-Man's position after losing a life"""
        self.x, self.y = 13, 23
        self.direction = (0, 0)

# Create Ghost class
class Ghost:
    def __init__(self, x, y, color=RED):
        self.x = x
        self.y = y
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.color = color

    def move(self, maze):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]

        # If the ghost hits a wall, it changes direction
        if maze[new_y][new_x] == '#':
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        else:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x * 16 + 8, self.y * 16 + 8), 8)

# Pac-Man AI class (using BFS pathfinding)
class PacmanAI(Pacman):
    def __init__(self, x, y, color=GREEN):
        super().__init__(x, y, color)

    def move(self, maze):
        path = bfs(maze, (self.x, self.y))
        if path:
            # Move towards the next direction in the path
            self.direction = path[0]
        else:
            # If no path found, stand still
            self.direction = (0, 0)
        super().move(maze)

# BFS function to find nearest pellet
def bfs(maze, start):
    rows = len(maze)
    cols = len(maze[0])
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    while queue:
        (x, y), path = queue.popleft()

        if maze[y][x] == '.':
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y][new_x] != '#' and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.append(((new_x, new_y), path + [(dx, dy)]))

    return []

# Main menu to select game mode
def main_menu():
    font = pygame.font.Font(None, 36)
    options = ["1. Player", "2. CPU", "3. Player vs CPU"]
    selected = 0

    while True:
        screen.fill(BLACK)

        for i, option in enumerate(options):
            color = WHITE if i == selected else BLUE
            text = font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected

# Pause functionality
def pause_game():
    font = pygame.font.Font(None, 48)
    pause_text = font.render("Paused - Press P to Resume", True, WHITE)
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    paused = True
    while paused:
        screen.blit(pause_text, pause_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False  # Resume game

# Draw maze
def draw_maze(maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, pygame.Rect(x * 16, y * 16, 16, 16))
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, (x * 16 + 8, y * 16 + 8), 2)

# Check for ghost collision
def check_collision(pacman, ghosts):
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            return True
    return False

# Check for remaining dots in the maze
def check_remaining_dots(maze):
    return any('.' in row for row in maze)

# Game over screen
def game_over_screen(score):
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    while True:
        screen.fill(BLACK)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Restart the game

# Main game loop
def main_game(selected_mode):
    # Create maze
    maze_ai = None  # Initialize maze_ai to None
    if selected_mode == 0:  # Player mode
        maze = create_maze(MAZE_TEMPLATE_PLAYER)
    elif selected_mode == 1:  # AI mode
        maze = create_maze(MAZE_TEMPLATE_AI)
    elif selected_mode == 2:  # Player vs AI
        maze = create_maze(MAZE_TEMPLATE_PLAYER)  # Player maze for player
        maze_ai = create_maze(MAZE_TEMPLATE_AI)  # AI maze for AI

    # Initialize Pac-Man and Ghosts
    pacman = Pacman(1, 1)
    ghosts = [Ghost(7, 7), Ghost(8, 8)]
    pacman_ai = PacmanAI(1, 1) if selected_mode == 1 or selected_mode == 2 else None

    while True:
        # Draw the maze and entities
        screen.fill(BLACK)
        draw_maze(maze)

        # Draw Pac-Man and Ghosts
        if pacman:
            pacman.draw(screen)

        if pacman_ai:
            pacman_ai.draw(screen)

        for ghost in ghosts:
            ghost.draw(screen)

        # Display score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {pacman.score}", True, WHITE)
        lives_text = font.render(f"Lives: {pacman.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        # Check for win condition
        if not check_remaining_dots(maze):
            # Display win message or do something when all dots are consumed
            print("You win!")
            pygame.quit()
            sys.exit()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game()  # Pause game
                if event.key == pygame.K_LEFT:
                    pacman.direction = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    pacman.direction = (1, 0)
                if event.key == pygame.K_UP:
                    pacman.direction = (0, -1)
                if event.key == pygame.K_DOWN:
                    pacman.direction = (0, 1)

        # Move Pac-Man and AI
        if pacman:
            pacman.move(maze)

        if pacman_ai:
            pacman_ai.move(maze_ai)

        # Move Ghosts
        for ghost in ghosts:
            ghost.move(maze)

        # Check for collisions
        if pacman and check_collision(pacman, ghosts):
            pacman.lives -= 1  # Decrement life
            if pacman.lives <= 0:
                game_over_screen(pacman.score)  # Show game over screen
                return  # Restart game
            pacman.reset_position()  # Reset Pac-Man's position on collision

        # Refresh the display
        pygame.display.flip()
        clock.tick(FPS)

# Start the game
if __name__ == "__main__":
    selected_mode = main_menu()
    main_game(selected_mode)
