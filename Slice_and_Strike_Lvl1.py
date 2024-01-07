# PROTOTYPE 1

import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_Y = 300
BOARD_WIDTH = 200
KNIFE_SPEED = 12
BOARD_SPEED = 2
APPLE_SIZE = 13
APPLES_COUNT = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slice and Strike - LEVEL 1")

# Game variables
knives_count = 8
board_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
board_direction = 1
apples = [{'x': board_x + (i + 1) * (BOARD_WIDTH // (APPLES_COUNT + 1)), 'y': BOARD_Y - APPLE_SIZE, 'hit': False} for i in range(APPLES_COUNT)]
knife = {'x': SCREEN_WIDTH // 2, 'y': 0, 'dropped': False}
score = 0

# Function to check collision
def check_collision(knife, apple):
    distance = ((knife['x'] - apple['x']) ** 2 + (knife['y'] - apple['y']) ** 2) ** 0.5
    return distance < APPLE_SIZE

# Initialize font
pygame.font.init()  # Ensure the font module is initialized
font = pygame.font.SysFont(None, 36)  # You can change the font and size as needed

game_won = False
START, PLAYING, END = range(3) 
game_state = START

time_limit = 40  # 40 seconds time limit
start_time = None


# Main game loop
running = True
while running:
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == START:
                    game_state = PLAYING
                elif game_state == END:
                    running = False
                elif game_state == PLAYING and not knife['dropped']:
                    # Only drop a knife if the game is in the PLAYING state
                    knife['dropped'] = True
                    knives_count -= 1    
    
    
                
    screen.fill(WHITE)
        
    if game_state == START:
        # Display start screen with rules
        welcome_text = font.render("Welcome to Slice and Strike!", True, (0, 0, 0))
        rules_text = font.render("Press Space to Start.", True, (0, 0, 0))
        screen.blit(welcome_text, (200, 200))
        screen.blit(rules_text, (220, 250))
        
        
        
        
    
    elif game_state == PLAYING:
        
        
        
        # Start the timer when the game state changes to PLAYING
        if start_time is None:
            start_time = current_time

        elapsed_time = (current_time - start_time) / 1000  # Convert milliseconds to seconds
        remaining_time = max(time_limit - elapsed_time, 0)

        if remaining_time <= 0:
            # Time's up, end the game
            game_state = END
        
        
        
        # Update board and apple positions
        board_x += BOARD_SPEED * board_direction
        if board_x + BOARD_WIDTH > SCREEN_WIDTH or board_x < 0:
            board_direction *= -1
    
        # Update apple positions
        for i in range(APPLES_COUNT):
            apples[i]['x'] = board_x + (i + 1) * (BOARD_WIDTH // (APPLES_COUNT + 1))
    
    
        # Update knife position
        if knife['dropped']:
            knife['y'] += KNIFE_SPEED
    
            # Check collision with apples
            for apple in apples:
                if not apple['hit'] and check_collision(knife, apple):
                    apple['hit'] = True
                    score += 1
                    knife['dropped'] = False
                    knife['y'] = 0
                    # Do not decrement knives count here as it's already decremented on drop
                    break
    
            # Reset knife if it falls off screen
            if knife['y'] > SCREEN_HEIGHT:
                knife = {'x': SCREEN_WIDTH // 2, 'y': 0, 'dropped': False}
                # Do not decrement knives count here
    
        # Draw board
        pygame.draw.rect(screen, (0, 0, 0), (board_x, BOARD_Y - 10, BOARD_WIDTH, 20))
    
        # Draw apples (only if not hit)
        for apple in apples:
            if not apple['hit']:
                pygame.draw.circle(screen, RED, (apple['x'], apple['y']), APPLE_SIZE)
    
        # Draw knife
        pygame.draw.line(screen, (0, 0, 0), (knife['x'], knife['y']), (knife['x'], knife['y'] + 30), 3)
    
        # Display knives count and score
        font = pygame.font.SysFont(None, 36)
        knives_text = font.render(f"Knives Left: {knives_count}", True, (0, 0, 0))
        score_text = font.render(f"Score: {score}/{APPLES_COUNT}", True, (0, 0, 0))
        screen.blit(knives_text, (10, 10))
        screen.blit(score_text, (10, 50))        

        if score == APPLES_COUNT or knives_count <= 0:
            game_state = END
            
        time_text = font.render(f"Time Left: {int(remaining_time)}", True, (0, 0, 0))
        screen.blit(time_text, (SCREEN_WIDTH - 170, 10))

    
    
    elif game_state == END:
        # Display end screen with win/lose message
        if score == APPLES_COUNT:
            end_text = font.render("Congratulations! You win!", True, (0, 0, 0))
        else:
            end_text = font.render("Game Over! Try again.", True, (0, 0, 0))
        screen.blit(end_text, (250, 250))
        #replay_text = font.render("Press Space to Exit", True, (0, 0, 0))
        #screen.blit(replay_text, (220, 300))
    

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()






# CONCERNS:
# additional feature: need knife to remain on the board : end game when two knives collide
# time it takes for knife to regenerate could be shorter
# graphics 
#



